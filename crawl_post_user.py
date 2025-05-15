import random
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
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/data_crawl_post_user.json"
    output_file = "data/facebook_posts.json"
    data_filename = "data/data.json"

    # Đọc dữ liệu tài khoản
    with open(accounts_filename, 'r', encoding='utf-8') as file:
        accounts_data = json.load(file)

    with open(data_filename, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)

    # Đọc danh sách các tài khoản đã crawl thành công
    crawled_accounts = set()
    crawled_file_path = "data/user_crawled.txt"
    if os.path.exists(crawled_file_path):
        with open(crawled_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "Tài khoản đã crawl thành công:" in line:
                    account = line.strip().split(":")[-1].strip()
                    crawled_accounts.add(account)

    # Lọc và trộn danh sách tài khoản chưa được crawl
    filtered_accounts_data = {
        key: value for key, value in accounts_data.items() if key not in crawled_accounts
    }
    account_items = list(filtered_accounts_data.items())
    random.shuffle(account_items)

    driver.maximize_window()

    try:
        # Đăng nhập Facebook một lần
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account["email"]
        password_facebook = facebook_account["password"]

        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(email_facebook, password_facebook)
        time.sleep(60)
        print("Đăng nhập thành công vào Facebook.")

        # Lặp qua danh sách tài khoản
        for account_key, account_data in account_items:
            try:
                print(f"\nĐang xử lý tài khoản: {account_key}")

                group_url = account_data["url2"]
                emso_username = account_data["username"]
                emso_password = account_data["password"]
                post_url = account_data["url1"]

                base_page.scroll_to_element_and_crawl(
                    username=emso_username,
                    password=emso_password,
                    nums_post=1,
                    crawl_page=group_url,
                    post_page=post_url,
                    page=False
                )

                print(f"Hoàn tất xử lý tài khoản: {account_key}")

                # Ghi lại tài khoản đã crawl
                with open(crawled_file_path, "a", encoding="utf-8") as file:
                    file.write(f"Tài khoản đã crawl thành công: {account_key}\n")

                base_page.clear_media_folder()
                print("Đợi 15p để xử lý user tiếp theo...")
                time.sleep(700)

            except Exception as e:
                print(f"Đã gặp lỗi khi xử lý tài khoản {account_key}: {e}")
                continue

        print("Đã hoàn tất xử lý tất cả các tài khoản.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
