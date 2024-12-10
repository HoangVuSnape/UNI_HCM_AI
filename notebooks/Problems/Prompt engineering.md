# Meta 
### **Phân Tích Chi Tiết Meta Prompting**

#### 1. **Đặc điểm chính** _(Key Characteristics)_

Theo nghiên cứu của Zhang et al. (2024), **meta prompting** có những đặc điểm sau:

1. **Cấu trúc ưu tiên (Structure-oriented)**
    
    - Tập trung vào định dạng và mô hình của vấn đề và giải pháp thay vì nội dung cụ thể.
    - Ví dụ: Thay vì hỏi trực tiếp “Kết quả của 2 + 2 là gì?”, một meta prompt sẽ yêu cầu mô hình **tuân theo quy trình cụ thể** để tính toán.
2. **Tập trung vào cú pháp (Syntax-focused)**
    
    - Sử dụng cú pháp như một khung hướng dẫn để định hình đầu ra mong muốn.
    - Ví dụ: _"Hãy trả lời theo định dạng: [Giới thiệu] - [Giải thích chi tiết] - [Kết luận]."_
3. **Ví dụ trừu tượng (Abstract examples)**
    
    - Cung cấp các ví dụ mang tính khái quát để minh họa cấu trúc của vấn đề và cách giải quyết, không tập trung vào chi tiết cụ thể.
    - Ví dụ: Thay vì đưa một bài toán cụ thể, meta prompt đưa ra dạng bài toán chung: _“Nếu bài toán là f(x) = g(y), làm thế nào để giải y?”
    - ![](../../assets/images/Pasted%20image%2020241206153056.png)
4. **Đa năng (Versatile)**
    
    - Có thể áp dụng trong nhiều lĩnh vực, giúp cung cấp các phản hồi có cấu trúc cho nhiều loại vấn đề khác nhau.
5. **Tiếp cận phân loại (Categorical approach)**
    
    - Dựa trên **lý thuyết kiểu** (_type theory_) để nhấn mạnh sự phân loại và sắp xếp hợp lý các thành phần trong prompt.
    - Ví dụ: Phân loại các bước giải toán thành "Dữ kiện", "Phân tích", và "Kết luận".

---
![](../../assets/images/Pasted%20image%2020241202155807.png)
![](../../assets/images/Pasted%20image%2020241206161430.png)
""" 
câu hỏi: ddđ?
trả lời: 

**hỏi:** ddđ ?
**trả lời:** hhhhhhhh

**hỏi**: ddđ ?
**trả lời**: hhhhhhh
 Cấu trúc output sinh câu hỏi - trả lời
 output
 ""
 **hỏi:** ddđ ?
**trả lời:** hhhhhhhh
""""
#### 2. **Sự Khác Biệt So Với Few-Shot Prompting**

Cả **meta prompting** và **few-shot prompting** đều là kỹ thuật tương tác với LLM, nhưng có sự khác biệt rõ ràng:



| **Đặc điểm**       | **Few-Shot Prompting**                                   | **Meta Prompting**                                            |
| ------------------ | -------------------------------------------------------- | ------------------------------------------------------------- |
| **Cách tiếp cận**  | Tập trung vào nội dung (content-driven).                 | Tập trung vào cấu trúc (structure-oriented).                  |
| **Ví dụ sử dụng**  | Đưa ra một vài ví dụ cụ thể để mô hình học cách trả lời. | Đưa ra ví dụ trừu tượng nhấn mạnh cách tổ chức và giải quyết. |
| **Ứng dụng chính** | Phù hợp với các vấn đề yêu cầu nhiều dữ kiện cụ thể.     | Phù hợp với các vấn đề cần giải pháp có tổ chức.              |
| **Độ tổng quát**   | Tương đối phụ thuộc vào ngữ cảnh và nội dung.            | Tính tổng quát cao, áp dụng đa dạng ngữ cảnh.                 |

---

#### 3. **Ví dụ Minh Họa**

##### Bài toán từ MATH Benchmark:

_Giả sử đề bài yêu cầu tính giá trị của 2x+3=72x + 3 = 72x+3=7._

- **Few-Shot Prompting**:
	Example 1: 
	Problem: 3x + 4 = 10. 
	Solution: Subtract 4 from both sides to get 3x = 6. Then divide by 3 to get x = 2.
	
	Problem: 5x - 1 = 9.
	Solution: Add 1 to both sides to get 5x = 10. Then divide by 5 to get x = 2.
	
	Problem: 2x + 3 = 7.
	Solution: ?
- **Meta Prompting**:

	To solve a linear equation of the form ax + b = c:
	1. Subtract b from both sides.
	2. Divide both sides by a to isolate x.
	Example: Solve 2x + 3 = 7 by following the steps.


---

#### 4. **Lợi Ích của Meta Prompting**

1. **Tổng quát hóa**: Phù hợp với nhiều loại vấn đề và không cần điều chỉnh nhiều khi chuyển ngữ cảnh.
2. **Cấu trúc rõ ràng**: Đầu ra được tổ chức tốt hơn vì mô hình được hướng dẫn theo khuôn mẫu cụ thể.
3. **Khả năng ứng dụng rộng rãi**: Dễ dàng mở rộng sang các lĩnh vực khác nhau mà không cần tạo lại _prompt_ mới.

#### 5. **Thách Thức**

1. **Đòi hỏi thiết kế tỉ mỉ**: Việc xây dựng meta prompt cần sự hiểu biết sâu về cấu trúc vấn đề và kỹ thuật NLP.
2. **Khó với mô hình nhỏ**: Mô hình không đủ lớn có thể gặp khó khăn trong việc xử lý các cú pháp và khung trừu tượng phức tạp.

# **Self-Consistency**

**Self-Consistency** là một kỹ thuật tiên tiến trong **prompt engineering**, được đề xuất bởi Wang et al. (2022), nhằm cải thiện hiệu quả của **chain-of-thought prompting** (CoT). Kỹ thuật này thay thế việc giải mã tham lam (greedy decoding) truyền thống bằng cách:

1. **Tạo ra nhiều con đường suy luận khác nhau** dựa trên **few-shot CoT**.
2. **Lựa chọn câu trả lời nhất quán nhất** từ các kết quả được sinh ra.

Phương pháp này giúp cải thiện hiệu suất trong các bài toán liên quan đến tính toán số học (_arithmetic reasoning_) và suy luận thông thường (_commonsense reasoning_).
![](../../assets/images/Pasted%20image%2020241202161955.png)
---

### **Nguyên Lý Hoạt Động**

**Self-Consistency** hoạt động qua các bước sau:

1. **Tạo nhiều đầu ra suy luận khác nhau**:
    
    - Với cùng một prompt, LLM được yêu cầu tạo ra nhiều câu trả lời bằng cách sử dụng các kỹ thuật như sampling (ví dụ: sử dụng _temperature sampling_ để tăng tính đa dạng trong đầu ra).
2. **Tìm kiếm sự nhất quán**:
    
    - Các kết quả được so sánh để tìm câu trả lời xuất hiện phổ biến nhất hoặc câu trả lời có logic chặt chẽ nhất.
3. **Xác định câu trả lời cuối cùng**:
    
    - Câu trả lời được chọn dựa trên sự đồng thuận từ các suy luận khác nhau.

---

### **Ví Dụ Minh Họa**

#### **Prompt ban đầu**:

_"When I was 6 my sister was half my age. Now I’m 70 how old is my sister?"_

1. **Đầu ra truyền thống**:
    
    Sao chép mã
    
    `Output: 35`
    
    - Câu trả lời này sai vì áp dụng sai suy luận logic.

---

#### **Áp dụng Self-Consistency**

Sử dụng **few-shot CoT** (các ví dụ từ Wang et al. 2022):

1. **Prompt với Few-Shot Examples**:
    
    - Đưa vào các ví dụ giải toán số học cụ thể, hướng dẫn mô hình thực hiện từng bước suy luận logic.
2. **Đầu ra từ nhiều lần sinh (sampling outputs)**:
    
    Sao chép mã
    
    `Output 1: When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70 - 3 = 67. The answer is 67.  Output 2: When the narrator was 6, his sister was half his age, which is 3. Now that the narrator is 70, his sister would be 70 - 3 = 67 years old. The answer is 67.  Output 3: When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70/2 = 35. The answer is 35.`
    
3. **Xác định câu trả lời cuối cùng**:
    
    - Phân tích các đầu ra:
        - **Output 1 và Output 2** đồng nhất (suy luận đúng, câu trả lời là 67).
        - **Output 3** không phù hợp (suy luận sai, câu trả lời là 35).
    - **Kết quả cuối cùng**: Chọn câu trả lời **67** vì nó được đa số suy luận hỗ trợ.

---

### **Ưu Điểm của Self-Consistency**

1. **Tăng độ chính xác**:
    
    - Giảm nguy cơ mắc lỗi từ những suy luận không đầy đủ hoặc sai lệch.
2. **Xử lý bài toán phức tạp**:
    
    - Phương pháp này đặc biệt hiệu quả với các bài toán yêu cầu nhiều bước logic, như toán học hoặc suy luận thông thường.
3. **Đa dạng hóa đầu ra**:
    
    - Việc lấy mẫu (sampling) tạo ra các cách giải quyết khác nhau, giúp mô hình tiếp cận bài toán từ nhiều góc độ.

---

### **Hạn Chế**

1. **Tốn tài nguyên**:
    
    - Cần sinh nhiều đầu ra, tăng chi phí tính toán.
2. **Phụ thuộc vào số lượng mẫu**:
    
    - Cần đủ số lượng đầu ra để có thể xác định câu trả lời nhất quán.

---

### **Kết Luận**

**Self-Consistency** là một cải tiến quan trọng trong việc tăng độ chính xác của mô hình ngôn ngữ lớn trên các tác vụ suy luận logic. Thay vì dựa vào một lần suy luận tham lam, kỹ thuật này tạo ra nhiều đầu ra đa dạng, từ đó lựa chọn câu trả lời khả thi nhất dựa trên sự đồng thuận. Điều này không chỉ giúp cải thiện độ tin cậy của hệ thống mà còn giúp các mô hình giải quyết hiệu quả các bài toán phức tạp, đặc biệt là những bài toán đòi hỏi nhiều bước suy luận chặt chẽ.