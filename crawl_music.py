import yt_dlp
import os

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

# Ví dụ URL YouTube
youtube_url = "https://www.youtube.com/watch?v=zDNOhR-Ms-I&list=RDMMnHP2y3EeshQ&index=9"
download_audio(youtube_url)
