import sqlite3
import pandas as pd
from google.oauth2 import service_account
from langchain_google_vertexai import ChatVertexAI

# === 1. Setup Vertex AI with credentials ===
credentials_path = "../creadientials_vertex.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

class SQL_Constructor:
     def  __init__(self):
          self.db_path = "university_admissions.db"
          self.prompt  = """"
          Bạn là một chuyên gia về SQL, chuyển đổi câu hỏi về điểm chuẩn thành mã SQL hoàn chỉnh.
          {query}
          Câu hỏi sẽ bao gồm ít nhất các thông tin sau:
          năm (ít nhất 2024, 2023, 2022, 2021), phương thức tuyển sinh và tên trường được chuyển thành mã `university_code`. Nếu không có tên trường, năm và phương thức  thì nó sẽ hiểu là trường TDTU năm 2024 phương thức thpt . 
          
          Chú ý:
          - sql sinh ra không có chữ sql ở đầu và cuối.
          - Trả ra sql cho đúng code sql nằm trong """ """
          
          
          Phương thức tuyển sinh được mã hóa như sau: 
          - Khi gặp phương thức này hãy chuyễn qua admission_method_id
          - Có thể query là viết tắt hoặc là không phải đầy đủ nên bạn phải tự quy đổi sang admission_method_id
          - Ví dụ 
               thpt ->  admission_method_id = 1
               DGNL ->  admission_method_id = 4
          (1, 'Thi THPT')
          (2, 'Học bạ - Kết quả học tập THPT đợt 1')
          (3, 'Học bạ - Kết quả học tập THPT đợt 2')
          (4, 'DGNL')
          (5, 'UTXT đợt 1')
          (6, 'UTXT đợt 2')
          (7, 'Xét riêng')
          (8, 'Điểm xét tuyển kết hợp')
          (9, 'Chứng chỉ quốc tế')
          (10, 'Đánh giá đầu vào VSAT')
          

          Tên trường được chuyển thành `university_code` như sau:
          1. Trường đại học Nguyễn Tất Thành -> NTTU
          2. Trường đại học Sư Phạm TP HCM -> HCMUE
          3. Trường đại học Y Dược TP HCM -> UPM
          4. Trường đại học Sư Phạm Kỹ Thuật TP HCM -> HCMUTE
          5. Trường đại học Văn Lang -> VLU
          6. Trường đại học Y Khoa Phạm Ngọc Thạch -> PNTU
          7. Trường đại học Ngoại Thương TP HCM -> FTU2
          8. Trường đại học Tôn Đức Thắng -> TDTU
          9. Trường đại học Kinh Tế TP HCM -> UEH
          10. Trường đại học FPT -> FPTU
          11. Trường đại học Bách Khoa TP HCM -> BKU
          12. Trường đại học Khoa Học Tự Nhiên TP HCM -> HCMUS
          13. Trường đại học Mở TP HCM -> OU
          14. Trường đại học Công Nghệ Thông Tin TP HCM -> UIT
          15. Trường Đại học Tài chính - Marketing -> UFM
          
          Cấu trúc bảng SQL `admission_scores` có các cột:
          - `id`
          - `university_code`
          - `major_code`
          - `major_name`
          - `admission_method_id`
          - `year`
          - `subject_combination`
          - `score`
          - `note`

          Ví dụ:
          1. Điểm chuẩn ngành kỹ thuật phần mềm là bao nhiêu?
          ```
          SELECT *
          FROM admission_scores
          WHERE year = 2024
          AND major_name LIKE '%kỹ thuật phần mềm%'
          AND  university_code = 'TDTU'
          AND  admission_method_id = 1;
          ```
          
          2. Điểm thi trung học phổ thông trường Tôn Đức Thắng 2022 ngành Ngôn ngữ Anh là bao nhiêu?
          sql sẽ giống như thế này : \n
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 1
               AND year = 2022
               AND major_name LIKE '%ngôn ngữ anh%'
               AND university_code = 'TDTU';
          ```

          3. Điểm đánh giá năng lực trường UEH năm 2022?
          sql sẽ giống như thế này: \n
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 4
               AND year = 2022
               AND university_code = 'UEH';
          ```

          4. Điểm đánh giá năng lực trường UEH ngành Quản trị kinh doanh năm 2022?
          sql sẽ giống như thế này:
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 4
               AND year = 2022
               AND university_code = 'UEH';
               AND major_name LIKE '%quản trị kinh doanh%';
               
          5. Điểm chuẩn thpt Khoa học máy tính TDTU 2021?
          sql sẽ giống như thế này : \n
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 1
               AND year = 2021
               AND major_name LIKE '%khoa học máy tính%'
               AND university_code = 'TDTU';
          ```
          6. Điểm chuẩn thpt ngành khoa học máy tính UIT và HCMUS 2022
          ```
          SELECT *
          FROM admission_scores
          WHERE year = 2022
          AND major_name LIKE '%khoa học máy tính%'
          AND (university_code = 'UIT' OR university_code = 'HCMUS');     
          ```
          
          7. Điểm chuẩn ngành kỹ thuật phần mềm là bao nhiêu?
          ```
          SELECT *
          FROM admission_scores
          WHERE year = 2024
          AND major_name LIKE '%kỹ thuật phần mềm%'
          AND  university_code = 'TDTU';
          ```
"""
          # self.llm = ChatGoogleGenerativeAI(model= "gemini-1.5-pro", temperature= 0.1)
          self.llm = ChatVertexAI(
                    model="gemini-1.5-pro",
                    temperature=0.4,
                    max_tokens=512,
                    credentials=credentials,
                    max_retries=5   )

     def  transform_to_sql(self, user_query):
          query = {"query": user_query}
          sql_query = self.llm.invoke(self.prompt.format(
               query= query
          ))
          return sql_query.content
     
     def format_query(self, text):
          sql_query = text.replace("```sql", "").replace("```", "")
          print(sql_query)
          return sql_query
     
     def read_sql_query(self, sql):
          conn = sqlite3.connect(self.db_path)
          cur = conn.cursor()
          cur.execute(sql)
          rows = cur.fetchall()
          for row in rows:
               print(row)
          conn.close()

     
     def  run(self, user_query):
          sql_query = self.format_query(self.transform_to_sql(user_query))
          with sqlite3.connect(self.db_path) as conn:
               df = pd.read_sql_query(sql_query, conn)
          return df.to_string(index= False)


if __name__ == '__main__':

     sql = SQL_Constructor()
     input = "Điểm chuẩn ngành kỹ thuật phần mềm là bao nhiêu?"
     sql_query = sql.transform_to_sql(input)
     formatted = sql.format_query(sql_query)
     df = sql.run(input)
     
     print(sql_query)
     print("\n-----------------\n")
     print(formatted)

     # print("\n-----------------\n")
     # df = sql.read_sql_query(formatted)
     # print(df)

     print("\n-----------------\n")
     df1 = sql.run(input)
     print(df1)

