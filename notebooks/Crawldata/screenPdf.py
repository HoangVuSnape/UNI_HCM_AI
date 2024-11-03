
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from time import sleep
from functions import read_credentials, get_title_link_info, write_to_file, scroll_pdf_viewer
import mss
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


# page_title = [
#     "NỘI QUY PHÒNG THI HÌNH THỨC THI TRỰC TUYẾN (CHÍNH THỨC)",
#     "QUY ĐỊNH CẤP CHỨNG NHẬN CỬ NHÂN ƯU TÚ, KỸ SƯ ƯU TÚ, KIẾN TRÚC SƯ ƯU TÚ, DƯỢC SĨ ƯU TÚ ÁP D …",
#     "QUYẾT ĐỊNH SỐ 1276_SỬA ĐỔI, BỔ SUNG QUYẾT ĐỊNH SỐ 1830 VỀ ĐIỀU KIỆN XÉT CÔNG NHẬN TỐT NGHI …",
#     "QUYẾT ĐỊNH VỀ VIỆC BỔ SUNG DANH MỤC CHỨNG CHỈ TIẾNG ANH QUỐC TẾ XÉT MIỄN HỌC PHẦN VÀ CHUẨN …",
#     "QUY ĐỊNH ĐÀO TẠO TIẾNG ANH CỦA CHƯƠNG TRÌNH CHẤT LƯỢNG CAO KHÓA TUYỂN SINH 2020 TRỞ VỀ SAU",
#     "QUY ĐỊNH VỀ ỨNG DỤNG CÔNG NGHỆ TRONG TỔ CHỨC VÀ QUẢN LÝ CÁC HOẠT ĐỘNG GIÁO DỤC",
#     "NỘI QUY PHÒNG THI - ÁP DỤNG CHO TẤT CẢ SINH VIÊN - THAY THẾ CHO CÁC QUY ĐỊNH TRƯỚC",
#     "QUY ĐỊNH VỀ CÁC HỌC PHẦN CƠ SỞ TIN HỌC THEO CHUẨN MOS- ÁP DỤNG CHO SINH VIÊN KHÓA TUYỂN SI …",
#     "QUY ĐỊNH VỀ HOẠT ĐỘNG TẬP SỰ NGHỀ NGHIỆP - ÁP DỤNG CHO TẤT CẢ SINH VIÊN",
#     "BAN HÀNH QUY ĐỊNH CẤP CHỨNG NHẬN KỸ SƯ/CỬ NHÂN ƯU TÚ - ÁP DỤNG CHO TẤT CẢ SINH VIÊN",
#     "2017 - THÔNG BÁO ĐIỀU CHỈNH THỨC THỨC TỐT NGHIỆP BẬC ĐH THEO CHƯƠNG TRÌNH TOP 100 - ÁP DỤN …"
# ]

# page_link = [
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/104",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/101",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/103",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/102",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/53",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/55",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/19",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/14",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/13",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/9",
#     "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/7"
# ]

# List of titles and links
page_title = [
    "NỘI QUY PHÒNG THI HÌNH THỨC THI TRỰC TUYẾN (CHÍNH THỨC)",
    "QUY ĐỊNH CẤP CHỨNG NHẬN CỬ NHÂN ƯU TÚ, KỸ SƯ ƯU TÚ, KIẾN TRÚC SƯ ƯU TÚ, DƯỢC SĨ ƯU TÚ ÁP D …",
    # Add remaining titles here
]

page_link = [
    "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/104",
    "https://quychehocvu.tdtu.edu.vn/QuyChe/Detail/101",
    # Add remaining links here
]

# Create the main dataScreen folder if it doesn't exist
if not os.path.exists("dataScreen"):
    os.mkdir("dataScreen")

# Loop through each page title and link
for i in range(len(page_title)):
    driver.get(page_link[i])
    sleep(2)

    # Scroll to initial position to view the PDF
    scroll_position = 368
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    sleep(2)  # Wait for the content to load if needed

    # Locate the PDF viewer container and total page element
    pdf_viewer_container = driver.find_element(By.ID, 'pdfviewer_viewerContainer')
    total_pages_element = driver.find_element(By.ID, 'pdfviewer_totalPage')
    total_pages_text = total_pages_element.text
    total_pages = int(total_pages_text.split()[-1])

    print("Total number of pages:", total_pages)
    print(f"{i+1}-----------------")
    # Create a folder for each page title in dataScreen
    folder_name = os.path.join("dataScreen", page_title[i].replace(" ", "_"))
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for page in range(total_pages * 2 + 1):
        # Scroll PDF viewer and capture screenshot
        screenshot_path = os.path.join(folder_name, f"screenshot_page_{page + 1}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Saved screenshot of page {page + 1} as {screenshot_path}")

        # Scroll to next page (adjust 500 if needed)
        scroll_pdf_viewer(driver, pdf_viewer_container, 500)
        sleep(5)
        
    

# Close the browser once done
driver.quit()