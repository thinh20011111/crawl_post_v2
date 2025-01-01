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
    accounts_filename = "data/account.json"  # Đọc dữ liệu tài khoản từ file account.json
    data_filename = "data/data.json"
    
    # Đọc dữ liệu tài khoản từ account.json
    with open(accounts_filename, 'r') as file:
        accounts_data = json.load(file)
            
    with open(data_filename, 'r') as data_file:
        data = json.load(data_file)


    try:
        driver.get("https://www.tiktok.com/foryou")
        time.sleep(10)
        base_page.download_video_from_xpath("media")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
