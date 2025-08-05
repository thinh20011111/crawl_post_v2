from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import os
import json
import random

def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/account.json"
    output_file = "data/facebook_posts.json"
    data_filename = "data/data.json"

    # Đọc dữ liệu tài khoản từ data.json
    with open(data_filename, 'r') as data_file:
        data = json.load(data_file)

    driver.maximize_window()

    try:
        # Đăng nhập vào Facebook một lần
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account["email"]
        password_facebook = facebook_account["password"]

        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(email_facebook, password_facebook)
        print("Đăng nhập thành công vào Facebook.")
        driver.back()  # Quay lại trang trước đó
        base_page.login_facebook(email_facebook, password_facebook)
        print("Đăng nhập lại thành công vào Facebook.")
        time.sleep(10)  # Đợi một chút để đảm bảo đăng nhập hoàn tất
        
        
        # Vòng lặp vô tận
        while True:
            # Đọc dữ liệu tài khoản từ account.json
            with open(accounts_filename, 'r') as file:
                accounts_data = json.load(file)

            # Xáo trộn danh sách tài khoản
            account_items = list(accounts_data.items())
            random.shuffle(account_items)  # Ngẫu nhiên thứ tự, không trùng lặp

            print("Bắt đầu chu kỳ crawl mới với danh sách tài khoản đã xáo trộn.")

            # Lặp qua danh sách tài khoản đã được shuffle
            for account_key, account_data in account_items:
                try:
                    print(f"\nĐang xử lý tài khoản: {account_key}")

                    group_url = account_data["url2"]
                    emso_username = account_data["username"]
                    emso_password = account_data["password"]
                    post_url = account_data["url1"]

                    num_posts = 1
                    success = base_page.scroll_to_element_and_crawl(
                        username=emso_username,
                        password=emso_password,
                        nums_post=num_posts,
                        crawl_page=group_url,
                        post_page=post_url,
                        page=True
                    )

                    if success:
                        print(f"Hoàn tất xử lý tài khoản: {account_key}")
                        base_page.clear_media_folder()
                        print(f"Đăng bài thành công, chờ 500 giây trước khi xử lý tài khoản tiếp theo.")
                        time.sleep(800)
                    else:
                        print(f"Không có bài đăng thành công, tiếp tục với tài khoản tiếp theo.")
                except Exception as e:
                    print(f"Đã gặp lỗi khi xử lý tài khoản {account_key}: {e}")
                    continue

            print("Đã hoàn tất xử lý tất cả các tài khoản trong chu kỳ này. Bắt đầu chu kỳ mới.")

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong quá trình chạy: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()