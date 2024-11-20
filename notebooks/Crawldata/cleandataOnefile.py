
import re
from textwrap import fill

import re
from textwrap import fill

def clean_text(input_text):
    if re.search(r'\b([A-Z]{2,}\s+){2,}[A-Z]{2,}\b', input_text):
        return input_text

    # Đảm bảo Page x: xuống dòng và cách ra 2 dòng trước đó
    text = re.sub(r'(\s*)(Page\s*\d+:)', r'\n\n\2\n', input_text)

    # Gộp các dòng
    text = re.sub(r'\n+', ' ', text)

    # Loại bỏ khoảng trắng thừa
    text = re.sub(r'\s{2,}', ' ', text)

    # Thêm dòng trước và sau cụm từ
    text = re.sub(r'(BỘ QUY TẮC ỨNG XỬ CỦA NGƯỜI HỌC)', r'\n\1\n', text)

    # Thêm dòng trước các mục La Mã
    text = re.sub(r'([IVXLCDM]+\.)', r'\n\n\1', text)

    # Thêm dòng trước các số thứ tự
    text = re.sub(r'(\d+\.)', r'\n\1', text)

    # Thêm dòng trước các mục nhỏ dạng chữ thường kèm ngoặc
    text = re.sub(r'([a-z]\))', r'\n\1', text)

    # Sửa lỗi khoảng trắng trong văn bản tiếng Việt có dấu
    text = re.sub(r'(\w)\s+([̣̀́̉̃])', r'\1\2', text)
    text = re.sub(r'([̣̀́̉̃])\s+(\w)', r'\1\2', text)
    text = re.sub(r'(\w)\s+([̣̀́̉̃]\w)', r'\1\2', text)
    text = re.sub(r'\b(\w)\s(\w)\b', r'\1\2', text)

    # Chuẩn hóa văn bản tiếng Việt
    def normalize_vietnamese_text(text):
        replacements = {
            "à": "à", "á": "á", "ả": "ả", "ã": "ã", "ạ": "ạ",
            "ầ": "ầ", "ấ": "ấ", "ẩ": "ẩ", "ẫ": "ẫ", "ậ": "ậ",
            "ằ": "ằ", "ắ": "ắ", "ẳ": "ẳ", "ẵ": "ẵ", "ặ": "ặ",
            "è": "è", "é": "é", "ẻ": "ẻ", "ẽ": "ẽ", "ẹ": "ẹ",
            "ò": "ò", "ó": "ó", "ỏ": "ỏ", "õ": "õ", "ọ": "ọ",
            "ồ": "ồ", "ố": "ố", "ổ": "ổ", "ỗ": "ỗ", "ộ": "ộ",
            "ờ": "ờ", "ớ": "ớ", "ở": "ở", "ỡ": "ỡ", "ợ": "ợ",
            "ù": "ù", "ú": "ú", "ủ": "ủ", "ũ": "ũ", "ụ": "ụ",
            "ừ": "ừ", "ứ": "ứ", "ử": "ử", "ữ": "ữ", "ự": "ự",
            "ì": "ì", "í": "í", "ỉ": "ỉ", "ĩ": "ĩ", "ị": "ị",
            "ỳ": "ỳ", "ý": "ý", "ỷ": "ỷ", "ỹ": "ỹ", "ỵ": "ỵ"
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        return text

    text = normalize_vietnamese_text(text)

    # Wrap nội dung để đảm bảo độ dài dòng
    lines = text.splitlines()
    wrapped_lines = [fill(line.strip(), width=80) if line.strip() else line for line in lines]

    return "\n".join(wrapped_lines).strip()



def process_pdf_text(file_path, output_path):
    # Đọc dữ liệu từ file đầu vào
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Làm sạch và định dạng lại dữ liệu
    cleaned_text = clean_text(raw_text)
    
    # Lưu dữ liệu đã làm sạch vào file đầu ra
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    print(f"Làm sạch và định dạng xong! Đã lưu vào {output_path}")

# Đường dẫn file đầu vào và đầu ra
# Sử dụng raw string để đảm bảo đường dẫn được xử lý chính xác
input_file = r"E:\LLM_clone\Tdtu-chatbot\notebooks\Crawldata\Thông tin các Phòng_Ban_Trung tâm.txt"
output_file = r"E:\LLM_clone\Tdtu-chatbot\notebooks\Crawldata\cleaned_text_output7.txt"

# Chạy hàm xử lý
process_pdf_text(input_file, output_file)



