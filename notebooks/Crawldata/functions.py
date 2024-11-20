from selenium.webdriver.common.by import By
import json

def read_credentials(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Load JSON data
        mssv = data['mssv']     # Retrieve MSSV
        password = data['password']  # Retrieve password
    return mssv, password

def get_title_link_info(driver, page_titles, page_link, page_phong):
    
    # Tìm tất cả các phần tử có class 'list-item box'
    list_items = driver.find_elements(By.CLASS_NAME, 'list-item')

    # Lặp qua từng phần tử và in ra tiêu đề, link, và thông tin bổ sung
    for item in list_items:
        # Tìm thẻ <a> bên trong mỗi phần tử để lấy tiêu đề và link
        link_element = item.find_element(By.TAG_NAME, 'a')
        title = link_element.text
        link = link_element.get_attribute('href')  # Lấy link
        
        # Tìm thẻ <span> để lấy thông tin bổ sung (ngày, phòng ban)
        additional_info = item.find_element(By.TAG_NAME, 'span').text

        page_titles.append(title)
        page_link.append(link)
        page_phong.append(additional_info)

    return page_titles, page_link, page_phong

# Hàm ghi các danh sách vào file page1.txt với đánh số thứ tự
def write_to_file(page_titles, page_link, page_phong, filename="page1.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for idx, (title, link, phong) in enumerate(zip(page_titles, page_link, page_phong), 1):
            f.write(f"{idx} " + '-' * 50 + '\n')  # Thêm số thứ tự trước dấu gạch ngang
            f.write(f"Tiêu đề: {title}\n")
            f.write(f"Link: {link}\n")
            f.write(f"Thông tin bổ sung: {phong}\n")
            
            
## Using in crawlOnePdf.py
def scroll_pdf_viewer(driver, container, scroll_height):
    driver.execute_script("arguments[0].scrollTop += arguments[1];", container, scroll_height)
    