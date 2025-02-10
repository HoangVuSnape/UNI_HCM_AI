from typing import List
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class QueryTransformation:
    def __init__(self, llm=None):
        self.llm = llm or ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
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

    def transformAll(self, query: str) -> List[str]:
        sub_queries_list = []
        llm_chain = self.transformed_prompt | self.llm
        response = llm_chain.invoke({"query": query}).content

        sub_queries_list = response.split("\n")
        clean_sub_queries_list = [query for query in sub_queries_list if query]
        clean_sub_queries_list = clean_sub_queries_list
        print(f"Truy vấn đã được phân rã new:\n{clean_sub_queries_list}")
        return clean_sub_queries_list

if __name__ == "__main__":   
    # env_loader = EnvLoader()
    # env_loader.load_all()
    
    transformation = QueryTransformation()
    input1 = {"query": "Đại học Tôn Đức Thắng 2021"}
    input2 = {"query": "So sánh ngành CNTT giữa VLU và TDTU"}
    enhance = transformation.enhancing_query(input1)
    decompose = transformation.decomposition_query(input2)
    
    t = transformation.transformAll(input2)

