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
# import google.generativeai as genai
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import streamlit as st
from QueryTransformation import QueryTransformation
import warnings
warnings.filterwarnings("ignore")  # Tắt tất cả cảnh báo

from Retrieval import UniversityRetrievalStrategy

# === 1. Setup Vertex AI with credentials ===
credentials_path = "E:/LLM_clone/credentials/tdtuchat-16614553b756.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Geminai 
url_qdrant = os.getenv("qdrant_url")
api_key_qdrant = os.getenv("qdrant_api")
if not all([ url_qdrant, api_key_qdrant]):
    raise ValueError("Required Qdrant API keys are missing.")

# genai.configure(api_key=GEMINAI_API_KEY_1)


##########
llm = ChatVertexAI(
    model="gemini-1.5-pro",
    temperature=0.6,
    max_tokens=512,
    credentials=credentials,
    max_retries=5
)

# === 2. Define tools ===
@tool
def get_current_time_vietnam() -> str:
    """Lấy thời gian hiện tại của Việt nam (UTC+7)."""
    try:
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        vietnam_time = datetime.datetime.now(vietnam_tz)
        return vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error in retrieving time: {e}"

@tool
def queryTransformationTest(prompt: str) -> str:
    """ Đây là hàm giúp cải thiện câu input ban đầu"""
    
    agent = QueryTransformation()
    
    inputtest = {"query": prompt}
    response = agent.enhancing_query(inputtest)
    return response

@tool
def getRetrieval(query: str) -> list:
    "Đây là hàm lấy thông tin các trường đại học từ database"
    
    retriever = UniversityRetrievalStrategy()
    docs = retriever.retrieve(query, k= 3)

    return docs

tools = [get_current_time_vietnam, queryTransformationTest, getRetrieval]


# === 3. Create LLM and AgentExecutor ===
def get_llm_and_agent() -> AgentExecutor:
    """
    Create and return an AgentExecutor using the Vertex AI model and tools.
    """
    system = """
    Bạn là 1 chuyên gia AI và tên là AISnape. Bạn có thể trả lời những câu đầu vào về thời gian, cải thiện câu input ban đầu, lấy thông tin các trường đại học bằng các tools, : get_current_time_vietnam, queryTransformationTest, getRetrieval. 
    Chú ý:
        - Khi có từ cải thiện mới gọi đến tool queryTransformationTest
    Hãy sử dụng tools để hỗ trợ câu trả lời. 
    
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