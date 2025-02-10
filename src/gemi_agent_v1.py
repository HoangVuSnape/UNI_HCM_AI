import datetime
import pytz
from google.oauth2 import service_account
from langchain_google_vertexai import ChatVertexAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from query_transformation import QueryTransformation
import warnings
warnings.filterwarnings("ignore")  # Tắt tất cả cảnh báo

from query_to_sql import SQL_Constructor
from web_search import WebSearching
from adaptive_rag import AdaptiveAgent


# # === 1. Setup Vertex AI with credentials ===
credentials_path = "../tdtuchat-16614553b756.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

##########
llm = ChatVertexAI(
    model="gemini-1.5-pro",
    streaming= True, 
    temperature=0.5,
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
def getRetrieval(query: str) -> str:
    "Đây là hàm lấy thông tin các trường đại học từ database"
    
    agent = AdaptiveAgent()
    # agent.display()
    
    answer = agent.run(query)
    return answer

@tool
def getScore(query: str) -> str:
    "Đây là hàm lấy điểm chuẩn các phương thức của các trường bằng SQL"
    
    sql = SQL_Constructor()
    df = sql.run(query)

    return df 

@tool
def webSearch(query: str) -> str:
    "Tìm kiếm thông tin trên web"
    
    searching = WebSearching()
    docs = searching.run(query)
    
    return docs

tools = [get_current_time_vietnam, getRetrieval, getScore, webSearch]


# === 3. Create LLM and AgentExecutor ===
def get_llm_and_agent1() -> AgentExecutor:
    """
    Create and return an AgentExecutor using the Vertex AI model and tools.
    """
    system = """
    Bạn là một chuyên gia AI tên là AISnape. Bạn có khả năng xử lý các truy vấn đầu vào liên quan đến việc lấy thời gian hiện tại, cải thiện câu truy vấn, lấy thông tin các trường đại học, lấy điểm chuẩn từ cơ sở dữ liệu, và thực hiện tìm kiếm thông tin trên web bằng cách sử dụng các công cụ: get_current_time_vietnam, getRetrieval, getScore, webSearch.
    Hướng dẫn:
        - Thông tin trong database các trường từ năm 2021, 2022, 2023, 2024.   
        - Khi có chữ "search web" thì mới dùng tool webSearch còn không hãy dùng tool: getRetrieval để lấy thông tin. 
            - Ví dụ: search web: thủ tương phạm minh chính -> dùng tool webSearch
            - Phương thức tuyển sinh đại học TDTU 2022 -> dùng tool getRetrieval
            - Điểm chuẩn khoa học máy tính 2024 TDTU phương thức thpt -> dùng tool getScore
            
    Chú ý:   
    - Khi gặp câu hỏi liên quan, hãy sử dụng các công cụ đã định nghĩa để đưa ra câu trả lời chính xác.
    - Nếu không biết câu trả lời, hãy thẳng thắn trả lời "Tôi không biết" và không tạo ra thông tin không chính xác.
    Hãy tận dụng các công cụ một cách phù hợp để hỗ trợ câu trả lời của bạn.
    
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

if __name__ == "__main__":
    
    # Initialize the agent executor
    agent_executor = get_llm_and_agent1()