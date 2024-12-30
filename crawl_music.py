import yt_dlp
import os
import csv

def download_audio(youtube_url):
    # Tạo thư mục 'music' trong thư mục hiện tại nếu chưa tồn tại
    music_folder = os.path.join(os.getcwd(), 'music')
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn chất lượng âm thanh tốt nhất
        'outtmpl': os.path.join(music_folder, '%(title)s.mp3'),  # Chỉ định thư mục 'music' trong dự án
        'quiet': False,  # Tắt chế độ im lặng để thấy thông báo
        'noplaylist': True  # Không tải danh sách phát, chỉ tải video đơn
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def download_from_csv(csv_file):
    # Đọc dữ liệu từ file CSV và lấy URL trong cột A
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Kiểm tra nếu có URL trong cột A (cột 0)
            if row:
                youtube_url = row[0]
                print(f"Downloading: {youtube_url}")
                download_audio(youtube_url)

# Đọc file CSV có tên 'data_crawl_music.csv'
csv_file = 'data/data_crawl_music.csv'
download_from_csv(csv_file)
