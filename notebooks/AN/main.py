from langchain_groq import ChatGroq
import os
from pathlib import Path
from Serve import Serve
from dotenv import load_dotenv, find_dotenv
load_dotenv(Path("./.env"))

GROQ_API_KEY= os.getenv("groq_api_key")
llm = ChatGroq(
     model= "llama-3.3-70b-versatile",
     temperature= 0.1
)
serve = Serve(llm)
question = "Chỉ tiêu và phương thức tuyển sinh Đại học Nguyễn Tất Thành 2021"
#docs = retriever.retrieve(question)
response = serve.__call__(question)
print(response)
