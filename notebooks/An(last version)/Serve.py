from QueryTransformation import QueryTransformation
from Retrieval import UniversityRetrievalStrategy
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Set, Dict
from pydantic import BaseModel, Field
from langchain.schema import Document
import os
from langchain_groq import ChatGroq
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv(Path("./.env"), override= True)

class AdmissionResponse(BaseModel):
    answer: str = Field(description="Câu trả lời chi tiết cho câu hỏi", example="Trường ĐH Sư Phạm TPHCM có điểm chuẩn ngành Toán là 24.5")

class Serve:
     def __init__(self, llm = None):
          self.llm = llm or ChatGroq(
               model= "gemma2-9b-it",
               temperature= 0.1,
               api_key= os.getenv("groq_api_key"),
          )
          self.transformation = QueryTransformation()
          self.retriever = UniversityRetrievalStrategy()
          self.prompt = ChatPromptTemplate.from_messages([
          ("system", """ Bạn là một mô hình AI chuyên trả lời câu hỏi về tuyển sinh đại học tại Việt Nam. Nhiệm vụ của bạn là:
          Nhận đầu vào từ người dùng, bao gồm:
          Truy vấn: Câu hỏi hoặc yêu cầu cần trả lời.
          Ngữ cảnh: Dữ liệu do người dùng cung cấp, có thể chứa thông tin về tuyển sinh, học phí, đào tạo, phương thức xét tuyển, v.v.
          Quy tắc trả lời:

          Nếu ngữ cảnh cung cấp đủ thông tin để trả lời truy vấn, hãy đưa ra câu trả lời chính xác, ngắn gọn và đầy đủ dựa trên ngữ cảnh đó. Không bịa ra câu trả lời
          Định dạng đầu ra:

          Câu trả lời trực tiếp, không lan man.
          Chỉ dựa vào thông tin có sẵn trong ngữ cảnh.
          """),

          ("user", """Dựa vào truy vấn và ngữ cảnh được cung cấp sau đây hãy trả lời câu truy vấn(câu hỏi) một cách chính xác, trực tiếp và bao quát hết nội dung dựa vào ngữ cảnh đã cho. Không bịa ra câu trả lời
          Truy vấn: {query}
          Ngữ cảnh:
          {context}
          
          """)
          ])
     def format_docs(self, docs: List[Document]) -> str:
          return "\n\n".join([f"Nguồn {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

     def __call__(self, query, docs : List[Document]) -> AdmissionResponse:
          docs = self._remove_duplicates(docs)
          context = self.format_docs(docs)
          answer_chain = self.prompt | self.llm | StrOutputParser()
          answer = answer_chain.invoke({
               "context": context,
               "query": query
          })
          
          return AdmissionResponse(answer=answer)
     
     def run(self, query, docs : List[Document]) -> AdmissionResponse:
          context = "\n\n".join([f"Nguồn {i+1}:\n{doc}" for i, doc in enumerate(docs)])
          answer_chain = self.prompt | self.llm | StrOutputParser()
          answer = answer_chain.invoke({
               "context": context,
               "query": query
          })
          
          return AdmissionResponse(answer=answer)
     
     def _remove_duplicates(self, documents: List[Document]) -> List[Document]:
          seen_contents: Set[str] = set()
          unique_docs: List[Document] = []
          
          for doc in documents:
               # Normalize content for comparison
               normalized_content = self._normalize_content(doc.page_content)
               
               if normalized_content not in seen_contents:
                    seen_contents.add(normalized_content)
                    unique_docs.append(doc)
                    
          return unique_docs
     
     def _normalize_content(self, content: str) -> str:
        """
        Normalize document content for deduplication
        
        Args:
            content (str): Document content
            
        Returns:
            str: Normalized content
        """
        # Basic normalization: lowercase and remove extra whitespace
        return ' '.join(content.lower().split())