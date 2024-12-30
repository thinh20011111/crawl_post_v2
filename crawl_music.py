import os
import csv
import uuid
import json
import requests
import yt_dlp

# Hàm tạo tên file duy nhất cho banner
def generate_unique_filename(extension="jpg"):
    return f"{uuid.uuid4().hex}.{extension}"

# Hàm tải âm thanh từ YouTube và lưu vào thư mục 'music'
def download_audio(youtube_url):
    # Tạo thư mục 'music' nếu chưa tồn tại
    music_folder = os.path.join(os.getcwd(), 'music')
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn chất lượng âm thanh tốt nhất
        'outtmpl': os.path.join(music_folder, '%(title)s.mp3'),  # Lưu vào thư mục 'music'
        'quiet': False,  # Hiển thị thông báo trong quá trình tải
        'noplaylist': True  # Không tải danh sách phát, chỉ tải video đơn
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# Hàm tải banner của video YouTube
def download_banner(youtube_url, media_folder="media"):
    # Tạo thư mục 'media' nếu chưa tồn tại
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    # Lấy ID video từ URL
    video_id = youtube_url.split('v=')[1].split('&')[0]
    
    # URL của thumbnail video
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    # Tải banner về
    response = requests.get(thumbnail_url)
    
    if response.status_code == 200:
        # Tạo tên file duy nhất cho banner
        banner_filename = generate_unique_filename("jpg")
        banner_path = os.path.join(media_folder, banner_filename)
        
        # Lưu banner vào thư mục media
        with open(banner_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Banner of video {video_id} has been downloaded successfully as {banner_filename}")
        return banner_filename
    else:
        print(f"Failed to retrieve the banner for video {video_id}")
        return None

# Hàm đọc file CSV và tải âm thanh + banner cho mỗi URL
def download_from_csv(csv_file):
    # Đọc dữ liệu từ file CSV và lấy URL trong cột A
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data_to_save = []  # Dữ liệu để lưu vào file JSON
        for row in reader:
            # Kiểm tra nếu có URL trong cột A (cột 0)
            if row:
                youtube_url = row[0]
                print(f"Downloading audio: {youtube_url}")
                
                # Tải âm thanh
                download_audio(youtube_url)
                
                # Tải banner và lấy tên file banner
                print(f"Downloading banner: {youtube_url}")
                banner_filename = download_banner(youtube_url)
                
                # Lưu thông tin vào danh sách
                mp3_filename = youtube_url.split('v=')[1].split('&')[0] + '.mp3'
                data_to_save.append({
                    "mp3_filename": mp3_filename,
                    "banner_filename": banner_filename
                })

        # Lưu thông tin vào file JSON
        json_file_path = os.path.join(os.getcwd(), 'media', "data/data_music.json")
        
        if os.path.exists(json_file_path):
            # Nếu tệp đã tồn tại, mở và đọc dữ liệu cũ
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = []
        
        # Thêm dữ liệu mới vào JSON
        existing_data.extend(data_to_save)
        
        # Ghi lại vào file JSON
        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        print(f"Data has been saved to {json_file_path}")

# Đọc file CSV có tên 'data_crawl_music.csv' và tải dữ liệu
csv_file = 'data/data_crawl_music.csv'
download_from_csv(csv_file)
