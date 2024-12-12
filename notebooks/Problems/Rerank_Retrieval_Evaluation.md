# Link
- https://viblo.asia/p/retrieval-augmented-generation-phuong-phap-khong-the-thieu-khi-trien-khai-cac-du-an-llm-trong-thuc-te-phan-1-Ny0VG7yzVPA
- [Đánh giá retrieval](https://blog.duyet.net/2019/08/ir-evaluation.html)
- https://qdrant.tech/articles/hybrid-search/
- https://github.com/langchain-ai/langchain/blob/master/libs/partners/qdrant/langchain_qdrant/sparse_embeddings.py
- https://developer.chatx.vn/ii-tinh-nang-co-ban/rag-tao-tang-cuong-truy-xuat/rerank-sap-xep-lai
# Rerank
Việc **rerank** sau khi đã lấy kết quả tìm kiếm (như trong trường hợp bạn đã tìm được 5 kết quả tốt nhất dựa trên cosine similarity) có thể là **cần thiết** hoặc **không cần thiết**, tùy thuộc vào mục tiêu và yêu cầu cụ thể của bài toán bạn đang giải quyết.

### Ý nghĩa của **reranking**:

1. **Tối ưu lại thứ tự kết quả**: Mặc dù bạn đã lấy ra các kết quả gần nhất dựa trên cosine similarity (những điểm số cao nhất), nhưng **rerank** có thể giúp cải thiện thứ tự kết quả bằng cách sử dụng một số thông tin bổ sung hoặc một mô hình khác để đánh giá lại các kết quả tìm được. Ví dụ, bạn có thể sử dụng một mô hình học sâu (fine-tuned) để đánh giá lại thứ tự của các kết quả, kết hợp thêm các yếu tố như **relevance** hay **importance** của các kết quả.
    
2. **Đánh giá bổ sung với các tiêu chí khác**: Nếu chỉ dựa vào cosine similarity (hoặc độ tương đồng vector), bạn có thể bỏ qua những yếu tố khác như:
    
    - **Độ dài văn bản**: Một số văn bản có thể rất ngắn và không chứa đầy đủ thông tin, trong khi một văn bản dài có thể chứa nhiều thông tin hữu ích hơn.
    - **Định dạng câu hỏi**: Một số mô hình có thể biết cách điều chỉnh câu trả lời dựa trên cách câu hỏi được đặt ra (ví dụ: có thể đánh giá lại câu trả lời có liên quan đến dạng câu hỏi hơn).
3. **Các mô hình học máy để rerank**: Thông thường, sau khi tìm được các kết quả từ search engine (như Qdrant), bạn có thể **rerank** các kết quả này bằng cách sử dụng các mô hình đã được fine-tuned cho việc đánh giá **relevance** giữa truy vấn và kết quả, như:
    
    - **BERT hoặc RoBERTa** fine-tuned trên bài toán **Ranking**.
    - **Learning to Rank**: Phương pháp này sử dụng các mô hình học máy (như XGBoost, LightGBM) để học cách xếp hạng các kết quả dựa trên các đặc trưng của truy vấn và tài liệu.

### Khi nào không cần rerank:

Nếu bạn đã lấy ra **5 kết quả tốt nhất** dựa trên cosine similarity từ Qdrant (một hệ thống vector search), thì về lý thuyết, các kết quả này đã có độ liên quan khá cao với truy vấn của bạn. Trong trường hợp này, bạn không nhất thiết phải **rerank** nếu các kết quả này đáp ứng đủ yêu cầu về độ chính xác và không cần thêm sự điều chỉnh nào. Các trường hợp này có thể bao gồm:

- **Query đơn giản**: Truy vấn không quá phức tạp và không cần phải điều chỉnh thứ tự kết quả.
- **Sự khác biệt nhỏ**: Các kết quả đã có điểm cosine similarity gần nhau, và thứ tự ban đầu đã đủ tốt.

### Khi nào **rerank** là cần thiết:

1. **Cải thiện chất lượng kết quả**: Khi bạn cần cải thiện độ chính xác của kết quả tìm kiếm, reranking có thể giúp điều chỉnh lại các kết quả và đưa ra thứ tự tối ưu hơn.
2. **Truy vấn phức tạp**: Nếu truy vấn có sự phức tạp hoặc có sự mơ hồ, reranking có thể giúp mô hình hiểu được nội dung ngữ nghĩa của truy vấn một cách chính xác hơn.
3. **Cải thiện trải nghiệm người dùng**: Nếu bạn muốn kết quả không chỉ giống nhau về nội dung mà còn phù hợp với mục đích cụ thể của người dùng, reranking có thể giúp tạo ra các câu trả lời tinh tế hơn, tốt hơn cho yêu cầu của người tìm kiếm.

### Ví dụ thực tế:

Giả sử bạn đang xây dựng một hệ thống trả lời câu hỏi tự động và bạn đã sử dụng Qdrant để tìm kiếm 5 câu trả lời có độ tương đồng cao nhất với truy vấn "Một tín chỉ được tính tương đương bao nhiêu giờ học". Sau khi lấy được 5 kết quả tốt nhất, bạn có thể **rerank** những kết quả này bằng một mô hình fine-tuned (chẳng hạn như BERT) để đảm bảo thứ tự kết quả phản ánh chính xác hơn về **tính liên quan** với câu hỏi.

### Tóm lại:

- **Nếu bạn chỉ cần kết quả tìm kiếm đơn giản**, không cần phải rerank thêm, vì cosine similarity đã đủ để chọn lựa các kết quả tốt nhất.
- **Nếu bạn muốn tối ưu hoặc cải thiện chất lượng kết quả**, rerank có thể giúp bạn đưa ra các kết quả chính xác hơn, đặc biệt khi sử dụng các mô hình học sâu hoặc phương pháp học máy khác để đánh giá độ liên quan và chất lượng của các kết quả.


![](../../assets/images/Pasted%20image%2020241208204220.png)![](../../assets/images/Pasted%20image%2020241208204248.png)
## Blog 
- đây là tìm trên mì AI để về rerank tiếng việt

[Link post Nguyễn Bá đại](https://www.facebook.com/groups/miaigroup/posts/1653862535385012/)
Ở đây có nói các mô hình rerank để đánh giá và so sánh nó
![](../../assets/images/Pasted%20image%2020241211223340.png)
![](../../assets/images/Pasted%20image%2020241211223408.png)


# Evaluation
- ![](../../assets/images/Pasted%20image%2020241210140202.png)

# Hybrid seach
- https://qdrant.tech/articles/hybrid-search/
- https://github.com/qdrant/workshop-ultimate-hybrid-search/blob/main/notebooks/02-hybrid-search.ipynb
![](../../assets/images/Pasted%20image%2020241210141239.png)
![](../../assets/images/Pasted%20image%2020241210141335.png)
![](../../assets/images/Pasted%20image%2020241210141402.png)
Đúng là khi tài liệu **relevant** (liên quan) và **non-relevant** (không liên quan) không thể phân tách rõ ràng trong không gian điểm số 2D, thì việc sử dụng kết hợp tuyến tính của các điểm số từ các phương pháp tìm kiếm khác nhau (như Qdrant và BM25) sẽ không hiệu quả trong việc tạo ra một mô hình tìm kiếm kết hợp (hybrid search) tốt.

### Tại sao nó không ổn?

1. **Không tách biệt rõ ràng**:
    
    - Khi bạn vẽ phân phối các điểm số từ hai phương pháp tìm kiếm trong không gian 2D, nếu các tài liệu liên quan và không liên quan bị trộn lẫn mà không có sự phân tách rõ ràng, thì một công thức tuyến tính (như Scorefinal=w1×ScoreQdrant+w2×ScoreBM25\text{Score}_{final} = w_1 \times \text{Score}_{Qdrant} + w_2 \times \text{Score}_{BM25}) sẽ không có khả năng phân biệt được tài liệu nào là liên quan và tài liệu nào không liên quan.
    - Điều này giống như việc cố gắng vẽ một đường thẳng để phân tách hai nhóm điểm mà chúng lại nằm lẫn vào nhau, không có cách nào chỉ dùng một đường thẳng để phân loại chính xác.
2. **Điểm số không đồng nhất**:
    
    - Các phương pháp tìm kiếm như BM25 và Qdrant có thể trả về điểm số ở các phạm vi khác nhau. Điều này làm cho việc kết hợp chúng trở nên khó khăn hơn, vì một phương pháp có thể đánh giá một tài liệu là rất liên quan trong khi phương pháp kia lại đánh giá nó thấp hơn. Khi không có sự phân tách rõ ràng, việc kết hợp điểm số theo tỷ lệ tuyến tính có thể dẫn đến kết quả không chính xác.

### Vậy phải làm gì để "ổn"?

Mặc dù kết hợp tuyến tính không hiệu quả trong trường hợp này, nhưng vẫn có các phương pháp khác có thể giải quyết vấn đề này:

### **1. Các phương pháp phi tuyến tính (Non-linear methods)**:

- Thay vì chỉ dựa vào kết hợp tuyến tính, bạn có thể sử dụng các phương pháp **phi tuyến tính** để kết hợp điểm số. Ví dụ, sử dụng **học sâu (deep learning)** hoặc **mạng neural** để học cách kết hợp điểm số từ các phương pháp tìm kiếm khác nhau một cách thông minh hơn, giúp phân biệt được tài liệu liên quan và không liên quan.
- Các mô hình học sâu như **cross-encoder** hoặc **late interaction models** như **ColBERT** có thể đánh giá sự liên quan của tài liệu dựa trên ngữ nghĩa, thay vì chỉ dựa vào các điểm số đơn giản.

### **2. Reranking với mô hình học sâu**:

- Một cách tiếp cận khác là sử dụng **reranking**: sau khi phương pháp tìm kiếm nhanh (BM25 hoặc Qdrant) trả về một tập con nhỏ các tài liệu, bạn có thể sử dụng một mô hình học sâu (như một **cross-encoder**) để **rerank** lại các tài liệu này dựa trên ngữ nghĩa và mối quan hệ giữa truy vấn và tài liệu.
- Mô hình học sâu này có thể xử lý phi tuyến tính và đưa ra một sự phân biệt rõ ràng hơn giữa tài liệu liên quan và không liên quan.

### **3. Fusion với các phương pháp phức tạp hơn**:

- Bạn có thể thử sử dụng các phương pháp fusion phức tạp hơn, chẳng hạn như **Reciprocal Rank Fusion (RRF)** hoặc **Weighted Sum Fusion**, kết hợp nhiều phương pháp tìm kiếm (bao gồm BM25 và Qdrant) theo cách không chỉ đơn thuần là tuyến tính, mà có thể sử dụng các trọng số và tính toán lại dựa trên độ tin cậy của mỗi phương pháp.

### **4. Sử dụng các mô hình kết hợp chuyên sâu**:

- Một số hệ thống tìm kiếm hybrid hiện đại, chẳng hạn như **ColBERT** (a late interaction model), có thể sử dụng các kỹ thuật học sâu để học cách kết hợp các kết quả từ các phương pháp khác nhau mà không cần phải phân biệt chúng theo cách tuyến tính. Đây là một lựa chọn tốt khi bạn cần sự linh hoạt và độ chính xác cao trong việc kết hợp nhiều phương pháp tìm kiếm.

### **Kết luận**:

- Việc sử dụng kết hợp tuyến tính không phải lúc nào cũng là giải pháp tốt, đặc biệt khi các phương pháp tìm kiếm không thể phân tách tài liệu liên quan và không liên quan một cách rõ ràng.
- Tuy nhiên, có các phương pháp khác như **reranking**, **fusion phức tạp**, và **mô hình học sâu** có thể giúp giải quyết vấn đề này và cải thiện hiệu quả tìm kiếm.

------------ 
## More:
- ![](../../assets/images/Pasted%20image%2020241210181614.png)
- - **Bi-encoder:** Phương pháp này sẽ sử dụng một mô hình embedding vector để embedding Query và Document chunks (cái này đã được lưu trước đó vào vector database rồi). Sau đó sử dụng một số phép tính độ tương đồng giữa hai vector như _**cosine similarity**_, _**euclidean distance**_ hay _**Jaccard similarity**_ để tính toán độ tương đồng giữa Query và Document chunks. Sau đó lấy ra top K documents có similarity score cao nhất.
- **Cross-encoder:** Đối với Cross-encoder thì nó có một ưu điểm là mang lại độ chính xác tốt hơn Bi-encoder, thế nhưng nó lại có một nhược điểm là chạy chậm hơn. Vậy nên, thông thường người ta hay sử dụng Cross-encoder như một bước re-rank lại relevant documents sau khi lấy ra được từ bước Bi-encoder. Về cách hoạt động thì nó thực hiện ghép nối Query và Document lại với nhau, sau đó cho qua một Encoder model, từ đó có thể tận dụng được phép tính self-attention nhờ đó khiến cho mô hình mang lại độ chính xác rất cao. Đầu ra của mô hình là một candidate embedding tương ứng. Sau đó embedding sẽ được đi qua một head classifier cho ra score 0->1.



# Ground truth

- Link : [BeIR/scifact](https://huggingface.co/datasets/BeIR/scifact)
- [BeIR/scifact-qrels](https://huggingface.co/datasets/BeIR/scifact-qrels)
- [code Hybrid search](https://github.com/qdrant/workshop-ultimate-hybrid-search/blob/main/notebooks/02-hybrid-search.ipynb)


- Hiếu :
- https://huggingface.co/datasets/hiieu/legal_eval/viewer/default/corpus
- https://huggingface.co/datasets/hiieu/legal_eval_label
	- ở đây ảnh nói về Data để check. 

![](../../assets/images/Pasted%20image%2020241211204529.png)

![](../../assets/images/Pasted%20image%2020241211222034.png)
![](../../assets/images/Pasted%20image%2020241211222102.png)


![](../../assets/images/Pasted%20image%2020241212150010.png)
corpus
![](../../assets/images/Pasted%20image%2020241212150041.png)

queries
![](../../assets/images/Pasted%20image%2020241212150106.png)

label query và courpu
![](../../assets/images/Pasted%20image%2020241212150654.png)