from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from typing import List
import re
from langchain_openai import ChatOpenAI
from pathlib import Path
import openai
import os
from dotenv import load_dotenv

load_dotenv(Path("./.env"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Groq LLM
llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ('system', """Bạn là một chuyên gia trong việc Phân tích văn bản và xác định các điểm ngắt ngữ nghĩa tự nhiên nơi văn bản có thể bị chia tách trong khi vẫn duy trì ý nghĩa mạch lạc"""),
    ('user', """Hãy chia đoạn văn bản sau thành các semantic chunks với mỗi chunk có độ dài ít nhất 512 tokens, chỉ trả về kết quả là các semantic chunks, không giải thích. Trả về kết quả dưới dạng:
        *** doc1
        *** doc2
    Tài liệu :{document}""")
    ]     
    )


doc = """
Phương án tuyển sinh Đại học Văn Lang dự kiến năm 2021
Theo Đề án tuyển sinh ĐH chính quy dự kiến năm 2021, Trường ĐH Văn Lang dự kiến tuyển sinh 7.000 chỉ tiêu trình độ ĐH chính quy 50 ngành đào tạo, đồng thời dự kiến mở các ngành mới thuộc khối Sức khỏe.
Trường Đại học Văn Lang dự kiến mở các ngành mới năm 2021: Y Đa khoa, Y học cổ truyền,... bên cạnh những ngành hiện đã có như Răng Hàm Mặt, Điều dưỡng, Dược học, Kỹ thuật Xét nghiệm Y học.
Năm 2021, Trường ĐH Văn Lang tuyển sinh theo 5 phương thức xét tuyển độc lập và bình đẳng. Thí sinh có thể đăng ký xét tuyển/thi tuyển đồng thời nhiều phương thức:

1. Xét tuyển kết quả thi tốt nghiệp THPT năm 2021.

2. Xét tuyển kết quả học tập bậc THPT (học bạ).

3. Xét tuyển kết quả kỳ thi Đánh giá năng lực của ĐH Quốc gia TP.HCM năm 2021.

4. Xét tuyển kết hợp thi tuyển các môn năng khiếu (Vẽ, âm nhạc, sân khấu điện ảnh).

5. Xét tuyển thẳng (theo quy định của Bộ GD-ĐT và quy định của Trường ĐH Văn Lang).
Trường ĐH Văn Lang dành 60% chỉ tiêu theo phương thức xét tuyển kết quả học tập THPT, 30% chỉ tiêu cho kết quả kỳ thi THPT năm 2021, 5% chỉ tiêu theo kết quả kỳ thi Đánh giá năng lực năm 2021 của ĐH Quốc gia TP.HCM và 5% chỉ tiêu cho phương thức Xét tuyển thẳng.

Thí sinh đăng ký xét tuyển/ thi tuyển vào trường cần phải đảm bảo ngưỡng đảm bảo chất lượng đầu vào theo quy định của Bộ GD-ĐT (đối với nhóm ngành sức khỏe) và quy định của Trường ĐH Văn Lang theo từng phương thức (đối với các nhóm ngành còn lại).

Ngưỡng đảm bảo chất lượng đầu vào, điều kiện nhận hồ sơ Đăng kí xét tuyển
a. Đối với phương thức xét tuyển dựa vào điểm thi tốt nghiệp THPT 2021:
- Các ngành thuộc khối ngành sức khỏe: Dược học, Điều dưỡng, Kỹ thuật Xét nghiệm Y học, Răng – Hàm – Mặt: theo quy định của Bộ GD&ĐT. 
- Các ngành còn lại: sẽ được công bố trên cổng thông tin điện tử của Trường theo lộ trình tuyển sinh năm 2021.  
- Sử dụng Chứng chỉ ngoại ngữ quốc tế: Đối với các ngành xét tuyển có sử dụng tổ hợp môn thi có môn ngoại ngữ, nếu thí sinh có chứng chỉ IELTS từ 5.5 trở lên hoặc các chứng chỉ quốc tế tương đương (02 năm kể từ ngày dự thi) và tổng điểm 2 môn còn lại trong tổ hợp xét tuyển đạt tối thiểu 12 điểm  thì được chuyển điểm theo bảng điểm quy đổi.

b. Đối với phương thức: xét tuyển dựa vào kết quả học tập THPT (học bạ):  
- Các khối ngành sức khỏe: Dược học, Răng – Hàm – Mặt, Điều dưỡng, Kỹ thuật Xét nghiệm Y học: theo quy định của Bộ GD&ĐT. 
- Các ngành còn lại: tổng điểm của tổ hợp môn xét tuyển đạt từ 18,00 điểm trở lên (không có môn nào trong tổ hợp xét tuyển điểm dưới 1). Riêng ngành Ngôn ngữ Anh, điểm trung bình chung môn Tiếng Anh đạt từ 6,00 điểm trở lên.
- Sử dụng Chứng chỉ ngoại ngữ quốc tế: Đối với các ngành xét tuyển có sử dụng tổ hợp môn thi có môn ngoại ngữ, nếu thí sinh có chứng chỉ IELTS từ 5.5 trở lên hoặc các chứng chỉ quốc tế tương đương (02 năm kể từ ngày dự thi) và tổng điểm 2 môn còn lại trong tổ hợp xét tuyển đạt tối thiểu 12 điểm thì được chuyển điểm theo bảng điểm quy đổi.

C.  Đối với phương thức xét tuyển dựa vào kết quả Kỳ thi Đánh giá năng lực năm 2021 của Đại học Quốc gia Tp. Hồ Chí Minh: 

d. d. Đối với phương thức xét tuyển kết hợp thi tuyển môn năng khiếu: 
- Đối với 02 ngành Piano, Thanh nhạc: xét tuyển môn Ngữ văn kết hợp bài thi 2 môn năng khiếu (Ngữ văn, Năng khiếu âm nhạc 1, Năng khiếu âm nhạc 2). Điều kiện: môn Ngữ văn đạt từ 5,00 điểm trở lên; môn Năng khiếu âm nhạc 1 đạt từ 5,00 điểm trở lên; môn Năng khiếu âm nhạc 2 đạt từ 7,00 điểm trở lên.
- Đối với 02 ngành Đạo diễn điện ảnh – truyền hình, Diễn viên kịch, điện ảnh – truyền hình: xét tuyển môn Ngữ văn kết hợp bài thi 2 môn năng khiếu (Ngữ văn, NKSKĐA1, NKSKĐA2). Điều kiện: môn Ngữ văn đạt từ 5,00 điểm trở lên; môn năng khiếu sân khấu điện ảnh 1 đạt từ 5,00 điểm trở lên; môn năng khiếu sân khấu điện ảnh 2 đạt từ 7,00 điểm trở lên.
- Đối với 05 ngành: Kiến trúc, Thiết kế Nội thất, Thiết kế Đồ họa, Thiết kế Công nghiệp, Thiết kế Thời trang: xét tuyển điểm các môn văn hóa kết hợp kết quả bài thi môn Vẽ từ Trường Đại học Văn Lang hoặc 06 trường: Trường Đại học Kiến trúc Tp.HCM, Trường Đại học Mỹ thuật Tp.HCM, Trường Đại học Tôn Đức Thắng, Trường Đại học Kiến trúc Hà Nội, Trường Đại Mỹ thuật Công nghiệp, Trường ĐH Nghệ thuật (thuộc Đại học Huế).

e. Đối với phương thức: xét tuyển thẳng

Về việc tổ chức tuyển sinh 2021
a. Thời gian xét tuyển 
 (1) Xét tuyển kết quả học tập THPT (học bạ):  
• Đợt 1: từ 01/3 đến 30/4/2021; 
• Đợt 2: từ 10/5 đến 30/5/2021; 
• Đợt 3: từ 07/6 đến 30/6/2021; 
• Đợt 4: từ 5/7 đến 29/8/2021; 
• Các đợt còn lại (nếu có): từ 06/9 đến 30/10/2021.

(2) Xét tuyển kết quả kỳ thi tốt nghiệp THPT năm 2021: theo quy định của Bộ GD&ĐT. 

(3) Xét tuyển kết quả kỳ thi đánh giá năng lực năm 2021 của Đại học Quốc gia Tp.HCM: sau khi Đại học Quốc gia Tp.HCM công bố kết quả của thí sinh, Trường Đại học Văn Lang sẽ thông báo thời gian nhận hồ sơ xét tuyển, mức điểm nhận hồ sơ.

(4) Xét tuyển thẳng (xem thêm thông tin tại mục “Xét tuyển thẳng”) - Xét tuyển các đối tượng theo quy chế tuyển sinh của Bộ GD&ĐT: thí sinh nộp hồ sơ theo quy định và gửi hồ sơ xét tuyển về Bộ GD&ĐT. - Xét tuyển các đối tượng theo quy định của Trường ĐH Văn Lang như sau: 
• Đợt 1: từ 08/4 đến 30/4/2021; 
• Đợt 2: từ 10/5 đến 30/5/2021; 
• Đợt 3: từ 07/6 đến 30/6/2021; 
• Đợt 4: từ 5/7 đến 29/8/2021;

(5) Xét tuyển kết hợp thi tuyển các môn năng khiếu: thí sinh đăng ký xét tuyển vào các ngành năng khiếu của Trường Đại học Văn Lang cần đăng ký dự thi môn khiếu theo quy định (xem thêm thông tin mục “Thời gian thi tuyển các môn năng khiếu”).
"""
# Create and execute chain
chain = prompt | llm
result = chain.invoke({"document": doc})

print(result.content)
