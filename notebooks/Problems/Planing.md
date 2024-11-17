## **Giai đoạn 1: Khởi động và nghiên cứu (13/11/2024 - 24/11/2024)**

### **Mục tiêu:**

- Xác định yêu cầu cụ thể của hệ thống chatbot.
- Thu thập tài liệu, tệp PDF quy định và quy chế của trường.
- Nghiên cứu các công nghệ cần sử dụng: RAG, RLHF.

### **Công việc cụ thể:**

1. **Tìm hiểu yêu cầu và thu thập tài liệu (13/11 - 19/11):**
    
    - **Quý Vũ**: Thu thập tất cả các tài liệu PDF quy định, quy chế cần thiết từ trường học. Liệt kê và tổ chức các tài liệu.
    - **Quốc An**: Tìm hiểu kỹ thuật RAG và xác định cách trích xuất thông tin từ PDF.
    - **Bạn (người dùng)**: Nghiên cứu RLHF và cách áp dụng phản hồi từ người dùng để cải thiện chatbot.
2. **Phân tích và xây dựng mô hình dữ liệu (20/11 - 24/11):**
    
    - Xây dựng cấu trúc dữ liệu lưu trữ thông tin trích xuất từ các tệp PDF.
    - Nghiên cứu cách triển khai truy xuất tài liệu (RAG).
    -  Lên kế hoạch tích hợp phản hồi người dùng (RLHF) vào pipeline của chatbot.

---
## Note 
### 11/17/2024 - Metting
##### Vấn đề
- Data toàn dạng hình ảnh và chưa có text đc
- Data đang thiếu nên cần crawl thêm
- Platform tích hợp về RAG và RLHF chưa đc 
- Tìm model để embedding data vietnamese. 
- Rerank retrival cần thực hiện để có những kết quả từ những pdf... thì khi đó mình mới đánh giá. 
##### Những thắc mắc
-  Theo thầy thì mình có dùng mô hình đánh giá hay mình đánh giá tay từng câu hỏi. Và bên cạnh đó là chia ra 5 mức đánh giá hay là chỉ đánh giá là like hay không like. 
##### Cần làm
- Data cần phải clean và hoàn thiện
- Platform RAG và rhfl
- Tìm data để finetune về câu hỏi QA và summary 
- Nghiên cứu sâu về RHFL về thuật toán. 

Ngày tiếp theo là thứ 3 - 11/19/2024
### 11/19/2024 - Metting
##### Vấn đề

## **Giai đoạn 2: Thiết kế và phát triển MVP (25/11/2024 - 15/12/2024)**

### **Mục tiêu:**

- Phát triển giao diện frontend.
- Xây dựng backend hỗ trợ xử lý dữ liệu và tích hợp mô hình.
- Hoàn thành phiên bản chatbot cơ bản (MVP).

### **Công việc cụ thể:**

1. **Thiết kế giao diện và API (25/11 - 01/12):**
    
    - **Quý Vũ**: Thiết kế giao diện đơn giản (web hoặc ứng dụng) cho chatbot. Dùng các công cụ như React hoặc Flutter.
    - **Quốc An**: Xây dựng API backend hỗ trợ truy xuất thông tin từ dữ liệu PDF.
    - **Bạn**: Lên kịch bản hội thoại mẫu và thiết kế logic trả lời cơ bản cho chatbot.
2. **Tích hợp RAG và RLHF (02/12 - 08/12):**
    
    - **Quý Vũ**: Kết nối frontend với backend qua API.
    - **Quốc An**: Tích hợp kỹ thuật RAG vào pipeline backend.
    - **Bạn**: Tạo cơ chế thu thập phản hồi từ người dùng và tích hợp RLHF vào hệ thống.
3. **Hoàn thành phiên bản MVP (09/12 - 15/12):**
    
    - **Quý Vũ**: Hoàn thiện giao diện người dùng.
    - **Quốc An**: Kiểm tra truy xuất thông tin từ PDF và cải thiện độ chính xác.
    - **Bạn**: Tinh chỉnh logic hội thoại và đảm bảo phản hồi từ người dùng được sử dụng hiệu quả.

---

## **Giai đoạn 3: Tinh chỉnh và triển khai (16/12/2024 - 01/01/2025)**

### **Mục tiêu:**

- Tinh chỉnh hệ thống dựa trên kết quả thử nghiệm.
- Triển khai hệ thống trên server thực tế.

### **Công việc cụ thể:**

1. **Thử nghiệm và cải thiện hệ thống (16/12 - 22/12):**
    
    - **Quý Vũ**: Thu thập phản hồi từ người dùng thử nghiệm (sinh viên, giảng viên).
    - **Quốc An**: Sửa lỗi và tối ưu truy xuất thông tin từ PDF.
    - **Bạn**: Cải thiện chatbot qua RLHF dựa trên phản hồi thu được.
2. **Triển khai hệ thống (23/12 - 29/12):**
    
    - **Quý Vũ**: Thiết lập server để triển khai hệ thống (sử dụng AWS, Azure, hoặc các nền tảng khác).
    - **Quốc An**: Triển khai backend và kiểm tra độ ổn định.
    - **Bạn**: Đảm bảo pipeline RLHF hoạt động trơn tru trên môi trường thực tế.
3. **Hoàn thiện báo cáo và bàn giao sản phẩm (30/12 - 01/01):**
    
    - **Quý Vũ**: Hoàn thiện phần trình bày giao diện và quy trình sử dụng.
    - **Quốc An**: Tổng hợp các bước phát triển backend và kỹ thuật RAG.
    - **Bạn**: Hoàn thiện báo cáo về RLHF và kế hoạch cải thiện chatbot sau khi triển khai.