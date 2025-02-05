from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path("./.env"), override= True)

class RetrievalGrader:
    def __init__(self):
          self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1, api_key= os.getenv("GG_API2"))
          self.prompt = ChatPromptTemplate.from_messages([
               ("system", "Bạn là chuyên gia trong việc đánh giá chất lượng tìm kiếm tài liệu."),
               ("user", """Hãy đánh giá mức độ liên quan giữa câu truy vấn và các tài liệu được cung cấp .Chỉ trả về điểm số, không giải thích.
                    0: Hoàn toàn không liên quan
                    1: Rất ít liên quan, chỉ có một số từ khóa chung chung
                    2: Mối liên quan yếu, một số ý chính trùng khớp nhưng không đầy đủ
                    3: Mối liên quan vừa phải, tài liệu đề cập đến chủ đề nhưng thiếu chi tiết quan trọng
                    4: Mối liên quan cao, tài liệu bao quát hầu hết các ý chính của câu truy vấn
                    5: Hoàn toàn liên quan, tài liệu phản ánh đầy đủ và chính xác toàn bộ nội dung câu truy vấn
                    Yêu cầu chi tiết:
                    Phân tích ý nghĩa và nội dung chính của câu truy vấn.
                    So sánh ý chính và mức độ bao quát của tài liệu với nội dung của câu truy vấn.
                    Đưa ra lý do ngắn gọn cho điểm số được đánh giá.
                    Chú ý đến ngữ cảnh, từ đồng nghĩa, cách diễn đạt khác nhưng cùng ý nghĩa.
                    Đảm bảo công bằng, không thiên vị dựa trên độ dài hoặc hình thức trình bày.
                Truy vấn: {query}
                Tài liệu:
                {documents}
                
               """)
          ])

    def grade(self, query: str, documents: List[Document]) -> int:
        evaluation = self.llm.invoke(self.prompt.format(
            query=query,
            documents=documents.page_content
        ))
        
        # Return structured scores
        return evaluation.content