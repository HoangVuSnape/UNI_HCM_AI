## **1. RLHF là gì?**

- **RLHF** là một phương pháp kết hợp giữa **Machine Learning** và phản hồi từ con người để cải thiện chất lượng của một mô hình AI.
- Thay vì chỉ dựa vào dữ liệu huấn luyện, RLHF tận dụng phản hồi từ người dùng (feedback) để tinh chỉnh mô hình, giúp nó đưa ra các kết quả phù hợp hơn.

---

## **2. Quy trình cơ bản của RLHF**

RLHF có 3 giai đoạn chính:

1. **Supervised Fine-Tuning (Huấn luyện có giám sát):**
    
    - Mô hình ban đầu (thường là một LLM như GPT) được huấn luyện trên dữ liệu đầu vào (prompt) và phản hồi mong muốn (desired response).
    - **Mục tiêu:** Đưa ra phản hồi cơ bản chính xác.
2. **Reward Model (Mô hình đánh giá phần thưởng):**
    
    - Một mô hình khác được huấn luyện để đánh giá phản hồi từ mô hình chính dựa trên phản hồi của con người.
    - **Ví dụ:** Khi người dùng đưa ra phản hồi “tốt” hoặc “xấu,” mô hình học cách gán điểm số cho từng câu trả lời.
3. **Reinforcement Learning with PPO (Học tăng cường với Proximal Policy Optimization):**
    
    - Mô hình chính được tinh chỉnh bằng thuật toán học tăng cường, dựa trên phần thưởng từ mô hình đánh giá.
    - **Mục tiêu:** Đưa ra phản hồi không chỉ đúng mà còn phù hợp với kỳ vọng của người dùng.

---

## **3. Các khái niệm cơ bản cần nắm**

### **3.1 Mô hình phần thưởng (Reward Model)**

- Là thành phần trung gian trong RLHF, được huấn luyện để đánh giá chất lượng của các phản hồi từ mô hình chính.
- Dựa trên phản hồi từ con người (feedback), mô hình này dự đoán mức độ "tốt" của mỗi phản hồi.

### **3.2 Thuật toán PPO**

- **PPO (Proximal Policy Optimization)** là một thuật toán học tăng cường:
    - Tinh chỉnh chính sách (policy) của mô hình để tối ưu hóa phần thưởng.
    - Giúp tránh việc mô hình thay đổi quá nhanh (giữ sự ổn định).

### **3.3 Phản hồi từ con người**

- Phản hồi có thể ở dạng:
    - **Binary Feedback (Tốt/Không tốt).**
    - **Ranked Feedback (Xếp hạng phản hồi từ tốt nhất đến tệ nhất).**
    - **Custom Feedback (Phản hồi cụ thể hơn, như "phản hồi quá dài").**