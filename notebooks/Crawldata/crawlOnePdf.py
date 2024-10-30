from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
driver.get(page1_link[1])
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

# Open a file to save the text content
with open("pdf_text_output.txt", "w", encoding="utf-8") as file:
    # Scroll through the PDF viewer for the total number of pages
    for i in range(total_pages):
        scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
        # Wait for the text layer to load
        wait = WebDriverWait(driver, 10)
        text_layer = wait.until(EC.presence_of_element_located((By.ID, f'pdfviewer_textLayer_{i}')))

        # Wait for text elements within the text layer to load
        text_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'e-pv-text')))

        # Extract text from each element and store in list_pdf_0
        list_pdf_0 = [element.text for element in text_elements if element.text.strip()]

        # Write each page's text to the file
        file.write(f"Page {i + 1}:\n")
        file.write("\n".join(list_pdf_0))
        file.write("\n\n")  # Separate pages with newline for readability

        # Print the extracted texts for confirmation
        print(f"Extracted text for Page {i + 1}:", list_pdf_0)
        sleep(3)  # Pause to allow content to load

# # Close the browser once done
driver.quit()
