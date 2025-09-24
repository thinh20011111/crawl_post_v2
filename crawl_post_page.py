from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import json
import random


def run_account(base_page, account_key, account_data):
    """Xử lý crawl 1 account."""
    group_url = account_data.get("url2", "")
    emso_username = account_data.get("username")
    emso_password = account_data.get("password")
    post_url = account_data.get("url1")

    if not group_url or not emso_username or not emso_password or not post_url:
        print(f"[SKIP] Bỏ qua account {account_key} vì thiếu dữ liệu.")
        return False

    success = base_page.scroll_to_element_and_crawl(
        username=emso_username,
        password=emso_password,
        nums_post=1,
        crawl_page=group_url,
        post_page=post_url,
        page=True
    )

    if success:
        print(f"[DONE] Hoàn tất xử lý tài khoản: {account_key}")
        base_page.clear_media_folder()
        return True
    else:
        print(f"[FAIL] Không crawl được bài đăng cho {account_key}")
        return False


def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Chrome
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_page = BasePage(driver)
    accounts_filename = "data/account.json"
    data_filename = "data/data.json"

    # Đọc thông tin login Facebook
    with open(data_filename, "r") as data_file:
        data = json.load(data_file)

    driver.maximize_window()

    try:
        # Đăng nhập Facebook
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account.get("email")
        password_facebook = facebook_account.get("password")

        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(email_facebook, password_facebook)
        time.sleep(15)
        driver.back()
        base_page.login_facebook(email_facebook, password_facebook)

        print("✅ Đăng nhập thành công vào Facebook.")
        print("🔄 Bắt đầu chạy chương trình...")

        # Biến quản lý vòng lặp thường
        normal_index = 0
        normal_count = 0

        while True:
            # Đọc dữ liệu account
            with open(accounts_filename, "r") as file:
                accounts_data = json.load(file)

            # Tách ưu tiên và thường
            priority_keywords = ["beat", "24h", "tintuc", "hong", "tin", "office"]
            priority_accounts, normal_accounts = [], []

            for account_key, account_data in accounts_data.items():
                group_url = account_data.get("url2", "").lower()
                if any(keyword in group_url for keyword in priority_keywords):
                    priority_accounts.append((account_key, account_data))
                else:
                    normal_accounts.append((account_key, account_data))

            print(f"\n🔑 Page ưu tiên: {len(priority_accounts)}")
            print(f"📄 Page thường: {len(normal_accounts)}")

            # --- 1. Chạy 5 page ưu tiên ---
            if priority_accounts:
                selected_priority = random.sample(
                    priority_accounts, min(5, len(priority_accounts))
                )
                print(f"\n=== Bắt đầu block ưu tiên ({len(selected_priority)} page) ===")
                for account_key, account_data in selected_priority:
                    try:
                        print(f"[PRIORITY] Đang xử lý: {account_key} - {account_data.get('url2')}")
                        success = run_account(base_page, account_key, account_data)
                        if success:
                            print(f"⏳ Nghỉ {config.POST_DELAY} giây...\n")
                            time.sleep(config.POST_DELAY)
                    except Exception as e:
                        print(f"[ERROR] Lỗi ưu tiên {account_key}: {e}")

            # --- 2. Chạy page thường (tối đa 20) ---
            if normal_accounts:
                print(f"\n=== Bắt đầu block thường (tối đa 20 page) ===")
                while normal_count < 20:
                    account_key, account_data = normal_accounts[normal_index]

                    try:
                        print(f"[NORMAL] Đang xử lý: {account_key} - {account_data.get('url2')}")
                        success = run_account(base_page, account_key, account_data)
                        if success:
                            print(f"⏳ Nghỉ {config.POST_DELAY} giây...\n")
                            time.sleep(config.POST_DELAY)
                    except Exception as e:
                        print(f"[ERROR] Lỗi thường {account_key}: {e}")

                    # Tăng index + count
                    normal_index += 1
                    normal_count += 1

                    # Nếu hết list thường thì quay lại từ đầu
                    if normal_index >= len(normal_accounts):
                        print("🔄 Hết list thường, quay lại từ đầu.")
                        normal_index = 0

                # Reset bộ đếm sau khi xong 20 thường
                normal_count = 0

    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
