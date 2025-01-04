import time
import datetime
import pytz
from google.oauth2 import service_account
from langchain_google_vertexai import ChatVertexAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.schema import HumanMessage
import os 
import google.generativeai as genai
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

# === 1. Setup Vertex AI with credentials ===
credentials_path = "E:/LLM_clone/Tdtu-chatbot/credentials/tdtuchat-16614553b756.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Geminai 
GEMINAI_API_KEY_1 = os.getenv("GEMINAI_API_KEY_1")
url_qdrant = os.getenv("qdrant_url")
api_key_qdrant = os.getenv("qdrant_api")
if not all([GEMINAI_API_KEY_1, url_qdrant, api_key_qdrant]):
    raise ValueError("Required Qdrant API keys are missing.")

genai.configure(api_key=GEMINAI_API_KEY_1)


class GenAIEmbeddings(Embeddings):
    def __init__(self, model: str = "models/text-embedding-004"):
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            # Gọi API để tạo embedding
            result = genai.embed_content(model=self.model, content=text)
            # Kiểm tra kết quả trả về
            if isinstance(result, dict) and "embedding" in result:
                embeddings.append(result["embedding"])
            else:
                raise ValueError(f"Unexpected response format: {result}")
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        # Gọi API để tạo embedding
        result = genai.embed_content(model=self.model, content=text)
        # Kiểm tra kết quả trả về
        if isinstance(result, dict) and "embedding" in result:
            return result["embedding"]
        raise ValueError(f"Unexpected response format: {result}")



embedding_model = GenAIEmbeddings()
##########
llm = ChatVertexAI(
    model="gemini-1.5-pro",
    temperature=0.6,
    max_tokens=200,
    credentials=credentials,
    max_retries=5
)

# === 2. Define tools ===
@tool
def get_current_time_vietnam() -> str:
    """Get the current time in Vietnam (UTC+7)."""
    try:
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        vietnam_time = datetime.datetime.now(vietnam_tz)
        return vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error in retrieving time: {e}"
    
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def get_retrieval(query: str = "What is this?") -> str:
    """Truy vấn tài liệu từ Qdrant bằng GenAI embeddings."""
    try:
        # Kết nối với Qdrant client
        client = QdrantClient(url=url_qdrant, api_key=api_key_qdrant)

        # Kiểm tra collection tồn tại
        if "BKU" not in [collection.name for collection in client.get_collections().collections]:
            return "Collection 'BKU' không tồn tại trong Qdrant!"

        # Khởi tạo vector store
        vector_store = Qdrant(
            client=client,
            collection_name="BKU",
            embeddings=embedding_model,
        )

        # Tạo embedding cho câu truy vấn
        query_embedding = embedding_model.embed_query(query)

        # Tìm kiếm tài liệu trong vector store
        docs = vector_store.similarity_search(query, k=5)

        # Kiểm tra và trả về kết quả
        if not docs:
            return "Không tìm thấy tài liệu phù hợp với truy vấn."
        
        # Trả về nội dung tài liệu
        return "\n".join([
            f"- {getattr(doc, 'page_content', 'No content found')}" for doc in docs
        ])

    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


tools = [get_current_time_vietnam, add, get_retrieval]

# === 3. Create LLM and AgentExecutor ===
def get_llm_and_agent() -> AgentExecutor:
    """
    Create and return an AgentExecutor using the Vertex AI model and tools.
    """
    system = """
    You are an expert AI assistant named AISnape. You specialize in answering Stack AI questions.
    Use the tools provided to help with specific queries.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    
    # Return the AgentExecutor
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# Initialize the agent executor
agent_executor = get_llm_and_agent()
