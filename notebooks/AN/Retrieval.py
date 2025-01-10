from QueryRouter import QueryRouter
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_qdrant import QdrantVectorStore
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path("./.env"))


embedding_model = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-document-embedding",
    model_kwargs={"trust_remote_code": True}
    )
class BaseRetrievalStrategy:
     def __init__(self, llm = None):
          self.embeddings = embedding_model
          self.llm = llm or genai.GenerativeModel(model_name= "gemini-1.5-flash-8b")
          self.classifier = QueryRouter()

     def retrieve(self, query, k=3):
          return self.db.similarity_search(query, k=k)
    
class UniversityRetrievalStrategy(BaseRetrievalStrategy):

     def retrieve(self, query: str, k = 3)-> list:
          university = self.classifier.UniversityRouting(query).university_code
          print(f'Truy vấn thuộc về trường: {university}')
          
          client = QdrantClient(
               url=os.getenv('qdrant_url'),
               api_key=os.getenv('qdrant_api'),
               prefer_grpc=True
          )
          
          vector_store = QdrantVectorStore(
               client=client, 
               collection_name=str(university),
               embedding=embedding_model
          )
          return vector_store.similarity_search(query, k)
     
# retriever = UniversityRetrievalStrategy()
# query = "tuyển sinh NTTU 2023"
# docs1, docs2 = retriever.retrieve(query, k= 3)
# print(docs1)
# print('----------------------')
# print(docs2)
