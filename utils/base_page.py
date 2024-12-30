from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import os
import logging
from PIL import Image
from io import BytesIO
import csv
import pandas as pd
import base64
import requests
from utils.config import Config
import json
import time
import yt_dlp
from send2trash import send2trash
import random


logging.basicConfig(
    filename='error.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = Config()
        self.media_dir = os.path.join(os.getcwd(), "media")
        os.makedirs(self.media_dir, exist_ok=True)
        self.output_file = "post.json"
    
    INPUT_USERNAME = "//input[@id='email']"
    INPUT_PASSWORD = "//input[@id='pass']"    
    LOGIN_BUTTON = "//button[text()='Log in']"
    CONTAIN_MEDIA = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[2]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[2]"
    TITLE_POST = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[2]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]/div[1]/div/div"
    MEDIA_DIR = "media"  # Thư mục lưu ảnh
    LOGIN_EMAIL_INPUT = "//input[@id='email' and @type='text']"
    LOGIN_PWD_INPUT = "//input[@id='password' and @type='password']"
    LOGIN_SUBMIT_BTN = "//button[@id='demo-customized-button' and ./div[text()='Đăng nhập']]"
    PROFILE_ACCOUNT_ICON = "//div[@id='root']/div/div/div/div/header/div/div/div[3]/div/div[2]/div[2]/i"
    INPUT_POST = "//textarea[@name='textInputCreatePost']"
    INPUT_MEDIA = "//input[@type='file' and @accept='image/jpeg,image/png,/.glb,video/mp4,video/avi,video/quicktime,video/Ogg,video/wmv,video/mov' and @multiple and @autocomplete='off']"
    CREATE_POST_BUTTON = "//button[@id='demo-customized-button']//div[text()='Đăng']"
    OPEN_FORM = "//p[text()='Ảnh/Video']"
    LOGOUT_BTN = "//header//div[@role= 'button' and ./div/p[text()='Đăng xuất']]"
    MEDIA_TAB = "//div[@class='html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x18d9i69 x6s0dn4 x9f619 x78zum5 x2lah0s x1hshjfz x1n2onr6 xng8ra x1pi30zi x1swvt13']/span[text()='Ảnh']"
    VIEW_DETAIL = "//a[text()='Xem bài viết']"
    CLOSE_DETAIL = "/html/body/div[1]/div/div/div[1]/div/div[2]/div[1]/a"
    MEDIA_IN_DETAIL = "/html/body/div[1]/div/div/div[1]/div/div[6]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]"
    TITLE_POST = "(//div[contains(@data-ad-comet-preview, 'message')])[{index}]"
    POST = "//div[@aria-posinset='{index}']"
    MORE_OPTION = "(//div[@aria-haspopup='menu' and contains(@class, 'x1i10hfl') and contains(@aria-label, 'Hành động với bài viết này')])[{index}]"
    SKIP_BANNER = "//div[contains(text(), 'Tiếp tục')]"
    ITEMS_VIDEO_WATCH = "(//div[@class='x1qjc9v5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x78zum5 xdt5ytf x1l90r2v xyamay9 xjl7jj']//div[.//span[text()='Video']])[1]/div/div/div/div/div/div/div/div/div/div/a"
    ITEM_VIDEO_WATCH = "(//div[@class='x1qjc9v5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x78zum5 xdt5ytf x1l90r2v xyamay9 xjl7jj']//div[.//span[text()='Video']])[1]/div/div/div/div[{index}]/div/div/div/div/div/div/a"
    TITLE_VIDEO_WATCH = "(//div[@class='x1qjc9v5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x78zum5 xdt5ytf x1l90r2v xyamay9 xjl7jj']//div[.//span[text()='Video']])[1]/div/div/div/div[{index}]/div/div/div/div/div/div[2]/span/div/a"
    NEXT_REELS = "//div[@aria-label='Thẻ tiếp theo' and contains(@class, 'x1i10hfl')]"
    OPEN_FORM_MOMENT = "//button[contains(@class, 'MuiButton-root') and .//p[text()='Khoảnh khắc']]"
    INPUT_UPLOAD_MOMENT = "//input[@id='files' and @name='files']"
    BUTTON_CREATE_MOMENT = "//button[@class='MuiLoadingButton-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-disableElevation MuiButtonBase-root css-n5x2z']"
    INPUT_TITLE_MOMENT = "//textarea[@id='textInputCreateMoment']"
    TITLE_REELS = "//div[@class='xyamay9 x1pi30zi x1swvt13 xjkvuk6']"
    CLOSE_BAN_ACCOUNT = "//button[@type='button' and .//i[contains(@class, 'fa-xmark')]]"
    OPEN_FORM_CREATE_MUSIC_BUTTON = "//div[@role='button' and contains(@class, 'MuiListItem-button')]//p[contains(text(), 'Tạo mới Album/Bài hát')]"
    TITLE_MUSIC = "//textarea[@id='title']"
    DES_MUSIC = "//textarea[@id='description_song']"
    INPUT_UPLOAD_BANNER_MUSIC = "//input[@name='banner']"
    INPUT_UPLOAD_MP3 = "//input[@name='file_mp3']"
    INPUT_CATEGORY_MUSIC = "//input[@name='category_music_id']"
    INPUT_PAGE_OWNER = "//input[@name='page_owner_id']"
    INPUT_AUTHOR = "//input[@name='music_host_added']"
    INPUT_FIELD = "//input[@type='file' and @accept='.doc, .docx, .pdf, .pptx, .ppt']"
    INPUT_FIELD2 = "//textarea[ @name='field']"
    SEND_REQUEST_MUSIC = "//button[.//div[text()='Gửi phê duyệt']]"
    OPTION_CATEGORY = "//div[@id='mui-52-option-{index}']/div/div/p"
    PAGE_OWNER_MUSIC = "//p[contains(.,'{page_name}')]"
    AUTHOR_MUSIC = "//div[@id='mui-56-option-0']" #Tài khoản phải có bạn bè
    
    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(locator_type, locator_value)
    
    def login_facebook(self, username, password):
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON) 
        time.sleep(5)
    
    def login_emso(self, username, password):
        self.driver.get(self.config.EMSO_URL)
        time.sleep(1)
        self.input_text(self.LOGIN_EMAIL_INPUT, username)
        self.input_text(self.LOGIN_PWD_INPUT, password)
        self.click_element(self.LOGIN_SUBMIT_BTN)
        self.wait_for_element_clickable(self.PROFILE_ACCOUNT_ICON)
        
    def logout(self):
        self.click_element(self.PROFILE_ACCOUNT_ICON)
        self.click_element(self.LOGOUT_BTN)
        
    def is_element_present_by_xpath(self, xpath: str) -> bool:
        try:
            # Tìm phần tử bằng XPath
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            # Nếu không tìm thấy phần tử, trả về False
            return False
    
    def click_element(self, xpath: str, timeout=15):
        try:
            element = self.wait_for_element_clickable(xpath, timeout)
            # Cuộn đến phần tử nếu cần
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            # print(f"Clicked on element with XPath: {xpath}")
        except Exception as e:
            print(f"Error while clicking element with XPath '{xpath}': {e}")
            raise
        
    def wait_for_element_clickable(self, xpath: str, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            print(f"Element with XPath '{xpath}' not clickable after {timeout} seconds.")
            raise
 
    def input_text(self, xpath: str, text: str):
        try:
            # Chờ phần tử khả dụng
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            # Tìm phần tử và cuộn tới nó
            element = self.driver.find_element(By.XPATH, xpath)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # Đảm bảo phần tử hiện hữu và không bị thay đổi trạng thái
            for _ in range(3):  # Thử tối đa 3 lần nếu có lỗi StaleElementReferenceException
                try:
                    # Chờ phần tử khả dụng lại nếu cần
                    WebDriverWait(self.driver, 3).until(EC.visibility_of(element))
                    
                    # Xóa văn bản hiện tại
                    element.click()
                    element.send_keys(Keys.CONTROL + "a")  # Chọn tất cả văn bản
                    element.send_keys(Keys.DELETE)  # Xóa văn bản cũ
                    
                    # Nhập văn bản mới
                    element.send_keys(text)
                    return  # Thành công, thoát khỏi hàm
                except StaleElementReferenceException:
                    # Reload phần tử nếu DOM thay đổi
                    element = self.driver.find_element(By.XPATH, xpath)
            raise Exception("Không thể tương tác với phần tử sau nhiều lần thử.")
        except TimeoutException:
            print("Phần tử không sẵn sàng hoặc không khả dụng trong thời gian chờ.")
        except Exception as e:
            print(f"Không thể nhập văn bản vào phần tử: {e}")
    
    def get_text_from_element(self, locator):
        text = self.driver.find_element(By.XPATH, locator).text
        return text
    
    def get_data_from_json_file(self, file_name):
        data_file = f'{file_name}.json'
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f, strict = False)
        return data
        
    @staticmethod
    def extract_username_from_url(url):
        """
        Trích xuất username từ URL của Facebook.
        """
        match = re.search(r"https://www\.facebook\.com/([^/]+)", url)
        if match:
            return match.group(1)
        return None

    def save_to_json(self, group_url, posts, output_file):
        try:
            # Trích xuất username từ group_url
            username = self.extract_username_from_url(group_url)

            # Nếu không trích xuất được username, dừng lại
            if not username:
                print("Invalid Facebook URL, cannot extract username.")
                return

            # Nếu file chưa tồn tại, tạo mới một dictionary rỗng
            if not os.path.exists(output_file):
                data = {}
            else:
                # Nếu file đã tồn tại, đọc dữ liệu từ file
                with open(output_file, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from {output_file}. The file might be corrupted.")
                        return  # Nếu file bị lỗi, dừng lại

            # Lấy các bài viết đã tồn tại từ group trong file
            existing_group_posts = data.get(username, [])

            # Lọc các bài viết mới, bỏ qua những bài đã tồn tại trong file
            existing_titles = {post["title"] for post in existing_group_posts}
            new_posts = [post for post in posts if post["title"] not in existing_titles]

            # Thêm bài viết mới vào danh sách cũ
            if username not in data:
                data[username] = []

            data[username].extend(new_posts)

            # Lưu dữ liệu vào file JSON
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Data saved successfully to {output_file}.")

        except Exception as e:
            print(f"Error saving to JSON: {e}")

            
    def read_existing_posts(self, output_file):
        try:
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    existing_posts = {}
                    for group, posts in data.items():
                        for post in posts:
                            existing_posts[post["title"]] = True
                    return existing_posts
        except Exception as e:
            print(f"Error reading existing posts: {e}")
        return {}

    def upload_image(self, file_input_locator, image_name):
        try:
            # Kiểm tra nếu image_name là một danh sách, nếu có, lấy phần tử đầu tiên
            if isinstance(image_name, list):
                image_name = image_name[0]  # Lấy ảnh đầu tiên trong danh sách

            # Đảm bảo đường dẫn tuyệt đối tới thư mục 'media' và ảnh
            media_dir = os.path.join(os.getcwd(), 'media')  # Lấy đường dẫn tuyệt đối thư mục 'media'
            image_path = os.path.join(media_dir, image_name)  # Đảm bảo đường dẫn chính xác

            # In ra đường dẫn ảnh để kiểm tra
            print(f"Đường dẫn ảnh: {image_path}")

            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(image_path):
                print(f"File không tồn tại: {image_path}")
                return

            # Tìm phần tử input và gửi đường dẫn ảnh
            file_input = self.wait_for_element_present(file_input_locator)
            file_input.send_keys(image_path)

            print(f"Đã upload ảnh: {image_path}")

        except Exception as e:
            print(f"Error uploading image: {e}")
    
    def upload_mp3(self, file_input_locator, image_name):
        try:
            # Kiểm tra nếu image_name là một danh sách, nếu có, lấy phần tử đầu tiên
            if isinstance(image_name, list):
                image_name = image_name[0]  # Lấy ảnh đầu tiên trong danh sách

            # Đảm bảo đường dẫn tuyệt đối tới thư mục 'media' và ảnh
            media_dir = os.path.join(os.getcwd(), 'music')  # Lấy đường dẫn tuyệt đối thư mục 'media'
            image_path = os.path.join(media_dir, image_name)  # Đảm bảo đường dẫn chính xác

            # In ra đường dẫn ảnh để kiểm tra
            print(f"Đường dẫn ảnh: {image_path}")

            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(image_path):
                print(f"File không tồn tại: {image_path}")
                return

            # Tìm phần tử input và gửi đường dẫn ảnh
            file_input = self.wait_for_element_present(file_input_locator)
            file_input.send_keys(image_path)

            print(f"Đã upload ảnh: {image_path}")

        except Exception as e:
            print(f"Error uploading image: {e}")
        
    def wait_for_element_present(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return self.find_element_by_locator(locator)

    def find_element_by_locator(self, locator, context=None):
        if context:
            element = context.find_element(By.XPATH, locator)
        else:
            element = self.driver.find_element(By.XPATH, locator)
        return element

    def read_accounts_from_json(self, filename):
        with open(filename, 'r') as file:
            accounts_data = json.load(file)
        return accounts_data

    # Đọc các bài viết từ file facebook_posts.json
    def read_posts_from_json(self, filename, pagename):
        with open(filename, 'r') as file:
            posts_data = json.load(file)
        return posts_data.get(pagename, [])

    # Đăng bài lên Facebook (giả định)
    def create_post(self, title, image_names):
        try:
            # Mở form tạo bài đăng
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM)))  # Ensure post loads
            self.click_element(self.OPEN_FORM)

            # Nhập tiêu đề bài đăng
            self.input_text(self.INPUT_POST, title)

            # Tải lên các ảnh (nếu có)
            if image_names:
                for image_name in image_names:
                    self.upload_image(self.INPUT_MEDIA, image_name)  # Giả sử upload_image hỗ trợ tải ảnh

            # Nhấn nút đăng bài
            self.click_element(self.CREATE_POST_BUTTON)
            self.wait_for_element_not_present(self.CREATE_POST_BUTTON)

        except Exception as e:
            print(f"Error creating post: {e}")
    
    def create_moment(self, title, image_names):
        try:
            # Mở form tạo bài đăng
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM_MOMENT)))  # Ensure post loads
            self.click_element(self.OPEN_FORM_MOMENT)

            # Nhập tiêu đề bài đăng
            self.wait_for_element_present(self.INPUT_TITLE_MOMENT)
            self.input_text(self.INPUT_TITLE_MOMENT, title)

            # Tải lên các ảnh (nếu có)
            if image_names:
                for image_name in image_names:
                    self.upload_image(self.INPUT_UPLOAD_MOMENT, image_name)  # Giả sử upload_image hỗ trợ tải ảnh

            # Nhấn nút đăng bài
            self.click_element(self.BUTTON_CREATE_MOMENT)
            self.wait_for_element_not_present(self.BUTTON_CREATE_MOMENT)

        except Exception as e:
            print(f"Error creating post: {e}")
    
    def clear_media_folder(self):
        try:
            # Lấy đường dẫn thư mục gốc của dự án (C:\Users\Thinh\OneDrive\Máy tính\crawl_post_v2)
            current_dir = os.path.dirname(os.path.abspath(__file__))  # Lấy đường dẫn của file hiện tại (utils)
            project_root = os.path.abspath(os.path.join(current_dir, '..'))  # Lùi hai cấp để tới thư mục gốc

            media_folder_path = os.path.join(project_root, "media")  # Xây dựng đường dẫn đến thư mục media

            # Kiểm tra nếu thư mục tồn tại
            if not os.path.exists(media_folder_path):
                print(f"Thư mục {media_folder_path} không tồn tại.")
                return

            # Xóa tất cả tệp trong thư mục media và đưa chúng vào thùng rác
            for file_name in os.listdir(media_folder_path):
                file_path = os.path.join(media_folder_path, file_name)
                if os.path.isfile(file_path):
                    send2trash(file_path)  # Di chuyển tệp vào thùng rác
                    print(f"Đã di chuyển tệp {file_name} vào thùng rác.")

            print(f"Đã xóa tất cả các tệp trong thư mục: {media_folder_path} và đưa vào thùng rác.")
            
        except Exception as e:
            print(f"Lỗi khi xóa các tệp trong thư mục media: {e}")
    
    def wait_for_element_not_present(self, locator, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            logging.info(f"Element located by {locator} is not present in the DOM.")
        except TimeoutException:
            raise AssertionError(f"Element located by {locator} is still present in the DOM after {timeout} seconds.")
        except NoSuchElementException:
            logging.warning(f"Element located by {locator} was not found in the DOM initially.")

    # ====================================================================================================
    def scroll_to_element_and_crawl(self, username, password, nums_post, crawl_page, post_page, index_start=1):
        self.driver.get(crawl_page)
        post_data = []  # Danh sách để lưu dữ liệu của các bài post hợp lệ
        current_post_index = index_start  # Bắt đầu từ index_start
        skip_count = 0  # Biến đếm số bài bỏ qua

        # Đọc dữ liệu cũ nếu có từ tệp JSON
        output_file = "data/post.json"
        existing_data = {}
        if os.path.exists(output_file):
            try:
                with open(output_file, "r", encoding="utf-8") as json_file:
                    existing_data = json.load(json_file)
            except Exception as json_err:
                print(f"Lỗi khi đọc dữ liệu từ tệp JSON cũ: {json_err}")

        if self.is_element_present_by_xpath(self.POST.replace("{index}", '1')) == False:
            raise Exception(f"Page lỗi không lấy được post")

        while len(post_data) < nums_post:  # Tiếp tục đến khi đủ nums_post hợp lệ
            try:
                # Tạo XPath động cho phần tử chính (post)
                post_xpath = self.POST.replace("{index}", str(current_post_index))

                # Đợi cho đến khi phần tử được tải xong
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, post_xpath)))

                # Tìm phần tử chính bằng XPath
                post_element = self.driver.find_element(By.XPATH, post_xpath)

                # Nếu không tìm thấy phần tử đầu tiên, dừng vòng lặp và trả lỗi
                

                # Cuộn đến vị trí của phần tử chính
                self.driver.execute_script("arguments[0].scrollIntoView();", post_element)

                # Chờ để đảm bảo phần tử đã tải đầy đủ
                time.sleep(2)

                # Tìm các phần tử con trong element post tại vị trí index (title có thể là message đầu tiên)
                message_elements = post_element.find_elements(By.XPATH, ".//div[contains(@data-ad-comet-preview, 'message')]")

                # Kiểm tra nếu bài đăng có message (được coi là title)
                if not message_elements or not message_elements[0].text.strip():
                    print(f"Post {current_post_index} không có title hợp lệ, bỏ qua.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:  # Kiểm tra nếu đã bỏ qua quá 20 bài
                        print(f"Đã bỏ qua quá 20 bài, dừng quá trình tại page - {crawl_page}.")
                        break  # Dừng quá trình nếu bỏ qua quá nhiều bài
                    continue  # Bỏ qua bài đăng này và tiếp tục với bài đăng tiếp theo

                # Lấy text từ tất cả các phần tử message
                messages = [message.text for message in message_elements]

                # Kiểm tra nếu messages đã tồn tại trong dữ liệu cũ
                if any(post.get("messages") == messages for post in existing_data.get(crawl_page, [])):
                    print(f"Post {current_post_index} với messages đã tồn tại, bỏ qua.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:  # Kiểm tra nếu đã bỏ qua quá 20 bài
                        print("Đã bỏ qua quá 20 bài, dừng quá trình.")
                        break  # Dừng quá trình nếu bỏ qua quá nhiều bài
                    continue  # Bỏ qua bài đăng này nếu messages đã tồn tại

                # Tìm các phần tử ảnh trong post
                image_elements = post_element.find_elements(By.XPATH, ".//img")
                image_urls = []

                for img in image_elements:
                    # Kiểm tra kích thước ảnh bằng naturalWidth
                    img_width = self.driver.execute_script("return arguments[0].naturalWidth;", img)
                    if img_width >= 100:
                        img_url = img.get_attribute("src")
                        if img_url:
                            image_urls.append(img_url)

                # Kiểm tra nếu không có ảnh hợp lệ
                if len(image_urls) == 0:
                    print(f"Post {current_post_index} không có ảnh hợp lệ (> 100px), bỏ qua.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:  # Kiểm tra nếu đã bỏ qua quá 20 bài
                        print(f"Đã bỏ qua quá 20 bài, dừng quá trình tại page - {crawl_page}.")
                        break  # Dừng quá trình nếu bỏ qua quá nhiều bài
                    continue  # Bỏ qua bài đăng này và tiếp tục với bài đăng tiếp theo

                # Tải xuống và lưu các ảnh vào thư mục "media"
                media_dir = "media"
                os.makedirs(media_dir, exist_ok=True)
                image_paths = []

                for i, img_url in enumerate(image_urls):
                    try:
                        response = requests.get(img_url, stream=True)
                        if response.status_code == 200:
                            # Lưu chỉ tên ảnh mà không phải đường dẫn đầy đủ
                            image_name = f"page_{current_post_index}_img_{i}.jpg"
                            image_path = os.path.join(media_dir, image_name)
                            with open(image_path, "wb") as img_file:
                                img_file.write(response.content)
                            image_paths.append(image_name)  # Lưu tên ảnh thay vì đường dẫn đầy đủ
                        else:
                            break  # Ngừng tải ảnh nếu có lỗi
                    except Exception:
                        print(f"Lỗi khi tải ảnh")
                        break  # Ngừng tải ảnh nếu có lỗi

                # Kiểm tra nếu không có ảnh hợp lệ (trong trường hợp image_paths vẫn rỗng)
                if len(image_paths) == 0:
                    print(f"Post {current_post_index} không có ảnh hợp lệ, bỏ qua.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:  # Kiểm tra nếu đã bỏ qua quá 20 bài
                        print(f"Đã bỏ qua quá 20 bài, dừng quá trình tại page - {crawl_page}.")
                        break  # Dừng quá trình nếu bỏ qua quá nhiều bài
                    continue  # Bỏ qua bài đăng này và tiếp tục với bài đăng tiếp theo

                # Lưu dữ liệu bài viết hợp lệ vào danh sách
                post_data.append({
                    "post_index": current_post_index,
                    "messages": messages,
                    "images": image_paths  # Lưu chỉ tên ảnh
                })

                print(f"Đã xử lý post {current_post_index}. Text: {messages}, Ảnh hợp lệ: {len(image_paths)}")

            except Exception as e:
                print(f"Lỗi khi xử lý phần tử tại index {current_post_index}: {e}")

            # Tăng index để tiếp tục cuộn và kiểm tra bài đăng tiếp theo
            current_post_index += 1

            # Kiểm tra nếu đã đủ số lượng bài hợp lệ
            if len(post_data) >= nums_post:
                print(f"Đã thu thập đủ {nums_post} bài đăng hợp lệ.")
                break  # Dừng quá trình crawl khi đã đủ số lượng bài hợp lệ

        # Sau khi crawl xong tất cả các bài, đăng bài lần lượt
        if post_data:
            try:
                # Đăng nhập một lần trước khi bắt đầu đăng bài
                self.login_emso(username, password)
                self.driver.get(post_page)

                # Đảm bảo trang đã được tải xong
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM)))  # Thay INPUT_POST bằng phần tử quan trọng trong form đăng bài

                # Vòng lặp đăng bài
                for post in post_data:
                    try:
                        # Đăng bài với tiêu đề và hình ảnh
                        self.create_post(post["messages"][0], post["images"])
                        print(f"Đã đăng bài thành công cho post {post['post_index']}")
                        self.driver.refresh()  # Làm mới trang để chuẩn bị đăng bài tiếp theo
                    except Exception as post_err:
                        # Nếu có lỗi khi đăng bài, in ra lỗi và tiếp tục với bài tiếp theo
                        print(f"Lỗi khi đăng bài {post['post_index']}: {post_err}")

            except Exception as login_err:
                # Nếu có lỗi trong quá trình đăng nhập, in ra và tiếp tục
                print(f"Lỗi khi đăng nhập hoặc truy cập trang đăng bài: {login_err}")

            finally:
                # Đăng xuất sau khi đăng xong tất cả các bài
                self.logout()
                print("Đã đăng xuất khỏi tài khoản.")

            # Lưu dữ liệu vào tệp JSON khi đã xử lý xong
            if crawl_page in existing_data:
                existing_data[crawl_page].extend(post_data)
            else:
                existing_data[crawl_page] = post_data

            try:
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                print(f"Dữ liệu đã được lưu vào {output_file}")
            except Exception as json_err:
                print(f"Lỗi khi lưu dữ liệu vào tệp JSON: {json_err}")
                
    def download_facebook_video(self, video_url):
        # Lấy thời gian hiện tại để đảm bảo tên file là duy nhất
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = f"media/facebook_video_{timestamp}.mp4"  # Tên file sẽ bao gồm timestamp
        video_name = f"facebook_video_{timestamp}.mp4"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_filename,  # Đặt tên file đầu ra với timestamp
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return [video_name]
    
    def get_and_create_watch(self, username, password, nums_post, crawl_page, post_page, index_start=1):
        self.driver.get(crawl_page)
        page_name = self.extract_username_from_url(crawl_page)
        print(f"page_username = {page_name}")
        self.driver.get(f"https://www.facebook.com/{page_name}/videos")
        
        post_data = []  # List to store valid post data
        current_post_index = index_start  # Start from index_start
        skip_count = 0  # Counter for skipped posts

        output_file = "data/watch.json"
        existing_data = {}

        # Đọc dữ liệu hiện có từ file JSON nếu có
        if os.path.exists(output_file):
            try:
                with open(output_file, "r", encoding="utf-8") as json_file:
                    existing_data = json.load(json_file)
            except Exception as json_err:
                print(f"Error reading existing JSON file: {json_err}")

        if self.is_element_present_by_xpath(self.ITEM_VIDEO_WATCH.replace("{index}", '1')) == False:
            raise Exception(f"Page error: unable to fetch post")

        while len(post_data) < nums_post:
            try:
                post_xpath = self.ITEM_VIDEO_WATCH.replace("{index}", str(current_post_index))

                # Chờ cho phần tử tải xong
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, post_xpath)))

                # Tìm phần tử chính bằng XPath
                post_element = self.driver.find_element(By.XPATH, post_xpath)

                # Cuộn đến phần tử
                self.driver.execute_script("arguments[0].scrollIntoView();", post_element)

                # Chờ để đảm bảo phần tử đã tải hoàn toàn
                time.sleep(2)

                # Tìm <a> chứa đường link video
                video_link_element = post_element.find_element(By.XPATH, post_xpath)  # Find the <a> tag with href

                video_url = video_link_element.get_attribute("href")  # Lấy URL video từ thuộc tính href

                # Tìm các phần tử chứa thông điệp và xử lý chúng
                message_elements = post_element.find_elements(By.XPATH, self.TITLE_VIDEO_WATCH.replace("{index}", str(current_post_index)))

                if not message_elements or not message_elements[0].text.strip():
                    print(f"Post {current_post_index} has no valid title, skipping.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:
                        print(f"Skipped over 20 posts, stopping process for page - {crawl_page}.")
                        break
                    continue

                messages = [message.text for message in message_elements]

                # Kiểm tra nếu bài đăng đã tồn tại trong existing_data
                if crawl_page not in existing_data:
                    existing_data[crawl_page] = []

                # Kiểm tra trùng lặp trong existing_data
                if any(post["messages"] == messages and post["video"] == video_url for post in existing_data[crawl_page]):
                    print(f"Post {current_post_index} with these messages already exists, skipping.")
                    current_post_index += 1
                    skip_count += 1
                    if skip_count >= 20:
                        print("Skipped over 20 posts, stopping process.")
                        break
                    continue

                # Kiểm tra trùng lặp trong post_data
                if any(post['post_index'] == current_post_index and post['messages'] == messages for post in post_data):
                    print(f"Duplicate post {current_post_index} with these messages, skipping.")
                    current_post_index += 1
                    skip_count += 1
                    continue

                # Thư mục chứa media
                media_dir = "media"
                os.makedirs(media_dir, exist_ok=True)

                # Kiểm tra video có dưới 5 phút hay không
                if self.is_video_under_5_minutes(video_url):
                    video_path = self.download_facebook_video(video_url)
                    # Đợi sau khi tải xong video
                    time.sleep(5)
                    # Lưu dữ liệu bài đăng
                    post_data.append({
                        "post_index": current_post_index,
                        "messages": messages,
                        "video": video_path
                    })
                    print(f"Downloaded video under 5 minutes for post {current_post_index}.")
                else:
                    current_post_index += 1
                    skip_count += 1
                    print(f"Skipped video over 5 minutes for post {current_post_index}.")
                    continue

                # Thêm bài đăng vào existing_data nếu chưa có
                existing_data[crawl_page].append({
                    "post_index": current_post_index,
                    "messages": messages,
                    "video": video_path
                })

                print(f"Processed post {current_post_index}. Text: {messages}, Valid video: {len(video_path)}")

            except Exception as e:
                print(f"Error processing element at index {current_post_index}: {e}")

            current_post_index += 1

            if len(post_data) >= nums_post:
                print(f"Collected {nums_post} valid posts.")
                break

        # Lưu dữ liệu vào file JSON sau khi thu thập xong
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {output_file}")
        except Exception as json_err:
            print(f"Error writing to JSON file: {json_err}")

        # Đăng nhập và tạo bài viết trên trang post_page
        if post_data:
            try:
                self.login_emso(username, password)
                self.driver.get(post_page)
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM)))

                for post in post_data:
                    try:
                        self.create_post(post["messages"][0], post["video"])
                        print(f"Đã đăng bài thành công cho post {post['post_index']}")
                    except Exception as post_err:
                        print(f"Lỗi khi đăng bài {post['post_index']}: {post_err}")

            except Exception as login_err:
                print(f"Lỗi khi đăng nhập hoặc truy cập trang đăng bài: {login_err}")

            finally:
                self.logout()
                print("Đã đăng xuất khỏi tài khoản.")

            # Cập nhật và lưu lại dữ liệu vào file JSON
            try:
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                print(f"Dữ liệu đã được lưu vào {output_file}")
            except Exception as json_err:
                print(f"Lỗi khi lưu dữ liệu vào tệp JSON: {json_err}")

    
    # Thêm một hàm kiểm tra thời lượng video
    def is_video_under_5_minutes(self, video_url):
        duration_seconds = self.get_video_duration(video_url)
        if duration_seconds and duration_seconds <= 300:  # 5 phút = 300 giây
            return True
        return False

    # Hàm giả lập kiểm tra thời lượng video (tùy vào cách bạn thực hiện thực tế)
    def get_video_duration(self, video_url):
        try:
            duration_seconds = 180  # Ví dụ: Video 3 phút
            return duration_seconds
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return None
    
    def get_and_create_moment(self, username, password, nums_post):
        self.driver.get("https://www.facebook.com/reel/")
        self.click_element(self.NEXT_REELS)

        post_data = []  # List to store valid post data
        output_file = "data/moment.json"
        current_post_index = 0
        existing_data = {}

        # Read existing data from the JSON file if available
        if os.path.exists(output_file):
            try:
                with open(output_file, "r", encoding="utf-8") as json_file:
                    existing_data = json.load(json_file)
            except Exception as json_err:
                print(f"Error reading existing JSON file: {json_err}")

        while len(post_data) < nums_post:
            try:
                time.sleep(2)
                # Get the current video URL
                video_url = self.driver.current_url

                # Get video duration
                duration_seconds = self.get_video_duration(video_url)
                if duration_seconds is None or duration_seconds > 300:
                    current_post_index += 1
                    print(f"Skipped video over 5 minutes for post {current_post_index}.")
                    self.click_element(self.NEXT_REELS)  # Skip to the next video
                    continue

                # Chờ các phần tử xuất hiện
                message_elements = self.wait_for_element_present(self.TITLE_REELS)

                # Kiểm tra nếu message_elements là danh sách hoặc iterable
                if isinstance(message_elements, list) or hasattr(message_elements, '__iter__'):
                    messages = [re.sub(r'[^\w\s,.\'\"#]', '', message.text) for message in message_elements]
                else:
                    messages = [re.sub(r'[^\w\s,.\'\"#]', '', message_elements.text)]

                # Kiểm tra danh sách tin nhắn có rỗng hoặc chỉ chứa văn bản trống
                if not messages or all(not msg.strip() for msg in messages):
                    self.click_element(self.NEXT_REELS)
                    print("No messages found, clicked Next.")
                    continue

                # Cắt ngắn từng tin nhắn đến 150 ký tự
                shortened_messages = []
                for msg in messages:
                    if len(msg) > 150:
                        msg = msg[:150]
                        if len(msg.split()) > 1:
                            msg = ' '.join(msg.split()[:-1])
                    shortened_messages.append(msg)

                print("Processed messages:", shortened_messages)

                # Directory for storing media
                media_dir = "media"
                os.makedirs(media_dir, exist_ok=True)

                # Tải xuống video vì thời lượng hợp lệ
                try:
                    video_path = self.download_facebook_video(video_url)
                    time.sleep(5)
                    post_data.append({
                        "messages": shortened_messages,
                        "video": video_path
                    })
                    print(f"Downloaded video under 5 minutes for post {current_post_index}.")
                except Exception as download_err:
                    print(f"Error downloading video for post {current_post_index}: {download_err}")
                    self.click_element(self.NEXT_REELS)
                    continue

                # Cập nhật dữ liệu
                if f"moment_{current_post_index}" not in existing_data:
                    existing_data[f"moment_{current_post_index}"] = []

                existing_data[f"moment_{current_post_index}"].append({
                    "post_index": current_post_index,
                    "messages": shortened_messages,
                    "video": video_path
                })

                print(f"Processed post {current_post_index}. Text: {shortened_messages}, Valid video: {len(video_path)}")
                self.click_element(self.NEXT_REELS)

            except Exception as e:
                print(f"Error processing element at index {current_post_index}: {e}")
                self.click_element(self.NEXT_REELS)

            current_post_index += 1

            if len(post_data) >= nums_post:
                print(f"Collected {nums_post} valid posts.")
                break

        # Save the collected data to the JSON file after the loop
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {output_file}")
        except Exception as json_err:
            print(f"Error writing to JSON file: {json_err}")

        # Đăng nhập và tạo bài viết trên trang post_page
        if post_data:
            try:
                self.login_emso(username, password)
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM)))
                
                if self.is_element_present_by_xpath(self.OPEN_FORM) == False:
                    self.driver.refresh()

                for post in post_data:
                    try:
                        self.create_moment(post["messages"][0], post["video"])
                        print(f"Đã đăng bài thành công cho post {post['post_index']}")
                    except Exception as post_err:
                        print(f"Lỗi khi đăng bài {post['post_index']}: {post_err}")

            except Exception as login_err:
                self.click_element(self.CLOSE_BAN_ACCOUNT)
                print(f"Lỗi khi đăng nhập hoặc truy cập trang đăng bài: {login_err}")

            finally:
                self.logout()
                print("Đã đăng xuất khỏi tài khoản.")

            # Cập nhật và lưu lại dữ liệu vào file JSON
            try:
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                print(f"Dữ liệu đã được lưu vào {output_file}")
            except Exception as json_err:
                print(f"Lỗi khi lưu dữ liệu vào tệp JSON: {json_err}")
    
    def upload_file(self, file_input_locator, image_path):
        absolute_image_path = os.path.abspath(image_path)
        file_input = self.wait_for_element_present(file_input_locator)
        file_input.send_keys(absolute_image_path)
        
    def set_input_value_by_xpath(self, xpath, value):
        # Tìm phần tử input theo XPath và thay đổi giá trị
        input_element = self.driver.find_element(By.XPATH, xpath)
        input_element.clear()  # Xóa giá trị hiện tại
        input_element.send_keys(value)  # Chèn giá trị mới vào input
        
    def upload_music(self, music_name, music_des, banner, mp3, page_name, author, field):
        self.click_element(self.OPEN_FORM_CREATE_MUSIC_BUTTON)
        self.input_text(self.TITLE_MUSIC, music_name)
        self.input_text(self.DES_MUSIC, music_des)
        self.upload_image(self.INPUT_UPLOAD_BANNER_MUSIC, banner)
        self.upload_mp3(self.INPUT_UPLOAD_MP3, mp3)
        self.click_element(self.INPUT_CATEGORY_MUSIC)
        time.sleep(1)
        self.click_element(self.OPTION_CATEGORY.replace("{index}", "0"))
        
        self.click_element(self.INPUT_PAGE_OWNER)
        self.click_element(self.PAGE_OWNER_MUSIC.replace("{page_name}", page_name))
        
        self.click_element(self.INPUT_AUTHOR)
        self.click_element(self.AUTHOR_MUSIC)
        self.upload_file(self.INPUT_FIELD, field)
        self.click_element(self.SEND_REQUEST_MUSIC)
    
    def approve_music(self, music_name):
        
        
        print("duyệt bài hát")
        
        
        