from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from pathlib import Path
import sqlite3
import pandas as pd

class SQL_Constructor:
     def  __init__(self):
          self.db_path = "university_admissions.db"
          self.prompt  = """"
          Bạn là một chuyên gia về SQL, chuyển đổi câu hỏi về điểm chuẩn thành mã SQL hoàn chỉnh.
          {query}
          Câu hỏi sẽ bao gồm ít nhất các thông tin sau:
          năm (ít nhất 2024, 2023, 2022, 2021), phương thức tuyển sinh và tên trường được chuyển thành mã `university_code`.
          Chú ý rằng sql sinh ra không có chữ sql ở đầu và cuối.
          Trả ra sql cho đúng code sql nằm trong """ """
          Phương thức tuyển sinh được mã hóa như sau:
          (1, 'Thi THPT')
          (2, 'Học bạ - Kết quả học tập THPT đợt 1')
          (3, 'Học bạ - Kết quả học tập THPT đợt 2')
          (4, 'DGNL')
          (5, 'UTXT đợt 1')
          (6, 'UTXT đợt 2')
          (7, 'Xét riêng')

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
          1. Điểm thi trung học phổ thông trường Tôn Đức Thắng 2022 ngành Ngôn ngữ Anh là bao nhiêu?
          sql sẽ giống như thế này : \n
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 1
               AND year = 2022
               AND major_name LIKE '%ngôn ngữ anh%'
               AND university_code = 'TDTU';
          ```

          2. Điểm đánh giá năng lực trường UEH năm 2022?
          sql sẽ giống như thế này: \n
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 4
               AND year = 2022
               AND university_code = 'UEH';
          ```

          3. Điểm đánh giá năng lực trường UEH ngành Quản trị kinh doanh năm 2022?
          sql sẽ giống như thế này:
          ```
          SELECT *
          FROM admission_scores
          WHERE admission_method_id = 4
               AND year = 2022
               AND university_code = 'UEH';
               AND major_name LIKE '%quản trị kinh doanh%';
          ```
"""
          self.llm = ChatGoogleGenerativeAI(model= "gemini-1.5-pro", temperature= 0.1)

     def  transform_to_sql(self, user_query):
          query = {"query": user_query}
          sql_query = self.llm.invoke(self.prompt.format(
               query= query
          ))
          return sql_query.content
     
     def format_query(self, text):
          sql_query = text.replace("```sql\n", "").replace("\n```", "")
          return sql_query
     
     def  run(self, user_query):
          sql_query = self.format_query(self.transform_to_sql(user_query))
          with sqlite3.connect(self.db_path) as conn:
               df = pd.read_sql_query(sql_query, conn)
          return df.to_string(index= False)
     
# sql = SQL_Constructor()

# sql_query = sql.transform_to_sql("Điểm chuẩn thpt Công nghệ thông tin TDTU 2021")
# formatted = sql.format_query(sql_query)
# df = sql.run("Điểm chuẩn thpt ngành marketing TDTU 2022")
# print(sql_query)
# print(formatted)
# print(df)