Kỹ thuật hay thầy là khi prompt thì nó sẽ gọi api để lấy tạo ra câu prompt hoàn chinh để lấy ra đc cái retrival ưng ý. 
# RAG Advance
Link: 
[RAG của bạn tiến và đoàn](https://www.youtube.com/watch?v=OHFGDn_tJwA): Ở đây là link youtube bạn đó làm 1 dự án thực tế bạn có giải thích kĩ ra về các bước rag. Vì dự án của công ty nên không có show code. Nhưng mình biết rõ được các flow chạy. 
Hoặc ở trong đây :
[Advance RAG- Hơi Non](https://atekco.io/1713861441749-toan-canh-cac-ky-thuat-advanced-rag/): Đây là bài blog cũng nói đến chủ đề này,

https://arxiv.org/pdf/2312.10997
https://arxiv.org/pdf/2410.03780
## Link tham khảo

https://medium.com/ai-advances/advanced-rag-techniques-unlocking-the-next-level-040c205b95bc
https://pub.towardsai.net/advanced-rag-techniques-an-illustrated-overview-04d193d8fec6
https://towardsdatascience.com/advanced-retrieval-augmented-generation-from-theory-to-llamaindex-implementation-4de1464a9930
https://arxiv.org/pdf/2404.01037
https://github.com/ianhojy/auto-hyde/tree/main
https://medium.com/m/global-identity-2?redirectUrl=https%3A%2F%2F 
towardsdatascience.com/2Fautohyde-making-hyde-better-for-advanced-1lm-rag-619e58cdbd8e

### Link langchain 

Advance RAG Th.Cuong: https://www.purpleslate.com/the-ultimate-guide-to-understanding-advanced-retrieval-augmented-generation-methodologies/ 
https://www.anthropic.com/news/contextual-retrieval
https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb
RAG 
- LangChain: https://python.langchain.com/docs/introduction/
  - Agents: https://python.langchain.com/docs/tutorials/qa_chat_history/#tying-it-together-1
  - BM25: https://python.langchain.com/docs/integrations/retrievers/bm25/#create-a-new-retriever-with-documents
  - How to combine results from multiple retrievers: https://python.langchain.com/docs/how_to/ensemble_retriever/
  - Langchain Milvus: https://python.langchain.com/docs/integrations/vectorstores/milvus/#initialization
  - Recursive URL: https://python.langchain.com/docs/integrations/document_loaders/recursive_url/#overview
  - Langchain Streamlit: https://python.langchain.com/docs/integrations/callbacks/streamlit/#installation-and-setup
  - Langchain Streamlit: https://python.langchain.com/docs/integrations/providers/streamlit/#memory
- Milvus Standalone: https://milvus.io/docs/v2.0.x/install_standalone-docker.md
  - Attu: https://github.com/zilliztech/attu
- Streamlit Documentation: https://docs.streamlit.io/
- OpenAI API: https://platform.openai.com/docs
## I. Giới thiệu về RAG

1. Tổng quan về RAG

Những hạn chế của LLMs: Các LLM chỉ có thể trả lời tốt ở các câu hỏi mà chúng ra được học trước đó. Còn đối với những câu hỏi mới (dữ liệu mới) chưa được học thì nó sẽ bị vấn đề là hallucination.

- Retrieval-Augmented Generation (RAG) là một kỹ thuật giúp nâng cao khả năng của mô hình sinh (language model generation) kết hợp với tri thức bên ngoài (external knowledge).

- Phương pháp này thực hiện bằng cách truy xuất thông tin liên quan từ kho tài liệu (tri thức) và sử dụng chúng cho quá trình sinh câu trả lời dựa trên LLMs.
![](../../assets/images/Pasted%20image%2020241125162517.png)
## Kiến trúc 
![](../../assets/images/Pasted%20image%2020241125162726.png)
Trong ảnh và video có nói
Pre-retrieval
- query routing: điều hướng đến 
- Query filtering, query expanasion
Post-retrieval
- Fusion: 1 query ban đầu sẽ chia nhỏ hơn để retrieval -  nó không năm ở post-retrieval mà nằm ở retriveval . có thể xem ở link atekco.io. 
- ![](../../assets/images/Pasted%20image%2020241125171441.png)

![](../../assets/images/Pasted%20image%2020241125163732.png)


## 1. Load PDF
### Indexing 
![](../../assets/images/Pasted%20image%2020241125163937.png)

![](../../assets/images/Pasted%20image%2020241125164238.png)
![](../../assets/images/Pasted%20image%2020241125164323.png)
![](../../assets/images/Pasted%20image%2020241125164816.png)
### Chunk optimization
![](../../assets/images/Pasted%20image%2020241125164447.png)
![](../../assets/images/Pasted%20image%2020241125164523.png)
![](../../assets/images/Pasted%20image%2020241125164710.png)
![](../../assets/images/Pasted%20image%2020241125164730.png)



### Embedding model
![](../../assets/images/Pasted%20image%2020241125165041.png)
#### Vector store 
![](../../assets/images/Pasted%20image%2020241125165117.png)
## 2. Query transformation and Query routing 
![](../../assets/images/Pasted%20image%2020241125170938.png)

![](../../assets/images/Pasted%20image%2020241125165511.png)
![](../../assets/images/Pasted%20image%2020241125170017.png)

## 3. Retrieval 


## 4. Evaluate
https://docs.llamaindex.ai/en/stable/examples/evaluation/RAGChecker/
![](../../assets/images/Pasted%20image%2020241128232729.png)
### **Các tiêu chí đánh giá chất lượng câu phản hồi**

1. **Context Relevance**
    
    - **Giải thích**: Đảm bảo câu phản hồi sử dụng đúng ngữ cảnh liên quan, không lấy thông tin không cần thiết.
    - **Ví dụ**:
        - **Câu hỏi**: "TDTU nằm ở đâu?"
        - **Phản hồi tốt**: "TDTU nằm tại TP.HCM."
        - **Phản hồi kém**: "TP.HCM là một thành phố lớn, TDTU là một trường đại học tốt."
2. **Answer Faithfulness**
    
    - **Giải thích**: Phản hồi phải đúng với ngữ cảnh được cung cấp, không được sáng tạo thông tin sai.
    - **Ví dụ**:
        - **Ngữ cảnh**: "TDTU có 4 cơ sở tại Việt Nam."
        - **Phản hồi tốt**: "TDTU có 4 cơ sở."
        - **Phản hồi kém**: "TDTU có 5 cơ sở trên toàn quốc."
3. **Answer Relevance**
    
    - **Giải thích**: Câu trả lời phải liên quan trực tiếp đến câu hỏi, không lan man.
    - **Ví dụ**:
        - **Câu hỏi**: "Khoa Công nghệ Thông tin TDTU đào tạo ngành nào?"
        - **Phản hồi tốt**: "Khoa CNTT TDTU đào tạo ngành Khoa học Máy tính, Trí tuệ Nhân tạo."
        - **Phản hồi kém**: "TDTU là một trường đại học uy tín."

---

### **Các tiêu chí đánh giá khả năng của hệ thống**

1. **Noise Robustness**
    
    - **Giải thích**: Hệ thống không bị rối bởi thông tin nhiễu hoặc không cần thiết.
    - **Ví dụ**:
        - **Tài liệu**: "TDTU thành lập năm 1997. Có 4 cơ sở. Trường này nằm gần quán cà phê A."
        - **Phản hồi tốt**: "TDTU có 4 cơ sở."
        - **Phản hồi kém**: "TDTU nằm gần quán cà phê A."
2. **Negative Rejection**
    
    - **Giải thích**: Hệ thống không đưa ra phản hồi khi không có thông tin cần thiết.
    - **Ví dụ**:
        - **Câu hỏi**: "Giáo sư nào thành lập TDTU?"
        - **Phản hồi tốt**: "Xin lỗi, tôi không có thông tin về câu hỏi này."
        - **Phản hồi kém**: "TDTU được thành lập bởi Giáo sư X."
3. **Information Integration**
    
    - **Giải thích**: Hệ thống tổng hợp thông tin từ nhiều nguồn để trả lời các câu hỏi phức tạp.
    - **Ví dụ**:
        - **Câu hỏi**: "TDTU đào tạo bao nhiêu ngành và có bao nhiêu cơ sở?"
        - **Phản hồi tốt**: "TDTU đào tạo hơn 40 ngành và có 4 cơ sở."
        - **Phản hồi kém**: "TDTU đào tạo nhiều ngành. TDTU có cơ sở tại TP.HCM."
4. **Counterfactual Robustness**
    
    - **Giải thích**: Nhận biết và bỏ qua thông tin sai lệch, không sử dụng chúng trong phản hồi.
    - **Ví dụ**:
        - **Tài liệu**: "TDTU nằm ở TP.HCM. TDTU là một trường tiểu học."
        - **Phản hồi tốt**: "TDTU nằm ở TP.HCM."
        - **Phản hồi kém**: "TDTU là một trường tiểu học ở TP.HCM."

## RAGChecker Metrics
link: 
- https://github.com/amazon-science/RAGChecker
- https://docs.llamaindex.ai/en/stable/examples/evaluation/RAGChecker/
- https://docs.llamaindex.ai/en/stable/examples/evaluation/pairwise_eval/
RAGChecker provides a comprehensive set of metrics to evaluate different aspects of RAG systems:

1. Overall Metrics:
    
    - Precision: The proportion of correct claims in the model's response.
    - Recall: The proportion of ground truth claims covered by the model's response.
    - F1 Score: The harmonic mean of precision and recall.
2. Retriever Metrics:
    
    - Claim Recall: The proportion of ground truth claims covered by the retrieved chunks.
    - Context Precision: The proportion of retrieved chunks that are relevant.
3. Generator Metrics:
    
    - Context Utilization: How well the generator uses relevant information from retrieved chunks.
    - Noise Sensitivity: The generator's tendency to include incorrect information from retrieved chunks.
    - Hallucination: The proportion of incorrect claims not found in any retrieved chunks.
    - Self-knowledge: The proportion of correct claims not found in any retrieved chunks.
    - Faithfulness: How closely the generator's response aligns with the retrieved chunks.

These metrics provide a nuanced evaluation of both the retrieval and generation components, allowing for targeted improvements in RAG systems.

![](../../assets/images/Pasted%20image%2020241128233542.png)
![](../../assets/images/Pasted%20image%2020241128234558.png)
# Thắc mắc về sự kết hợp hợp RAG và RLHF
- Hiện tại mình chỉ thấy trên youtube hay nhiều nguồn có sử dụng RAG chứ k thấy họ thêm RLHF. Nên hơi lấn cấn về lấy data của RLHF.


# More RAG
Link paper: [R2GQA: Retriever-Reader-Generator Question Answering System to Support Students Understanding Legal Regulations in Higher Education](https://arxiv.org/pdf/2409.02840)


- ![](../../assets/images/Pasted%20image%2020241129160920.png)
- Bài paper còn có phân tích về error để 
- Cái thứ 2 là họ dung BM25 và kĩ thuật chunking để tắc hiểu quả truy xuất dữ liệu hay nha. Mình cần nghiên cứu cái này. 