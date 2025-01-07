from typing import List
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from pathlib import Path
import os
import json

from dotenv import load_dotenv
load_dotenv(Path("./.env"))
genai.configure(api_key=os.getenv("Google_API_KEY"))

class QueryTransformation:
    def __init__(self, llm=None):
        self.llm = llm or ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-8b",
            temperature=0
        )

        # Chat prompt for enhancing
        self.enhanced_prompt = ChatPromptTemplate.from_messages([
            ("system", "Bạn là trợ lý tối ưu hóa truy vấn giúp cải thiện các truy vấn để có thể truy xuất được nhiều hơn các thông tin liên quan các vấn đề tuyển sinh hơn từ vectorstore."),
            ("user", """Hãy tối ưu câu truy vấn sau để có thể truy xuất được nhiều thông tin liên quan nhất đến tất cả các vấn đề tuyển sinh từ vectorstore. 
            Truy vấn gốc: {query}
            Chỉ trả về truy vấn đã được cải thiện, không giải thích.""")
        ])

        # Chat prompt for decomposing
        self.decomposition_prompt = ChatPromptTemplate.from_messages([
            ("system", "Bạn là trợ lý phân tích truy vấn, giúp chia nhỏ các truy vấn phức tạp thành các truy vấn phụ đơn giản và độc lập hơn."),
            ("user", """Phân tích truy vấn sau có phải lại một câu truy vấn phức tạp, có liền qua đến nhiều khía cạnh, nhiều trường và nhiều vấn đề không. Nếu có hãy phân tách câu truy vấn thành 4 truy vấn con nhỏ hơn, độc lập. Nếu không, hãy viết lại câu truy vấn sao cho truy xuất được nhiều thông tin có liên 
            Truy vấn gốc: {query}
            
            Yêu cầu:
            1. Mỗi truy vấn con tập trung vào một khía cạnh cụ thể
            2. Các truy vấn con phải độc lập và có ý nghĩa
            
            Lưu ý: chỉ trả về dưới dạng từng câu hỏi sau khi phân rả, không in ra truy vấn ban đầu
            Ví dụ:
            Truy vấn: So sánh ngành công nghệ thông tin giữa NTTU và VLU

            Ngành công nghệ thông tin tại NTTU
            Ngành công nghệ thông tin tại VLU
            Cơ sở vật chất, học phí tại NTTU
            Cơ sở vật chất, học phó tại VLU""")
        ])
    
    def enhancing_query(self, query: str) -> str:
        llm_chain = self.enhanced_prompt | self.llm
        response = llm_chain.invoke({"query": query}).content
        print(f"Truy vẫn đã được cải thiện: {response}")
        
        return response
    
    def decomposition_query(self, query: str) -> List[str]:
        sub_queries_list = []
        llm_chain = self.decomposition_prompt | self.llm
        response = llm_chain.invoke({"query": query}).content

        sub_queries_list = response.split("\n")
        clean_sub_queries_list = [query for query in sub_queries_list if query]
        clean_sub_queries_list = clean_sub_queries_list
        print(f"Truy vấn đã được phân rã:\n{clean_sub_queries_list}")
        return clean_sub_queries_list
    
    def transform(self, query):
        return self.decomposition_query(self.enhancing_query(query))
# transformation = QueryTransformation()
# enhance = transformation.enhancing_query({"query": "Đại học Tôn Đức Thắng 2021"})
# decompose = transformation.decomposition_query({"query": "So sánh ngành CNTT giữa VLU và TDTU"})

