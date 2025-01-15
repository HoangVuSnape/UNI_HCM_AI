### 1. **Mô tả bài toán**

- **Bối cảnh**: Trình bày tình hình thực tế về nhu cầu sử dụng chatbot trong tuyển sinh (VD: tự động hóa, hỗ trợ 24/7, cá nhân hóa thông tin).
- **Vấn đề**: Những thách thức của việc triển khai chatbot thông thường (thiếu chính xác, khó tùy chỉnh theo ngữ cảnh).
- **Giới thiệu RAG và Adaptive RAG**: Làm rõ vai trò của RAG và các tính năng giúp giải quyết bài toán.

---

### 2. **Mục tiêu và ý nghĩa**

- **Mục tiêu**:
    - Xây dựng chatbot tuyển sinh với khả năng trả lời chính xác, nhanh chóng.
    - Cải thiện trải nghiệm người dùng thông qua cá nhân hóa và khả năng tìm kiếm thông minh.
- **Ý nghĩa**:
    - Ứng dụng công nghệ tiên tiến vào giáo dục.
    - Giảm tải công việc cho đội ngũ tư vấn tuyển sinh.

---

### 3. **Input -> Output**

- **Input**:
    - Câu hỏi từ người dùng (VD: "Điểm chuẩn ngành CNTT là bao nhiêu?")
- **Output**:
    - Câu trả lời cụ thể, chính xác dựa trên cơ sở dữ liệu trường học (VD: "Điểm chuẩn ngành CNTT năm 2023 là 24 điểm").

---

### 4. **Related Work**

- So sánh với các nghiên cứu hoặc ứng dụng trước đây:
    - **Hạn chế** của chatbot dựa trên retrieval-only hoặc generation-only.
    - Tóm tắt các phương pháp đã triển khai trong lĩnh vực giáo dục (Intent classification, Retrieval-Augmented Generation).
- Giải thích vì sao RAG hoặc Adaptive RAG là lựa chọn tốt hơn.
- Chú ý đến các paper nào? 

---

### 5. **Kiến thức cơ sở**

- Các thuật ngữ cần thiết:
    - **RAG (Retrieval-Augmented Generation)**: Sự kết hợp giữa tìm kiếm (retrieval) và sinh ngữ liệu (generation).
    - **Adaptive RAG**: Phiên bản cải tiến với khả năng điều chỉnh theo ngữ cảnh.
    - **SQL Agent**: Kết nối chatbot với cơ sở dữ liệu SQL.
    - retrieval (simple, hybrid search). 
- Mô tả nhanh các công nghệ hỗ trợ:
    - Framework: QDrant, SQLite.. gì đó. CHuyển data này postgres nha. 
    - **WebSearch**: Tích hợp tìm kiếm trên web.

---

### 6. **Phương pháp đề xuất**

- **Lựa chọn công nghệ**:
    - Sử dụng cái nào và tại sao?
    - Phân biệt giữa RAG, Adaptive RAG, và Contextual RAG. Lý do chọn một trong các phương pháp này.
    - So sanh các phương pháp: enhance, split query when it's complex..
    - SQL code. : get correct score.
- **Cách tiếp cận**:
	- Lúc đầu dùng các gom tất cả cùng 1 collection- Cải tiến là tách ra các trường và dùng lllm để phân biệt là nó vô collection trường nào. 
    - Intent classification để hiểu ý định người dùng.
    - Query rewriting để tối ưu hóa câu truy vấn.
    - Generation (sinh văn bản) để tạo ra câu trả lời tự nhiên.

---

### 7. **Mô tả hệ thống**

- **Kiến trúc hệ thống**:
    - Các thành phần chính: Input processing, Retrieval module, Generation module, SQL agent, WebSearch module.
- **Quy trình xử lý**:
    - Người dùng nhập câu hỏi.
    - Intent classification → Retrieval từ cơ sở dữ liệu/web → Generation.
- Mô tả từng bước xử lý với Input → Output.

---
### Data:
- 15 trường đại 
- data sql
- data grouth truth....
### 8. **Thực nghiệm**

- tạo ra bộ query để test thử: 
	- Đánh giá con người
	- rag evaluation..
	- data grouth truth
- **Thực hiện**:
    - Quy trình triển khai và các bước tối ưu.

---

### 9. **Độ đo và phương pháp đánh giá**

- **Độ đo**:
    - Precision, Recall, F1-score để đánh giá hiệu suất trả lời.
- **Đánh giá chủ quan**:
    - Human evaluation: Mời chuyên gia tuyển sinh đánh giá.
- **So sánh**:
    - Đối chiếu với các mô hình khác (VD: retrieval-only).
    - So sánh adaptive rag, 
	- so sánh enhance query, complex query: hỏi về 2 trường...
	- 

---

### 10. **Kết quả**

- **Thống kê**:
    - Bảng biểu thể hiện độ chính xác của mô hình.
- **So sánh**:
    - Biểu đồ thể hiện hiệu suất giữa RAG, Adaptive RAG và các phương pháp khác.
- **Phân tích lỗi**:
    - Trình bày các trường hợp sai, nguyên nhân, và giải pháp.

---

### 11. **Bình luận và kết luận**

- Đánh giá hiệu quả của phương pháp.
- Lợi ích mang lại cho lĩnh vực tuyển sinh.
- Đề xuất cải thiện trong tương lai.
	- Thêm các trường 
	- Thêm data về học phí và 
	- CHỉ tiêu tuyển sinh
	- Tách ra font end backend
	- Dùng long term memory: ý là nếu mà data để ngày mai sẽ mất chỉ xài ngay lúc này
	- Chưa deploy...
	- 

---

### 12. **Tài liệu tham khảo**

- Danh sách các nghiên cứu, công cụ, và tài liệu đã sử dụng trong quá trình thực hiện.