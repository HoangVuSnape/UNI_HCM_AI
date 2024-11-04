# crawl.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from functions import read_credentials, get_title_link_info, write_to_file  # Import functions

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
write_to_file(page1_titles, page1_link, page1_phong, filename="page1.txt")

sleep(2)

# Page 2
page2 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[2]/div/div[2]/nav/ul[3]/li[1]/a')
page2.click()

page2_titles, page2_link, page2_phong = [], [], []
page2_titles, page2_link, page2_phong = get_title_link_info(driver, page2_titles, page2_link, page2_phong)

# Write Page 2 data to file
write_to_file(page2_titles, page2_link, page2_phong, filename="page2.txt")

sleep(2)

# Page 3
page3_titles, page3_link, page3_phong = [], [], []
page2.click()  # Assuming the same link for page 3
page3_titles, page3_link, page3_phong = get_title_link_info(driver, page3_titles, page3_link, page3_phong)

# Write Page 3 data to file
write_to_file(page3_titles, page3_link, page3_phong, filename="page3.txt")

sleep(2)

# Close the browser after everything is done
driver.quit()
