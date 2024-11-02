
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from time import sleep
from functions import read_credentials, get_title_link_info, write_to_file, scroll_pdf_viewer

import os
import pyautogui
# Setup the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ phóng to
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)

# Login URL and credentials
driver.get("https://stdportal.tdtu.edu.vn/Login/Index?ReturnUrl=https%3A%2F%2Fstdportal.tdtu.edu.vn%2F")
sleep(1)

# Read login credentials from a file
mssv, password = read_credentials('credentials.json')

# Tìm trường nhập MSSV và mật khẩu, sau đó điền thông tin
mssv_input = driver.find_element(By.ID, 'txtUser')
password_input = driver.find_element(By.ID, 'txtPass')

# Nhập thông tin đăng nhập
mssv_input.send_keys(mssv)
password_input.send_keys(password)
sleep(2)

# Click the login button
driver.find_element(By.ID, 'btnLogIn').click()
sleep(6)

# Navigate to the regulations link
link_element = driver.find_element(By.XPATH, "/html/body/div[1]/main/section[2]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/a[@href='https://quychehocvu.tdtu.edu.vn']")
link_href = link_element.get_attribute('href')

# Nhấp vào liên kết để truy cập trang quy chế
driver.get(link_href)
sleep(5)

# Navigate to a specific PDF page link
link1111 = "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/115"

driver.get(link1111)

sleep(2)

# Locate the PDF viewer container
pdf_viewer_container = driver.find_element(By.ID, 'pdfviewer_viewerContainer')

# Locate the total page count element
total_pages_element = driver.find_element(By.ID, 'pdfviewer_totalPage')

# Extract the number of pages from the text (e.g., "of 39")
total_pages_text = total_pages_element.text  # e.g., "of 39"
total_pages_number = total_pages_text.split()[-1]
total_pages = int(total_pages_number)

print("Total number of pages:", total_pages)
if not os.path.exists("dataScreen"):
    os.mkdir("dataScreen")
    
for i in range(total_pages):
    # Scroll PDF viewer
    scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
    
    # Đợi cho nội dung tải xong
    sleep(3)  
    
    # Chụp màn hình và lưu vào thư mục dataScreen với tên tương ứng từng trang
    screenshot_path = os.path.join("dataScreen", f"screenshot_page_{i + 1}.png")
    pyautogui.screenshot(screenshot_path)
    print(f"Saved screenshot of page {i + 1} as {screenshot_path}")

# # Close the browser once done
driver.quit()
