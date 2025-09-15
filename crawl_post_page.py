from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
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
    # chrome_options.add_argument("--headless")  # Tạm tắt headless để gỡ lỗi
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Khởi tạo WebDriver
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Lỗi khi khởi tạo WebDriver: {str(e)}")
        return

    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/account.json"
    output_file = "data/facebook_posts.json"
    data_filename = "data/data.json"

    # Đọc dữ liệu tài khoản từ data.json
    try:
        with open(data_filename, 'r') as data_file:
            data = json.load(data_file)
    except Exception as e:
        print(f"Lỗi khi đọc file {data_filename}: {str(e)}")
        driver.quit()
        return

    driver.maximize_window()

    try:
        # Đăng nhập vào Facebook
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account.get("email")
        password_facebook = facebook_account.get("password")

        if not email_facebook or not password_facebook:
            print("Thiếu thông tin đăng nhập Facebook trong file data.json")
            return

        try:
            driver.get(config.FACEBOOK_URL)
            base_page.login_facebook(email_facebook, password_facebook)
            print("Đăng nhập thành công vào Facebook.")
            time.sleep(5)  # Đợi đăng nhập hoàn tất
        except Exception as e:
            print(f"Lỗi khi đăng nhập Facebook: {str(e)}")
            return

        # Vòng lặp vô tận
        while True:
            # Đọc dữ liệu tài khoản từ account.json
            try:
                with open(accounts_filename, 'r') as file:
                    accounts_data = json.load(file)
            except Exception as e:
                print(f"Lỗi khi đọc file {accounts_filename}: {str(e)}")
                continue

            print(f"\n===== Bắt đầu chu kỳ crawl mới với {len(accounts_data)} tài khoản =====")

            # Lặp qua các tài khoản theo thứ tự từ trên xuống dưới
            for account_key, account_data in accounts_data.items():
                try:
                    print(f"\n[ACCOUNT] Đang xử lý: {account_key} - {account_data.get('url2')}")

                    group_url = account_data.get("url2", "")
                    emso_username = account_data.get("username")
                    emso_password = account_data.get("password")
                    post_url = account_data.get("url1")

                    if not group_url or not emso_username or not emso_password or not post_url:
                        print(f"[SKIP] Bỏ qua account {account_key} vì thiếu dữ liệu.")
                        continue

                    # Kiểm tra trạng thái cửa sổ trình duyệt
                    try:
                        driver.title  # Kiểm tra xem cửa sổ trình duyệt còn tồn tại không
                    except NoSuchWindowException:
                        print("Cửa sổ trình duyệt đã bị đóng. Khởi tạo lại WebDriver.")
                        driver.quit()
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        driver.maximize_window()
                        base_page = BasePage(driver)
                        # Đăng nhập lại Facebook
                        driver.get(config.FACEBOOK_URL)
                        base_page.login_facebook(email_facebook, password_facebook)
                        print("Đăng nhập lại thành công vào Facebook.")
                        time.sleep(5)

                    # Đăng nhập vào emso.vn trước khi truy cập url2
                    try:
                        base_page.login_emso(emso_username, emso_password)
                        print(f"Đăng nhập thành công vào emso.vn cho {account_key}")
                    except Exception as e:
                        print(f"[ERROR] Lỗi đăng nhập emso.vn cho {account_key}: {str(e)}")
                        continue

                    # Kiểm tra chuyển hướng sau khi truy cập url2
                    try:
                        driver.get(group_url)
                        time.sleep(5)  # Chờ trang tải
                        current_url = driver.current_url
                        if current_url != group_url:
                            print(f"[WARNING] Trang {group_url} chuyển hướng đến {current_url}")
                            if "login" in current_url.lower():
                                print("[ERROR] Chuyển hướng đến trang đăng nhập. Đăng nhập lại emso.vn.")
                                base_page.login_emso(emso_username, emso_password)
                                driver.get(group_url)  # Thử lại url2
                                time.sleep(5)
                    except Exception as e:
                        print(f"[ERROR] Lỗi khi truy cập {group_url}: {str(e)}")
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
                        print(f"⏳ Nghỉ 60 giây trước khi xử lý account tiếp theo.")
                        time.sleep(60)  # Giảm thời gian chờ để tránh timeout
                    else:
                        print(f"[FAIL] Không crawl được bài đăng cho {account_key}, chuyển tiếp account khác.")

                    # Nghỉ ngẫu nhiên ngắn giữa các tài khoản
                    time.sleep(random.uniform(5, 15))

                except Exception as e:
                    import traceback
                    print(f"[ERROR] Lỗi khi xử lý tài khoản {account_key}: {str(e)}")
                    traceback.print_exc()
                    continue

            print("===== Đã hoàn tất xử lý tất cả account. Bắt đầu vòng lặp mới =====")
            time.sleep(random.uniform(5, 10))  # Nghỉ trước khi bắt đầu vòng lặp mới

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong quá trình chạy: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()