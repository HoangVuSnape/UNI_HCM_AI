"""
Mình có 1 file pdf mà chỉ dạng ảnh trong đó và mình dùng 1 mô hình ocr để từ ảnh qua text rồi nhưng mà nó bị lỗi nhiều chỗ và không được clean cho lắm. Bạn giúp mình clean lại với data sạch hơn. Vì lý do Là nhiều chữ nên mỗi lần mình sẽ gửi tầm 3 pages và bạn sẽ clean lại giúp mình:

Chỉ clean lại thôi chứ không tóm tắt.

"""


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

Hiện tại về toán mình không đá động nhiều không biết là trong báo cáo mình có cần trình bay toán không ạ. 
Tiêu chí đánh giá 1 bài báo cáo thường là gì vậy ạ. 

# Data tuyển sinh
- Nếu table tạo thành text thì rất rắc rối. 
- cái thứ 2 là mô tả về ngành đào tạo rất nhiều. 
	- Không biết có nên tải pdf về để lấy không


SQL data - query construction 
- [sql](https://python.langchain.com/docs/tutorials/sql_qa/)
- [sql agent](https://langchain-ai.github.io/langgraph/tutorials/sql-agent/)
web search, 
data 
function calling api geminai. 
- Nếu sử dụng api thì không cần colab
- Còn nếu mô hình thì có thể colab rồi tạo thử function calling
- Không thì tải bản gguf rồi ccmap để làm sever chạy thử. Đọc xem nó có hỗ trợ thử 
	- Tìm hiểu thử mô hình này có hỗ trợ tiếng việt không. 

---
# Để giải quyết vấn đề này, bạn có thể sử dụng một giải pháp kết hợp:

1. **Vẫn dùng Qdrant cho văn bản**: Để tìm kiếm các thông tin liên quan đến văn bản (ví dụ: câu hỏi trả lời hoặc tìm kiếm ngữ nghĩa trong văn bản), Qdrant là công cụ rất hiệu quả.
    
2. **Sử dụng cơ sở dữ liệu quan hệ (SQL) cho bảng**: Khi dữ liệu có cấu trúc bảng, bạn nên lưu trữ và truy vấn thông tin từ một cơ sở dữ liệu quan hệ (ví dụ: MySQL, PostgreSQL). Sau đó, bạn có thể sử dụng các truy vấn SQL để lấy dữ liệu từ các bảng đó, đảm bảo tính chính xác và hiệu quả khi làm việc với dữ liệu có cấu trúc.
    
3. **Kết hợp cả hai**: Bạn có thể kết hợp kết quả từ Qdrant (tìm kiếm văn bản) và SQL (truy vấn dữ liệu bảng). Ví dụ, khi cần thông tin từ bảng, bạn có thể truy vấn SQL để lấy dữ liệu có cấu trúc, trong khi Qdrant có thể giúp bạn tìm kiếm thông tin từ văn bản hoặc các câu hỏi không có cấu trúc. Một cách tiếp cận phổ biến là sử dụng cả hai nguồn dữ liệu và kết hợp kết quả từ chúng trong một hệ thống RAG.
    

Vậy bạn sẽ cần dùng nhiều DB (Qdrant cho embedding và một DB quan hệ như PostgreSQL hoặc MySQL cho bảng), nhưng bạn chỉ cần quản lý một cách hợp lý để truy vấn và kết hợp thông tin từ cả hai nguồn.
# Tiếp tuần này:
- Mình đang cần tạo ra data ground truth. để đánh giá về retrieval và rerank
- Mình chưa matryoskla và những khía cảnh khác như transformation và router.
- https://github.com/langchain-ai/rag-from-scratch
[Rerank_Retrieval_Evaluation](Rerank_Retrieval_Evaluation.md)

Tuần này:
- https://blog.langchain.dev/query-construction/
- 


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