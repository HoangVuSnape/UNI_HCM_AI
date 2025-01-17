
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv(Path("./.env"))

genai.configure(api_key= os.getenv("GG_API"))

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    
    datasource: Literal["vectorstore", "web_search"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )
class UniversityCode(BaseModel):
    """Route a query to the corresponding university code."""
    
    university_code: Literal[
        "NTTU", "HCMUE", "UPM", "HCMUTE", "VLU", 
        "PNTU", "FTU2", "TDTU", "UEH", "FPTU",
        "BKU", "HCMUS", "OU", "UIT", "UFM"
    ] = Field(
        ...,
        description="University code corresponding to the query"
    )
class QueryRouter:
     def __init__(self, llm= None):
          self.llm = llm or ChatGoogleGenerativeAI(
                              model="gemini-1.5-flash-8b",
                              temperature=0
                              )

          self.route_prompt = PromptTemplate(
                    input_variables=["query"],
                    template= """Dựa vào truy vấn(câu hỏi) từ người dùng: {query}
                    Hãy phân thuộc dạng truy vấn vào: vectorstore hay web search.
                    Vectorstore bao gồm tất cả các thông tin liên quan đến tất cả các vấn đề tuyển sinh của các trường đại học tại Việt Nam: bao gồm điểm chuẩn qua các năm, học phí, thông tin trường đại học, thông tin ngành, ...
                    Nếu nội dung câu truy vấn của người dùng liên quan đến các vấn đề trên thì phần loại là vectorstore, còn lại là websearch """
          )
          self.knowledge_prompt = PromptTemplate(
               input_variables=["query"],
               template="""Phân loại truy vấn thuộc về trường nào trong 6 trường sau:
               1.Trường đại học Nguyễn Tất Thành -> NTTU
               2.Trường đại học Sư Phạm TP HCM -> HCMUE
               3.Trường đại học Y Dược TP HCM -> UPM
               4.Trường đại học Tài Chính - Marketing -> UFM
               5.Trường đại học Văn Lang -> VLU
               6.Trường đại học Y Khoa Phạm Ngọc Thạch -> PNTU
               7. Trường đại học Sư Phạm Kỹ Thuật TP HCM -> HCMUTE
               8. Trường đại học Ngoại Thương TP HCM -> FTU2
               9. Trường đại học Tôn Đức Thắng -> TDTU
               10. Trường đại học Kinh Tế TP HCM -> UEH
               11. Trường đại học FPT -> FPTU
               12. Trường đại học Bách Khoa TP HCM -> BKU
               13. Trường đại học Khoa Học Tự Nhiên TP HCM -> HCMUS
               14. Trường đại học Mở TP HCM -> OU
               15. Trường đại học Công Nghệ Thông Tin TP HCM -> UIT
               Query: {query}
               Chỉ in ra tên trường đã được phân loại:
               ví dụ: VLU
               """
          )

     def classify(self, query):
          print("Phân loại truy vấn")
          structured_llm_router = self.llm.with_structured_output(RouteQuery)
          question_router = self.route_prompt | structured_llm_router
          response = question_router.invoke(query)
          return response
     
     def UniversityRouting(self, query):
          structured_llm_router = self.llm.with_structured_output(UniversityCode)
          question_router = self.knowledge_prompt | structured_llm_router
          response = question_router.invoke(query)
          return response

    
# classifier = QueryRouter()
# source = classifier.classify("Chỉ tiêu tuyển sinh đại học Nguyễn Tất Thành 2022?")
# print((source.datasource))
#print(classifier.UniversityRouting({"query": "Thông tin trường Ngoai Thuong"}).university_code)
