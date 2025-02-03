from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from retrieval import UniversityRetrievalStrategy
from serve import Serve # test

class RetrievalGrader:
    def __init__(self):
          self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
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
        docs_text = "\n".join([doc.page_content for doc in documents])
        evaluation = self.llm.invoke(self.prompt.format(
            query=query,
            documents=docs_text
        ))
        
        # Return structured scores
        return evaluation.content


class AnswerGrader:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Bạn là chuyên gia trong việc đánh giá chất lượng câu trả lời cho các câu hỏi về tuyển sinh đại học."),
            ("user", """Hãy đánh giá mức độ mà câu trả lời đã giải quyết đầy đủ và chính xác câu hỏi được đặt ra, dựa trên mức độ phù hợp, đầy đủ thông tin và sự rõ ràng. Chỉ trả về điểm số, không giải thích
                Thang điểm đánh giá (0-5):
                0: Hoàn toàn không trả lời đúng trọng tâm câu hỏi, lạc đề hoặc bỏ qua hoàn toàn ý chính.
                1: Chỉ đề cập một phần nhỏ nội dung liên quan, chưa đủ để giải quyết câu hỏi.
                2: Câu trả lời có một số ý phù hợp nhưng thiếu các yếu tố quan trọng để giải quyết câu hỏi.
                3: Câu trả lời tương đối đầy đủ nhưng vẫn còn thiếu một số chi tiết quan trọng.
                4: Câu trả lời gần như đầy đủ, chỉ thiếu một vài chi tiết nhỏ hoặc cần giải thích rõ ràng hơn.
                5: Câu trả lời hoàn toàn đầy đủ, chính xác và rõ ràng, giải quyết toàn diện câu hỏi.
             
                Yêu cầu chi tiết:
                Đánh giá mức độ đầy đủ: Câu trả lời đã bao quát hết các khía cạnh của câu hỏi chưa?
                Tính chính xác: Các thông tin có đúng và phù hợp với câu hỏi không?
                Sự liên quan: Nội dung có trực tiếp giải quyết trọng tâm câu hỏi không?
            
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
    
    
if __name__ == "__main__":

    grader = RetrievalGrader()
    retriver = UniversityRetrievalStrategy()
    serve = Serve()
    query = "Tuyển sinh đại học Tôn Đức Thắng 2023"
    docs = retriver.retrieve("Tuyển sinh đại học Tôn Đức Thắng 2023")
    answer = serve.__call__(query, docs)
    
    print(grader.grade(query, docs))