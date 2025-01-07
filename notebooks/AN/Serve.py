from QueryTransformation import QueryTransformation
from Retrieval import UniversityRetrievalStrategy
from langchain_core.prompts import ChatPromptTemplate
import google.generativeai as genai
from typing import List, Set, Dict
from pydantic import BaseModel, Field
from langchain.schema import Document
import os
from langchain_groq import ChatGroq
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv(Path("./.env"))

genai.configure(api_key= os.getenv("Google_API_KEY"))

class AdmissionResponse(BaseModel):
    answer: str = Field(description="Câu trả lời chi tiết cho câu hỏi", example="Trường ĐH Sư Phạm TPHCM có điểm chuẩn ngành Toán là 24.5")

class Serve:
     def __init__(self, llm = None):
          self.llm = llm or ChatGroq(
               model= "llama-3.3-70b-versatile",
               temperature= 0.1
          )
          self.transformation = QueryTransformation()
          self.retriever = UniversityRetrievalStrategy()
          self.prompt = ChatPromptTemplate.from_messages([
          ("system", """ Bạn là trợ lý hiểu biết được giao nhiệm vụ cung cấp câu trả lời chính xác và ngắn gọn dựa trên thông tin được cung cấp. Nếu câu trả lời không nằm trong ngữ cảnh đã cho, hãy trả lời "Tôi không biết" thay vì bịa ra câu trả lời.
          Yêu cầu:
          1. Trả lời dựa trên thông tin trong ngữ cảnh
          2. Tổng hợp thông tin từ nhiều nguồn nếu có
          3. Trả lời rõ ràng, mạch lạc
          4. Nêu rõ nếu thông tin trong ngữ cảnh không đủ để trả lời
          Ngữ cảnh:
          {context}
          user.user
          {question} """)
          ])
     def format_docs(self, docs: List[Document]) -> str:
          return "\n\n".join([f"Nguồn {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

     def __call__(self, query) -> AdmissionResponse:
          enhanced_query = self.transformation.enhancing_query(query)
          decomposed_query = self.transformation.decomposition_query(enhanced_query)
          all_docs = []
          for sub_query in decomposed_query:
               docs = self.retriever.retrieve(sub_query)
               all_docs.extend(docs)
          all_docs = self._remove_duplicates(all_docs)
          context = self.format_docs(all_docs)

          #Generate answer
          answer_chain = self.prompt | self.llm | StrOutputParser()
          answer = answer_chain.invoke({
               "context": context,
               "question": enhanced_query
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

# serve = Serve()
# print(serve.retriever.retrieve(serve.transformation.enhancing_query("Đại học Tôn Đức Thắng 2021")))