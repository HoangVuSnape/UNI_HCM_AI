from query_router import QueryRouter
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain_qdrant import QdrantVectorStore
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path("../.env"), override= True)


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
               url=os.getenv('QDRANT_URL'),
               api_key=os.getenv('QDRANT_API'),
               prefer_grpc=True
          )
          
          vector_store = QdrantVectorStore(
               client=client, 
               collection_name=str(university),
               embedding=embedding_model
          )
          return vector_store.similarity_search(query, k)

# Test
if __name__ == "__main__":   
     
     retriever = UniversityRetrievalStrategy()
     query = "Điểm chuẩn ngành Công Nghê Thông Tin 2021 UIT"
     docs = retriever.retrieve(query, k= 3)
     
     #######
     metadata_0 = docs[0].metadata
     print(metadata_0)

     # Hoặc lấy từng phần cụ thể của metadata
     source = metadata_0['source']
     document_id = metadata_0['_id']
     collection_name = metadata_0['_collection_name']

     # In ra từng phần
     print("Source:", source)
     print("Document ID:", document_id)
     print("Collection Name:", collection_name)

     print('----------------------')
     
     ###
     for doc in docs:
          print(doc.page_content)
          print('----------------------')
