from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from functions import read_credentials, get_title_link_info, scroll_pdf_viewer
import os

# Path to your credentials file
credentials_file = 'credentials.json'

# Read MSSV and password
mssv, password = read_credentials(credentials_file)

# Setup the Chrome WebDriver
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)

# Login to the portal
driver.get("https://stdportal.tdtu.edu.vn/Login/Index?ReturnUrl=https%3A%2F%2Fstdportal.tdtu.edu.vn%2F")
sleep(1)

# Input credentials
mssv_input = driver.find_element(By.ID, 'txtUser')
password_input = driver.find_element(By.ID, 'txtPass')
mssv_input.send_keys(mssv)
password_input.send_keys(password)
sleep(2)

# Click the login button
driver.find_element(By.ID, 'btnLogIn').click()
sleep(6)

# Navigate to regulations page
link_element = driver.find_element(By.XPATH, "/html/body/div[1]/main/section[2]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/a[@href='https://quychehocvu.tdtu.edu.vn']")
link_href = link_element.get_attribute('href')
driver.get(link_href)
sleep(8)

# Page 1
page1_titles, page1_link, page1_phong = [], [], []
page1_titles, page1_link, page1_phong = get_title_link_info(driver, page1_titles, page1_link, page1_phong)

# Page 2
page2 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[2]/div/div[2]/nav/ul[3]/li[1]/a')
page2.click()
sleep(2)
page2_titles, page2_link, page2_phong = [], [], []
page2_titles, page2_link, page2_phong = get_title_link_info(driver, page2_titles, page2_link, page2_phong)

# Page 3
page3 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[2]/div/div[2]/nav/ul[3]/li[2]/a')
page3.click()
sleep(2)
page3_titles, page3_link, page3_phong = [], [], []
page3_titles, page3_link, page3_phong = get_title_link_info(driver, page3_titles, page3_link, page3_phong)

# Combine all titles and links
all_titles = page1_titles + page2_titles + page3_titles
all_links = page1_link + page2_link + page3_link

# Create data folder
os.makedirs("data_new", exist_ok=True)
error = 1
# Loop through all links
for link, title in zip(all_links, all_titles):
    print(f"Processing: {title}")
    driver.get(link)
    sleep(5)

    # Path to save the text content
    file_path = os.path.join("data_new", f"{title}.txt")

    try:
        # Locate PDF viewer container
        pdf_viewer_container = driver.find_element(By.ID, 'pdfviewer_viewerContainer')

        # Locate the total page count
        total_pages_element = driver.find_element(By.ID, 'pdfviewer_totalPage')
        total_pages_text = total_pages_element.text
        total_pages = int(total_pages_text.split()[-1])  # Extract page count
        print(f"Total pages in {title}: {total_pages}")
        
        # Initialize counter for consecutive empty pages
        empty_page_count = 0  # Đếm số lần liên tiếp gặp trang rỗng
        # Open file to save extracted text
        waitTime, sleepTime, checkFile = 0, 0, 0
       
        if total_pages < 10:
            waitTime =  30
            sleepTime = 8
        elif total_pages < 20:
            waitTime = 40
            sleepTime = 10
        else: 
            waitTime = total_pages * 3
            sleepTime = total_pages * 2
            
            
        with open(file_path, "w", encoding="utf-8") as file:
            for i in range(total_pages):
                # Scroll PDF viewer
                
                if i == 0:
                    wait = WebDriverWait(driver, waitTime)
                    
                    sleep(sleepTime)
                    scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
                    
                else: 
                    scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
                    sleep(sleepTime)
                    wait = WebDriverWait(driver, total_pages)
                
                    
                
                # scroll_pdf_viewer(driver, pdf_viewer_container, 700)
                # sleep(3)

                # Wait for text layer
                # wait = WebDriverWait(driver, 30)
                text_layer = wait.until(EC.presence_of_element_located((By.ID, f'pdfviewer_textLayer_{i}')))

                # Extract text elements
                text_elements = text_layer.find_elements(By.CLASS_NAME, 'e-pv-text')
                page_text = [element.text for element in text_elements if element.text.strip()]

                if not page_text:  # Nếu không có nội dung trên trang
                    empty_page_count += 1
                    print(f"No text found on Page {i + 1} of {title}. Consecutive empty pages: {empty_page_count}")

                    # Break if 3 consecutive empty pages
                    if empty_page_count >= 3:
                        print(f"Stopping due to 3 consecutive empty pages in {title}.")
                        break
                
                    

                # Write page text to file
                file.write(f"Page {i + 1}:\n")
                file.write("\n".join(page_text))
                file.write("\n\n")

                print(f"Extracted text for Page {i + 1} of {title}")

    except Exception as e:
        error_message = f"{error}----------------\n An error occurred with link '{link}' and title '{title}': {e}\n"
        print(error_message)
        error += 1
        with open("error.txt", "a", encoding="utf-8") as error_file:
            error_file.write(error_message)
    
    empty_page_count = 0  # Reset counter nếu trang có dữ liệu

# Close the driver
driver.quit()
 