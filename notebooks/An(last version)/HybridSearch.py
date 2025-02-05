from QueryRouter import QueryRouter
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
import os
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

load_dotenv(Path("./.env"), override= True)

embedding_model = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-document-embedding",
    model_kwargs={"trust_remote_code": True}
)

class DocumentReRanker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-12-v2"):
        """
        Initialize the re-ranker with a cross-encoder model.
        
        :param model_name: Name of the cross-encoder model to use
        """
        self.cross_encoder = CrossEncoder(model_name)
    
    def re_rank(self, query: str, documents: List[Document], top_k: int = 3) -> List[Document]:
        """
        Re-rank documents based on their relevance to the query.
        
        :param query: Search query string
        :param documents: List of documents to re-rank
        :param top_k: Number of top documents to return
        :return: Re-ranked list of documents
        """
        # Prepare input pairs for cross-encoder
        pairs = [[query, doc.page_content] for doc in documents]
        
        # Get relevance scores
        scores = self.cross_encoder.predict(pairs)
        
        # Create a list of (document, score) tuples and sort
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k documents
        return [doc for doc, score in scored_docs[:top_k]]


class BaseRetrievalStrategy:
    def __init__(self, llm=None):
        self.embeddings = embedding_model
        self.llm = llm or ChatGoogleGenerativeAI(model= "gemini-1.5-pro" , temperature= 0.1,
                                                   api_key= os.getenv("GG_API"))
        self.classifier = QueryRouter()
        self.re_ranker = DocumentReRanker()

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
            weights=[0.3, 0.7]  # Equal weights for both retrievers
        )

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        # Get university classification
        university = self.classifier.UniversityRouting(query).university_code
        print(f'Truy vấn thuộc về trường: {university}')

        # Get documents for the university (you'll need to implement this)
        documents = self._get_university_documents(university)
        
        # Initialize retrievers
        self._init_retrievers(university, documents)

        initial_results = self.ensemble_retriever.invoke(query)

        re_ranked_results = self.re_ranker.re_rank(query, initial_results, k)

        # Perform hybrid search
        return re_ranked_results

    def _get_university_documents(self, university: str) -> List[Document]:
        """
        Implement this method to get all documents for a specific university.
        This could be from your database, file system, or other storage.
        """
        # Example implementation - replace with your actual document retrieval logic
        client = QdrantClient(
            url=os.getenv('qdrant_url2'),
            api_key=os.getenv('qdrant_api2'),
            prefer_grpc=True
        )
        
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=str(university),
            embedding=embedding_model
        )
        
        # Get all documents for the university
        results = vector_store.similarity_search("", k=100)  # Adjust the number as needed
        return results
if __name__ == "__main__":         

    query = "Chỉ tiêu tuyển sinh 2021 VLU"
    retriever = UniversityRetrievalStrategy()
    docs = retriever.retrieve(query)
    print(docs)