from QueryRouter import QueryRouter
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain_qdrant import QdrantVectorStore
import os
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict
from langchain_core.documents import Document

load_dotenv(Path("./.env"))

embedding_model = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-document-embedding",
    model_kwargs={"trust_remote_code": True}
)

class BaseRetrievalStrategy:
    def __init__(self, llm=None):
        self.embeddings = embedding_model
        self.llm = llm or genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        self.classifier = QueryRouter()

    def retrieve(self, query, k=3):
        return self.db.similarity_search(query, k=k)

class UniversityRetrievalStrategy(BaseRetrievalStrategy):
    def __init__(self, llm=None):
        super().__init__(llm)
        self.bm25_docs: Dict[str, List[Document]] = {}  # Cache for BM25 documents per university

    def _init_retrievers(self, university: str, documents: List[Document]):
        # Initialize BM25 retriever if not already cached
        if university not in self.bm25_docs:
            self.bm25_docs[university] = documents
            self.bm25_retriever = BM25Retriever.from_documents(documents)

        # Initialize vector store retriever
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
        vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        # Create ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, vector_retriever],
            weights=[0.5, 0.5]  # Equal weights for both retrievers
        )

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        # Get university classification
        university = self.classifier.UniversityRouting(query).university_code
        print(f'Truy vấn thuộc về trường: {university}')

        # Get documents for the university (you'll need to implement this)
        documents = self._get_university_documents(university)
        
        # Initialize retrievers
        self._init_retrievers(university, documents)
        
        # Perform hybrid search
        return self.ensemble_retriever.invoke(query)[:k]

    def _get_university_documents(self, university: str) -> List[Document]:
        """
        Implement this method to get all documents for a specific university.
        This could be from your database, file system, or other storage.
        """
        # Example implementation - replace with your actual document retrieval logic
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
        
        # Get all documents for the university
        results = vector_store.similarity_search("", k=150)  # Adjust the number as needed
        return results

docs = "amskasklsaksas"
print(list(docs))