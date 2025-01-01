import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from utils.config import Config


def download_video(video_url, save_path, headers):
    """
    Tải video từ URL với header xác thực.
    """
    try:
        # Chỉ tải video từ URL HTTP/HTTPS hợp lệ
        if video_url.startswith("http"):
            response = requests.get(video_url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"Video đã được tải xuống: {save_path}")
            else:
                print(f"Không thể tải video từ {video_url} (Mã lỗi: {response.status_code})")
        else:
            print(f"URL video không hợp lệ: {video_url}")
    except Exception as e:
        print(f"Lỗi khi tải video: {e}")


def crawl_tiktok_foryou(download_folder="media", json_file="data/data_tiktok.json", num_posts=10):
    """
    Crawl video từ trang chủ TikTok (For You) và tải video với các header.
    """
    # Tạo thư mục media để lưu video nếu chưa có
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Tạo thư mục data nếu chưa có
    if not os.path.exists(os.path.dirname(json_file)):
        os.makedirs(os.path.dirname(json_file))

    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU khi chạy headless
    chrome_options.add_argument("--window-size=1920x1080")  # Thiết lập kích thước cửa sổ để tránh một số vấn đề hiển thị
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    video_data = []

    try:
        # Mở trang "For You" trên TikTok
        driver.get("https://www.tiktok.com/foryou")
        time.sleep(10)  # Chờ trang tải (có thể điều chỉnh)

        # Lấy cookie từ trình duyệt
        cookies = driver.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        # Cấu hình header bao gồm cookie
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Cookie": "; ".join([f"{key}={value}" for key, value in cookie_dict.items()])
        }

        # Cuộn để tải thêm video
        for _ in range(5):  # Điều chỉnh số lần cuộn nếu cần thiết
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

        # Lấy danh sách video
        videos = driver.find_elements(By.TAG_NAME, "video")
        print(f"Tìm thấy {len(videos)} video.")

        # Lấy thông tin video
        for i, video in enumerate(videos[:num_posts]):  # Giới hạn số video theo num_posts
            video_src = video.get_attribute("src")
            video_title = video.get_attribute("aria-label")  # Sử dụng aria-label hoặc tìm thuộc tính thích hợp
            if not video_title:
                video_title = video.get_attribute("data-title")  # Thử tìm title nếu aria-label không có
            if video_src:
                save_path = os.path.join(download_folder, f"video_{i + 1}.mp4")
                download_video(video_src, save_path, headers)
                # Lưu thông tin vào video_data
                video_data.append({
                    "title": video_title,
                    "filename": f"video_{i + 1}.mp4"
                })

        # Lưu dữ liệu vào file JSON
        if video_data:
            with open(json_file, "w", encoding="utf-8") as json_file:
                json.dump(video_data, json_file, ensure_ascii=False, indent=4)
            print(f"Dữ liệu đã được lưu vào {json_file}")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    crawl_tiktok_foryou(num_posts=10)
