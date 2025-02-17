import datetime
import pytz
from google.oauth2 import service_account
from langchain_google_vertexai import ChatVertexAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import warnings
warnings.filterwarnings("ignore")  # Tắt tất cả cảnh báo


from corrective_rag import CorrectiveRag


# # === 1. Setup Vertex AI with credentials ===
credentials_path = "../creadientials_vertex.json"
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
def corrective_Rag(query: str) -> str:
    "Đây là hàm lấy tìm kiếm thông tin từ người dùng bao gồm các trường đại học, điểm và vân vân..."
    
    agent = CorrectiveRag()
    # agent.display()
    
    answer = agent.run(query)
    return answer

tools = [get_current_time_vietnam, corrective_Rag]


# === 3. Create LLM and AgentExecutor ===
def get_llm_and_agent2() -> AgentExecutor:
    """
    Create and return an AgentExecutor using the Vertex AI model and tools.
    """
    system = """
    Bạn là một AI hỗ trợ tuyển sinh tên là AI tuyển sinh và thông tin ngoài luồng. 
    Bạn có khả năng xử lý các truy vấn đầu vào liên quan đến:
    - việc lấy thời gian hiện tại: get_current_time_vietnam
    - Tìm kiếm thông tin như các trường đại học, điểm chuẩn và thông tin ngoài: corrective_Rag.
    Chú ý:
    - Khi người dùng đưa thông tin vào thì sẽ gọi đến tool: corrective_Rag còn về thời gian : get_current_time_vietnam
    - Thông tin trong database các trường từ năm 2021, 2022, 2023, 2024.
    
    Ví dụ:
    Gọi tool corrective_Rag khi có các câu hỏi như sau:
    - Giới thiệu trường đại học Tôn Đức Thắng 
    - Giới thiệu ông Phạm Minh Chính
    - Điểm chuẩn phương thức thpt ngành Công nghệ sinh học trường đại học Tôn Đức Thắng 2022
    
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
    agent_executor = get_llm_and_agent2()