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
    # chrome_options.add_argument("--headless")
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
        print("✅ Đăng nhập thành công vào Facebook.")
        time.sleep(60)  # Đợi một chút để đảm bảo đăng nhập hoàn tất
        print("🔄 Tiếp tục chạy sau khi đăng nhập Facebook.")

        # Vòng lặp vô tận
        while True:
            # Đọc dữ liệu tài khoản từ account.json
            with open(accounts_filename, 'r') as file:
                accounts_data = json.load(file)

            # Danh sách từ khóa ưu tiên
            priority_keywords = ["beat", "24h", "tintuc", "hong", "tin", "office"]

            priority_accounts = []
            non_priority_accounts = []

            # Phân loại account theo từ khóa
            for account_key, account_data in accounts_data.items():
                group_url = account_data.get("url2", "").lower()
                if any(keyword in group_url for keyword in priority_keywords):
                    priority_accounts.append((account_key, account_data))
                else:
                    non_priority_accounts.append((account_key, account_data))

            # Xáo trộn từng nhóm
            random.shuffle(priority_accounts)
            random.shuffle(non_priority_accounts)

            # In số lượng page
            print(f"\n🔑 Số page ưu tiên: {len(priority_accounts)}")
            print(f"📄 Số page còn lại: {len(non_priority_accounts)}")

            # Gộp danh sách: ưu tiên trước, sau đó là không ưu tiên
            account_items = priority_accounts + non_priority_accounts

            print(f"\n===== Bắt đầu chu kỳ crawl mới với {len(account_items)} tài khoản =====")

            # Lặp qua toàn bộ account
            for account_key, account_data in account_items:
                try:
                    print(f"\n[ACCOUNT] Đang xử lý: {account_key} - {account_data.get('url2')}")

                    group_url = account_data.get("url2", "")
                    emso_username = account_data.get("username")
                    emso_password = account_data.get("password")
                    post_url = account_data.get("url1")

                    if not group_url or not emso_username or not emso_password or not post_url:
                        print(f"[SKIP] Bỏ qua account {account_key} vì thiếu dữ liệu.")
                        continue

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
                        print(f"[DONE] Hoàn tất xử lý tài khoản: {account_key}")
                        base_page.clear_media_folder()
                        print("⏳ Nghỉ 300 giây trước khi xử lý account tiếp theo.")
                        time.sleep(115)
                    else:
                        print(f"[FAIL] Không crawl được bài đăng cho {account_key}, chuyển tiếp account khác.")

                except Exception as e:
                    import traceback
                    print(f"[ERROR] Lỗi khi xử lý tài khoản {account_key}: {e}")
                    traceback.print_exc()
                    continue

            print("\n===== Đã hoàn tất xử lý tất cả account. Bắt đầu vòng lặp mới =====")

    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng trong quá trình chạy: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
