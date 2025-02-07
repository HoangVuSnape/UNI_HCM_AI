Test 1 : tdtu
- navie rag.
- ![](../assets/images/Pasted%20image%2020250204162935.png)
- Hybrid search
- ![](../assets/images/Pasted%20image%2020250204191235.png)

![](../assets/images/Pasted%20image%2020250205153606.png)


Có mấy vấn đề liên quan đến data ground truth.
Mình đang cảm thấy data tự động sinh ra là không ổn chút nào
- Data câu hỏi liên quan nhưng chắc gì thực tế hỏi sâu như vậy
- data bị nhiễu nên bộ test không ổn lắm

Mình phải tạo ra 1 bộ data test bằng tay để kiểm tra
- Những câu hỏi liên quan đến trường: Học phí, phương thức tuyển sinh, văn phòng...
- Những gì mà core của trường mà các trang web thường không có. 
	- Gộp lại thử và viết thêm báo cáo. 

![](../assets/images/Pasted%20image%2020250206184227.png)

## K = 3
- ![](../assets/images/Pasted%20image%2020250206231328.png)

![](../assets/images/Pasted%20image%2020250207140931.png)

# RAGAS
- ![](../assets/images/Pasted%20image%2020250206231239.png)


![](../assets/images/Pasted%20image%2020250206234920.png)
![](../assets/images/Pasted%20image%2020250206234939.png)
![](../assets/images/Pasted%20image%2020250207095543.png)

## Note
- mình thấy rằng mình mà tạo ra data với từng đó corpus thì tốn nhiều thời gian. Vì vậy mình sẽ tạo ra bộ câu hỏi khái quát được hệ thống của mình 
	- Như trường địa chỉ,
	- So sánh các trường : Câu hỏi 1 trường 2 trường
	- Câu hỏi phức tạp. nhiều thông tin. 

- Từ đó mình cần tạo gì trước
	- Bộ câu hỏi mong muốn
	- Tạo ra data hay là câu trả lời mong muốn chính là cột ground truth
	- Context hay là answer mình phải làm lại. Chứ k tự sinh ra đc
	- Mình nghĩ mình tạo không nên quá ít sample để test evaluation tự động - tại vì nêu ít quá k phải ánh đc gì 
	- Human evaluate thì nó có thể ít hơn để đánh giá kĩ hơn. 
- Chia ra các cấp bậc về câu hỏi để tổng quát được cả hệ thống chứ k phải sơ xài
	- Test câu 1 ý, 2 ý
	- Câu phức tập đơn giản
	- SQL
	- Câu về 