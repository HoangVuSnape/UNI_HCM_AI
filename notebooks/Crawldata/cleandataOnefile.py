import re
from textwrap import fill

def clean_text(text):
    # Thêm một dòng trống ngay bên dưới các tiêu đề Page và đảm bảo nội dung bắt đầu từ dòng mới
    text = re.sub(r'(Page\s*\d+:)', r'\1\n', text)

    # Loại bỏ khoảng trắng thừa và ký tự đặc biệt không mong muốn
    text = re.sub(r'\s+', ' ', text)  # Thay nhiều khoảng trắng liên tiếp thành một khoảng trắng duy nhất
    text = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', text)  # Điều chỉnh khoảng cách trước và sau dấu câu
    text = re.sub(r'\s*-\s*', '-', text)  # Xóa khoảng trắng xung quanh dấu gạch ngang

    # Xóa các số và dấu chấm lẻ ở đầu dòng (do định dạng PDF có thể gây ra)
    text = re.sub(r'(\d+\s*\.|\d+\s+)', '', text)

    # Thêm hai dòng trống phía trước mỗi tiêu đề "Page" để tách biệt các trang
    text = re.sub(r'(Page\s*\d+:)', r'\n\n\1\n', text)

    return text.strip()

def format_text(text, width=80):
    # Chia nhỏ các đoạn văn bản cho dễ đọc và căn chỉnh lại chiều rộng văn bản
    paragraphs = text.split('\n')
    formatted_text = "\n\n".join(fill(paragraph, width=width) for paragraph in paragraphs)
    return formatted_text

def process_pdf_text(file_path, output_path):
    # Đọc dữ liệu từ file đầu vào
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Làm sạch và định dạng lại dữ liệu
    cleaned_text = clean_text(raw_text)
    formatted_text = format_text(cleaned_text)

    # Lưu dữ liệu đã làm sạch vào file đầu ra
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(formatted_text)
    print(f"Làm sạch và định dạng xong! Đã lưu vào {output_path}")

# Đường dẫn file đầu vào và đầu ra
# Sử dụng raw string để đảm bảo đường dẫn được xử lý chính xác
input_file = r"E:\LLM_clone\Tdtu-chatbot\notebooks\Crawldata\data\page1\ĐẶC ĐIỂM NHẬN DIỆN SINH VIÊN TDTU.txt"
output_file = r"E:\LLM_clone\Tdtu-chatbot\notebooks\Crawldata\data\cleaned_text_output1.txt"

# Chạy hàm xử lý
process_pdf_text(input_file, output_file)