


**define tiêu chí đánh giá với tự động với** 
- 
Ở đây là nơi mình sẽ lưu lại những ideas và thắc mắc để hoàn thiện nâng cấp. 
# Câu hỏi
- Có cần finetuning model không?
 - Về data còn thiếu gì? - Data toàn hình ảnh, và mình chưa thu thập đủ data.
 - Chưa tạo ra 1 plateform tick hợp rag và rLHF. 


![](../../assets/images/data.png)


- Theo thầy thì mình có dùng mô hình đánh giá hay mình đánh giá tay từng câu hỏi. Và bên cạnh đó là chia ra 5 mức đánh giá hay là chỉ đánh giá là like hay không like. 
Phản hồi từ người dùng nên được thu thập như thế nào để đảm bảo tính hiệu quả?
- Trong này Mình dùng 1 mô hình LLM rồi dùng prompt để cho ra kết quả hả thầy hay là mình dùng Retrieval để ra kết quả để thu thập dữ liệu để dùng đó là data để đánh giá

- Với lại mình có tạo ra 1 bộ data để finetune để làm thành LLM của mình không. 
	- Nếu như vậy thì khi có LLM thì nó đã finetune thì nó đâu có đúng với RAG là truy xuất thông tin đúng không thầy. 

- Theo thầy mình dùng cái gì để đánh giá câu trả lời của mình. Dùng Mô hình hay là mình đánh giá bằng tay. 


Mình có 1 bài Enhace retrieval pdf của anh hiếu halong và mình không hiểu Id và context và queries của ảnh để đánh giá cho lắm. Mình cần phải biết thêm. 

Note lại 
- Mình đang có 2 hướng là 
	- 1, Lấy data mà không có retrieval mà ra đc output rồi -> reward
	- 2, Là từ retrieval của Vector DB để -> output rồi mới lấy đó để làm LLM.
	- 

## RLHF
### **4. Các câu hỏi để làm rõ RLHF**

#### **4.1 Về cơ bản RLHF là gì?**

- RLHF cải thiện mô hình bằng cách nào so với huấn luyện thông thường?
- Sự khác biệt giữa RLHF và các phương pháp tinh chỉnh khác (fine-tuning)?
- RLHF phù hợp với các loại mô hình và ứng dụng nào?

#### **4.2 Về dữ liệu và phản hồi**

- Phản hồi từ người dùng nên được thu thập như thế nào để đảm bảo tính hiệu quả?
- Làm sao để xử lý dữ liệu phản hồi không đồng nhất hoặc mâu thuẫn?
- Những dạng phản hồi nào có thể giúp cải thiện mô hình?
    - Ví dụ: **Tốt/Xấu** hay **Xếp hạng nhiều phản hồi**.

#### **4.3 Về mô hình phần thưởng**

- Mô hình phần thưởng học như thế nào từ dữ liệu phản hồi?
- Làm sao để đánh giá chất lượng của mô hình phần thưởng?
- Mô hình phần thưởng có thể bị sai lệch (bias) không? Nếu có thì cách xử lý?

#### **4.4 Về thuật toán PPO**

- PPO hoạt động như thế nào trong RLHF?
- Tại sao PPO được ưa chuộng hơn các thuật toán RL khác (như Q-learning hoặc DDPG)?
- Làm thế nào để chọn các siêu tham số (hyperparameters) trong PPO?

#### **4.5 Về ứng dụng thực tế**

- RLHF áp dụng hiệu quả nhất trong các lĩnh vực nào? (Ví dụ: chatbot, hỗ trợ y tế, tài chính...)
- Các tiêu chí nào đánh giá RLHF thành công?
- Những thách thức khi triển khai RLHF (tốn thời gian, dữ liệu phản hồi chất lượng kém...).

---

## **5. Các yếu tố cần chú ý khi triển khai RLHF**

### **5.1 Dữ liệu phản hồi**

- **Số lượng phản hồi:** RLHF cần lượng lớn phản hồi chất lượng cao để mô hình phần thưởng hoạt động tốt.
- **Đa dạng:** Phản hồi cần đến từ nhiều người dùng với các nhu cầu khác nhau.

### **5.2 Độ chính xác của mô hình phần thưởng**

- Một mô hình phần thưởng kém chính xác sẽ làm mô hình chính học sai lệch.
- Nên sử dụng tập dữ liệu kiểm thử để đánh giá mô hình phần thưởng.

### **5.3 Tinh chỉnh PPO**

- Chọn đúng tỷ lệ giữa dữ liệu mới (từ RLHF) và dữ liệu cũ để tránh mất kiến thức ban đầu.
- PPO cần được kiểm soát để không thay đổi hành vi mô hình quá mức.

---

## **6. Kịch bản đánh giá và câu hỏi cho RLHF**

- Làm thế nào để đảm bảo phản hồi của người dùng thực sự giúp cải thiện mô hình?
- Mô hình chatbot có thể trả lời chính xác trong bao nhiêu trường hợp dựa trên RLHF?
- RLHF có giúp mô hình giảm các lỗi như thông tin sai hoặc không liên quan không?

# Usecase để hoàn thiện
### **1. Mục tiêu cụ thể hơn cho các use case**

#### **Use Case 1: Chatbot hỗ trợ tra cứu thông tin quy chế sinh viên**

- **Chi tiết:**
    - Sinh viên có thể hỏi chatbot các câu liên quan đến quy chế học tập, kỷ luật, nghỉ phép, bảo lưu, tốt nghiệp.
    - Trả lời được các câu hỏi liên quan đến tài liệu PDF quy chế mà không cần người dùng phải đọc toàn bộ.
- **Ví dụ câu hỏi:**
    - "Thời gian tối đa để hoàn thành chương trình đại học là bao lâu?"
    - "Quy định về thi lại và học lại như thế nào?"
- **Đánh giá:**
    - Tỉ lệ trả lời đúng so với nội dung quy chế trong PDF (Precision).
    - Khả năng hiểu câu hỏi của sinh viên (Recall).
#### **Use Case 3: Chatbot tư vấn hành chính cho sinh viên**

- **Chi tiết:**
    - Chatbot hỗ trợ sinh viên tra cứu quy trình làm hồ sơ như xin nghỉ học, nộp đơn bảo lưu, đăng ký học lại.
    - Hướng dẫn sinh viên các bước cụ thể thay vì chỉ trả lời chung chung.
- **Ví dụ câu hỏi:**
    - "Làm thế nào để xin giấy xác nhận sinh viên?"
    - "Hạn chót nộp đơn bảo lưu là khi nào?"
- **Đánh giá:**
    - Mức độ hài lòng của người dùng qua phản hồi (RLHF).
    - Tỉ lệ trả lời đúng các bước quy trình.


# Gợi Ý tính năng
### **2. Gợi ý các tính năng bổ sung**

- **Tìm kiếm ngữ nghĩa (Semantic Search):** Khi sinh viên hỏi, chatbot hiểu nghĩa của câu hỏi thay vì chỉ tìm từ khóa.
- **Gợi ý nội dung liên quan:** Sau khi trả lời, chatbot đề xuất thêm các nội dung tương tự mà sinh viên có thể quan tâm.
    - Ví dụ: "Bạn cũng có thể xem thông tin về học lại ở mục 2.3 của tài liệu."
- **Hỗ trợ đa ngôn ngữ:** Nếu trường có sinh viên quốc tế, tích hợp hỗ trợ tiếng Anh hoặc các ngôn ngữ khác.
- **Giao diện thân thiện:** Xây dựng giao diện chatbot trực quan, dễ dùng cho cả sinh viên và giảng viên.

---

### **3. Kế hoạch đánh giá và cải thiện**

- **Đánh giá hiệu suất mô hình:**
    - **Precision/Recall:** Đo lường khả năng truy xuất thông tin từ tài liệu PDF.
    - **BLEU/ROUGE score:** Đánh giá độ tương đồng giữa câu trả lời của chatbot và tài liệu gốc.
- **Học từ phản hồi người dùng (RLHF):**
    - Tích hợp cơ chế thu thập phản hồi: Thêm nút "Hài lòng/Không hài lòng" trong giao diện chatbot.
    - Sử dụng phản hồi để tinh chỉnh chatbot, đảm bảo cải thiện sau mỗi phiên bản.
- **So sánh mô hình:**
    - Thử nghiệm các mô hình khác nhau (GPT-3.5, T5, BERT) để chọn mô hình phù hợp nhất cho tiếng Việt.

---

### **4. Hướng phát triển nâng cao**

- **Tích hợp văn bản và hình ảnh:** Nếu tài liệu có hình ảnh (biểu đồ, bảng), chatbot có thể giải thích dựa trên dữ liệu hình ảnh.
- **Khả năng giải thích (Explainability):** Khi trả lời, chatbot cho biết câu trả lời được trích dẫn từ đâu (ví dụ: "Trang 12 của tài liệu XYZ").
- **Tích hợp giọng nói:** Dùng Text-to-Speech để chatbot giao tiếp qua giọng nói, tiện lợi hơn cho người dùng.

### **5. Hình ảnh** 
- Link đến các hình ảnh của 1 trang nào nào hay là data base
- Multi modal
### **6. Hỏi đáp với wiki**