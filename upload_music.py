from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import os
import json

def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    # chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU khi chạy headless
    chrome_options.add_argument("--window-size=1920x1080")  # Thiết lập kích thước cửa sổ để tránh một số vấn đề hiển thị
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    
    # Mở trang web
    base_page = BasePage(driver)
    data_filename = "data/page_music.json"
    music_filename = "data/data_music.json"
    
    # Đọc dữ liệu tài khoản từ account.json
    with open(data_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
            
    with open(music_filename, 'r', encoding='utf-8') as file:
        musics = json.load(file)
        
    try:
        page_music = data.get("page_music", {})
        page_name = page_music["pagename"]
        username = page_music["username"]
        password = page_music["password"]
        author = page_music["author"]
        description = page_music["description"]
        field = page_music["field"]
        
        first_music = musics[0]
        mp3_filename = first_music["mp3_filename"]
        song_name = os.path.splitext(mp3_filename)[0]
        music_banner = first_music["banner_filename"]
        
        base_page.login_emso(username, password)
        driver.get("https://staging-fe.emso.vn/music_space")
        base_page.upload_music(song_name, description, music_banner, mp3_filename, page_name, author, field)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
