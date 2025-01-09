from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv 
load_dotenv(".env")

base_folder = "./Admission"
embedding_model = HuggingFaceEmbeddings(
     model_name="dangvantuan/vietnamese-document-embedding",     
     model_kwargs={"trust_remote_code": True}  # Add this parameter
)
url = os.getenv('qdrant_url')
api = os.getenv('qdrant_api')
splitter = SemanticChunker(embeddings= embedding_model, breakpoint_threshold_type= 'gradient', breakpoint_threshold_amount= 90, min_chunk_size= 512)
base_folder = "/content/drive/MyDrive/Data/Admission"

for folder_name in os.listdir(base_folder):
  folder_path = os.path.join(base_folder, folder_name)
  if os.path.isdir(folder_path):
    print(f"Processing folder: {folder_name}")

    loader = DirectoryLoader(folder_path, glob=["*.txt", "*.md"])
    documents = loader.load()

    chunks = splitter.split_documents(documents)
    name = "DH" + folder_name
    # Create vector store using proper URL format
    vector_store = Qdrant.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url= url,
        api_key=api,
        prefer_grpc=False,
        collection_name=name,
    )
    print(f"Collection '{folder_name}' created successfully.")
