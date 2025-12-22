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
    chrome_options.add_argument("--disable-features=PasswordCheck")
    chrome_options.add_argument("--disable-features=SafetyTipUI")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--incognito")  # Chế độ ẩn danh
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    # chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    base_page = BasePage(driver)
    accounts_filename = "data/account.json"
    data_filename = "data/data.json"
    
    # Đọc dữ liệu
    with open(accounts_filename, 'r') as file:
        accounts_data = json.load(file)
            
    with open(data_filename, 'r') as data_file:
        data = json.load(data_file)

    try:
        # Đăng nhập vào Facebook một lần
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account["email"]
        password_facebook = facebook_account["password"]

        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(email_facebook, password_facebook)
        time.sleep(60)
        print("Đăng nhập thành công vào Facebook.")

        # 🔹 Danh sách từ khóa ưu tiên
        priority_keywords = ["tintuc", "24h", "thethao", "Official", "beat", "news", "TV"]

        # 🔹 Sắp xếp tài khoản: tài khoản nào có url2 chứa từ khóa thì ưu tiên lên đầu
        def priority_sort(item):
            _, account_data = item
            url2 = account_data.get("url2", "").lower()
            # Nếu có chứa từ khóa thì giá trị = 0 (ưu tiên cao hơn)
            for keyword in priority_keywords:
                if keyword.lower() in url2:
                    return 0
            return 1  # Không chứa thì xếp sau

        sorted_accounts = sorted(accounts_data.items(), key=priority_sort)

        # Lặp qua các tài khoản đã sắp xếp
        for account_key, account_data in sorted_accounts:
            try:
                print(f"\nĐang xử lý tài khoản: {account_key}")

                group_url = account_data["url2"]
                emso_username = account_data["username"]
                emso_password = account_data["password"]
                post_url = account_data["url1"]

                num_posts = 1
                base_page.get_and_create_watch(
                    username=emso_username,
                    password=emso_password,
                    nums_post=num_posts,
                    crawl_page=group_url,
                    post_page=post_url
                )

                print(f"Hoàn tất xử lý tài khoản: {account_key}")
                base_page.clear_media_folder()

            except Exception as e:
                print(f"Đã gặp lỗi khi xử lý tài khoản {account_key}: {e}")
                continue

        print("Đã hoàn tất xử lý tất cả các tài khoản.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
