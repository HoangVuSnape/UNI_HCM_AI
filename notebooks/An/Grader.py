from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from Serve import Serve
from Retrieval import UniversityRetrievalStrategy

class RetrievalGrader:
    def __init__(self):
          self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0)
          self.prompt = ChatPromptTemplate.from_messages([
               ("system", "Bạn là chuyên gia trong việc đánh giá chất lượng tìm kiếm tài liệu."),
               ("user", """Chấm điểm độ liên quan giữa tài liệu thu thập được với câu truy vấn, liệu tài liệu thu thập được có liên quan đến câu truy vấn. Chỉ đưa ra điểm số (0-10) để chỉ mức độ liên quan giữa tài liệu và truy vấn. Không giải thích thêm
               
               Truy vấn: {query}
               
               Tài liệu:
               {documents}
               
               """)
          ])

    def grade(self, query: str, documents: List[Document]) -> int:
        docs_text = "\n".join([f"Doc {i+1}:\n{doc.page_content}" for i, doc in enumerate(documents)])
        evaluation = self.llm.invoke(self.prompt.format(
            query=query,
            documents=docs_text
        ))
        
        # Return structured scores
        return int(evaluation.content)

class HallucinationGrader:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Bạn là chuyên gia trong việc phát hiện liệu rằng AI có đang tự bịa ra câu trả lời hay không"),
            ("user", """Phân tích xem câu trả lời này có được hỗ trợ đầy đủ bởi các tài liệu được cung cấp hay không. Chỉ đưa ra điểm nhị phân 'yes' hoặc 'no' để chỉ ra liệu câu trả lời có dựa trên / được hỗ trợ bởi một tập hợp các sự kiện hay không. Không giải thích thêm
            
            Truy vấn: {query}
            Trả lời: {answer}
            Tài liệu hỗ trợ:
            {documents}
            
            """)
        ])

    def grade(self, query: str, answer: str, documents: List[Document]) -> str:
        docs_text = "\n".join([f"Doc {i+1}:\n{doc.page_content}" for i, doc in enumerate(documents)])
        evaluation = self.llm.invoke(self.prompt.format(
            query=query,
            answer=answer,
            documents=docs_text
        ))
        
        return evaluation.content

class AnswerGrader:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Bạn là chuyên gia trong việc đánh giá chất lượng câu trả lời cho các câu hỏi về tuyển sinh đại học."),
            ("user", """Đánh giá câu trả lời này cho truy vấn đã cho, Chỉ đưa ra điểm nhị phân 'yes' hoặc 'no' để chỉ ra liệu câu trả lời có hữu ích để giải quyết câu hỏi hay không. Không giải thích thêm
            
            Truy vấn: {query}
            Câu trả lời: {answer}
            
            """)
        ])

    def grade(self, query: str, answer: str) -> str:
        evaluation = self.llm.invoke(self.prompt.format(
            query=query,
            answer=answer
        ))
        
        return evaluation.content
    
# serve = Serve()
# grader = AnswerGrader()
# retriver = UniversityRetrievalStrategy()
# query = "Tuyển sinh đại học Tôn Đức Thắng 2023"
# docs = retriver.retrieve("Tuyển sinh đại học Tôn Đức Thắng 2023")
# answer = serve.__call__(query, docs)

# print(grader.grade(query, answer))