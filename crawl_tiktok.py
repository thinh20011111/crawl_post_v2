from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium_stealth import stealth
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
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/account_create_moment.json"  # Đọc dữ liệu tài khoản từ file account.json
    
    # Đọc dữ liệu tài khoản từ account.json
    with open(accounts_filename, 'r') as file:
        accounts_data = json.load(file)

    driver.maximize_window()
    try:
        # Lặp qua tất cả các tài khoản và xử lý
        num_posts_per_account = 2  # Số lượng bài viết cần crawl mỗi tài khoản

        for account_key, account_data in accounts_data.items():
            try:
                print(f"\nĐang xử lý tài khoản: {account_key}")

                # Lấy thông tin từ tài khoản
                emso_username = account_data["username"]
                emso_password = account_data["password"]

                # Crawl bài viết mới từ TikTok
                base_page.get_and_create_tiktok(
                    username=emso_username,
                    password=emso_password,
                    nums_post=num_posts_per_account,
                )

                print(f"Hoàn tất xử lý tài khoản: {account_key}")
                base_page.clear_media_folder()
                driver.refresh()
            except Exception as e:
                print(f"Đã gặp lỗi khi xử lý tài khoản {account_key}: {e}")
                continue  # Tiếp tục với tài khoản tiếp theo nếu gặp lỗi

        print("Đã hoàn tất xử lý tất cả các tài khoản.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
