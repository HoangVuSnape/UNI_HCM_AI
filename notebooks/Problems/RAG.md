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




# Thắc mắc về sự kết hợp hợp RAG và RLHF
- Hiện tại mình chỉ thấy trên youtube hay nhiều nguồn có sử dụng RAG chứ k thấy họ thêm RLHF. Nên hơi lấn cấn về lấy data của RLHF.

