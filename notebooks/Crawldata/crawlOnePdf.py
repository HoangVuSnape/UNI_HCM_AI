from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from functions import read_credentials, get_title_link_info, write_to_file, scroll_pdf_viewer

# Setup the Chrome WebDriver
options = webdriver.ChromeOptions()
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

# Fetch page content (Page1 titles, links, and additional info)
page1_titles, page1_link, page1_phong = [], [], []
page1_titles, page1_link, page1_phong = get_title_link_info(driver, page1_titles, page1_link, page1_phong)

# Write page1 info to a file
# write_to_file(page1_titles, page1_link, page1_phong, filename="page1.txt")

# Navigate to a specific PDF page link
driver.get(page1_link[2])
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

# Scroll through the PDF viewer for the total number of pages
for _ in range(total_pages):
    scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
    sleep(3)  # Pause to allow content to load

# Close the browser once done
driver.quit()
