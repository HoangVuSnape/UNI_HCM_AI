# crawl.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from functions import read_credentials, get_title_link_info, scroll_pdf_viewer  # Import functions
import os 
# Path to your credentials file
credentials_file = 'credentials.json'

# Read the MSSV and password
mssv, password = read_credentials(credentials_file)

# Set up Chrome options
options = webdriver.ChromeOptions()
options.page_load_strategy = 'normal'

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Open the login page
driver.get("https://stdportal.tdtu.edu.vn/Login/Index?ReturnUrl=https%3A%2F%2Fstdportal.tdtu.edu.vn%2F")
sleep(1)

# Find the input fields for MSSV and Password
mssv_input = driver.find_element(By.ID, 'txtUser')
password_input = driver.find_element(By.ID, 'txtPass')

# Input MSSV and password from the file
mssv_input.send_keys(mssv)
password_input.send_keys(password)
sleep(2)

# Click the login button
driver.find_element(By.ID, 'btnLogIn').click()

sleep(6)

# Find the link to the regulations page
link_element = driver.find_element(By.XPATH, "/html/body/div[1]/main/section[2]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/a[@href='https://quychehocvu.tdtu.edu.vn']")
link_href = link_element.get_attribute('href')

# Navigate to the regulations page
driver.get(link_href)
sleep(8)

# Page 1
page1_titles, page1_link, page1_phong = [], [], []
page1_titles, page1_link, page1_phong = get_title_link_info(driver, page1_titles, page1_link, page1_phong)

# Write Page 1 data to file
# write_to_file(page1_titles, page1_link, page1_phong, filename="page1.txt")

sleep(2)

# # Page 2
page2 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[2]/div/div[2]/nav/ul[3]/li[1]/a')
page2.click()

page2_titles, page2_link, page2_phong = [], [], []
page2_titles, page2_link, page2_phong = get_title_link_info(driver, page2_titles, page2_link, page2_phong)

sleep(2)

# # Page 3
page3_titles, page3_link, page3_phong = [], [], []
page2.click()  # Assuming the same link for page 3
page3_titles, page3_link, page3_phong = get_title_link_info(driver, page3_titles, page3_link, page3_phong)


sleep(2)

# Create base data directory
os.makedirs("data_new", exist_ok=True)

# Page links and titles
# page_links = [page1_link, page2_link, page3_link]
# page_titles = [page1_titles, page2_titles, page3_titles]


# TEST
page1_link = ["https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/125","https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/115"]
page1_titles = ["ĐẶC ĐIỂM NHẬN DIỆN SINH VIÊN TDTU", "BỘ QUY TẮC ỨNG XỬ CỦA NGƯỜI HỌC"]
# Path to error log file

page_links = [page1_link]
page_titles = [page1_titles]
error_log_path = "error.txt"

# Loop through each page
# Loop through each page and its corresponding titles/links
for i, (links, titles) in enumerate(zip(page_links, page_titles), start=1):
    folder_name = f"data_new/page{i}"
    os.makedirs(folder_name, exist_ok=True)
    
    for link, title in zip(links, titles):
        # Navigate to each link
        driver.get(link)
        sleep(5)
        
        # Open a file in the corresponding folder to save content
        file_path = os.path.join(folder_name, f"{title}.txt")
        
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                # Locate PDF viewer and total pages
                pdf_viewer_container = driver.find_element(By.ID, 'pdfviewer_viewerContainer')
                total_pages_element = driver.find_element(By.ID, 'pdfviewer_totalPage')
                total_pages_text = total_pages_element.text
                total_pages = int(total_pages_text.split()[-1])
                
                # Scroll and extract each page's text
                waitTime, sleepTime = 0
                checkFile = 0 
                
                if total_pages < 10:
                    waitTime =  30
                    sleepTime = 5
                elif total_pages < 20:
                    waitTime = 35
                    sleepTime = 10
                else: 
                    waitTime = total_pages * 3
                    sleepTime = total_pages * 1.5
                    
                for k in range(total_pages):
                    # scroll_pdf_viewer(driver, pdf_viewer_container, 700)
                    # wait = WebDriverWait(driver, 10)
                    
                    if k == 0:
                        wait = WebDriverWait(driver, waitTime)
                        
                        sleep(sleepTime)
                        scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
                        
                    else: 
                        scroll_pdf_viewer(driver, pdf_viewer_container, 700)  # Scroll by 700px
                        
                        wait = WebDriverWait(driver, total_pages)
                    
                        sleep(sleepTime)
                        
                    text_layer = wait.until(EC.presence_of_element_located((By.ID, f'pdfviewer_textLayer_{i}')))

                    # Find text elements specifically within the text layer
                    text_elements = text_layer.find_elements(By.CLASS_NAME, 'e-pv-text')
                    list_pdf = [element.text for element in text_elements if element.text.strip()]
                    
                    # if len(list_pdf) == 0:
                    #     checkFile += 1  
                    
                    # if checkFile == 3:
                    #     break
                    
                    # Write to file
                    file.write(f"Page {k + 1}:\n")
                    file.write("\n".join(list_pdf))
                    file.write("\n\n")
                    sleep(3)
        
        except Exception as e:
            error_message = f"An error occurred with link '{link}' and title '{title}': {e}\n"
            print(error_message)
            
            # Write error to error log file
            with open(error_log_path, "a", encoding="utf-8") as error_file:
                error_count = sum(1 for _ in open(error_log_path, "r", encoding="utf-8")) + 1
                error_file.write(f"{error_count}. {error_message}")
    # checkFile = 0          
    

# Close the browser after all pages are crawled
driver.quit()

