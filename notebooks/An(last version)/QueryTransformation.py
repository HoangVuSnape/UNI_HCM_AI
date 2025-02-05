from typing import List
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from pathlib import Path
import os
import json
from dotenv import load_dotenv

load_dotenv(Path("./.env"), override= True)

class QueryTransformation:
    def __init__(self, llm=None):
        self.llm = llm or ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.1,
            api_key= os.getenv("GG_API2")
        )

        # Chat prompt for decomposing
        self.transformed_prompt = ChatPromptTemplate.from_messages([
            ("system", """Bạn là một mô hình xử lý ngôn ngữ có nhiệm vụ phân tích truy vấn từ người dùng liên quan đến tuyển sinh đại học ở Việt Nam. Khi nhận được truy vấn, bạn cần thực hiện một trong hai nhiệm vụ sau:
             
            Nếu truy vấn đơn giản (chỉ đề cập đến một vấn đề chính), bạn cần cải thiện câu truy vấn sao cho rõ ràng hơn và có thể truy xuất được nhiều thông tin liên quan hơn.
             
            Nếu truy vấn phức tạp (đề cập đến nhiều vấn đề, nhiều trường hoặc có nhiều yếu tố cần phân tích), bạn cần chia nhỏ truy vấn thành bốn câu truy vấn con, mỗi câu truy vấn con tập trung vào một vấn đề cụ thể và độc lập.
            Khi chia nhỏ, hãy đảm bảo rằng các truy vấn con bao phủ đầy đủ các khía cạnh quan trọng trong truy vấn ban đầu. Nếu không đủ để tách thành bốn phần, hãy chỉ tạo ra số lượng truy vấn con phù hợp."""),
            ("user", """
            Nhận diện loại truy vấn:

            Nếu truy vấn đơn giản (chỉ liên quan đến một vấn đề cụ thể), bạn chỉ cần cải thiện truy vấn sao cho rõ ràng, đầy đủ và có thể truy xuất được nhiều thông tin liên quan hơn.
             
            Nếu truy vấn phức tạp (liên quan đến nhiều vấn đề hoặc nhiều trường đại học), bạn cần chia nhỏ thành tối đa 4 truy vấn con, sao cho mỗi truy vấn con đề cập đến một khía cạnh độc lập của truy vấn ban đầu.
             
            Quy tắc phân tách truy vấn:
            Nếu truy vấn liên quan đến nhiều trường đại học, hãy tạo truy vấn con riêng biệt cho từng trường.
            Nếu truy vấn bao gồm nhiều yếu tố (ví dụ: học phí, đào tạo, tuyển sinh), hãy chia thành các truy vấn con theo từng yếu tố.
            Nếu có sự so sánh giữa hai hoặc nhiều trường, hãy tạo các truy vấn con để làm rõ thông tin của từng trường trước, sau đó mới đến truy vấn so sánh nếu cần.
             
            Định dạng đầu ra:
            Nếu là truy vấn đơn giản: chỉ cung cấp một truy vấn đã cải thiện không cần thêm bất kì nội dung gì.
            Nếu là truy vấn phức tạp: chỉ liệt kê tối đa 4 truy vấn con được chia nhỏ, đánh số a, b, c, d .
            Truy vấn gốc: {query}
            
            Ví dụ:

            Nhập: "ptts năm 2021 TDTU"
            Xuất: "Phương thức tuyển sinh đại học năm 2021 TDTU"

            Nhập: "So sánh học phí VLU và TDTU 2024"
            Xuất:
            a. Học phí VLU năm 2024
            b. Học phí TDTU năm 2024
            c. Mức tăng học phí năm 2024 của VLU
            d. Mức tăng học phí năm 2024 của TDTU
             
            Nhập: "UIT và HCMUS 2021"
            Xuất:
            a. Tuyển sinh UIT năm 2021
            b. Tuyển sinh HCMUS năm 2021
            c. Đào tạo UIT năm 2021
            d. Đào tạo HCMUS năm 2021
             
            Nhập: UIT và HCMUS 2021
            Xuất:
            a. Tuyển sinh UIT năm  2021
            b. Tuyển sinh HCMUS năm  2021""")
        ])
    
    def transform(self, query: str) -> List[str]:
        sub_queries_list = []
        llm_chain = self.transformed_prompt | self.llm
        response = llm_chain.invoke({"query": query}).content

        sub_queries_list = response.split("\n")
        clean_sub_queries_list = [query for query in sub_queries_list if query]
        clean_sub_queries_list = clean_sub_queries_list
        print(f"Truy vấn đã được phân rã:\n{clean_sub_queries_list}")
        return clean_sub_queries_list
    
if __name__ == "__main__":         
        
    transformation = QueryTransformation()
    decompose = transformation.transform({"query": "So sánh TDTU và VLU"})

