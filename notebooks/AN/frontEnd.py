import streamlit as st
from AdaptiveRAG import AdaptiveAgent
from pathlib import Path
from dotenv import load_dotenv
from QueryTransformation import QueryTransformation
# Load environment variables
load_dotenv(Path("./.env"))

from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from agentGemi import get_llm_and_agent
import warnings
warnings.filterwarnings("ignore")  # Chỉ tắt FutureWarning


# === THIẾT LẬP GIAO DIỆN TRANG WEB ===-+
def setup_page():
    """
    Cấu hình trang web cơ bản
    """

    # Cấu hình giao diện trang
    st.set_page_config(
        page_title="University Admission Assistant",    # Tiêu đề tab trình duyệt
        page_icon="🎓",                                # Icon tab
        layout="wide"
    )

# === KHỞI TẠO ỨNG DỤNG ===
def initialize_app():
    """
    Khởi tạo các cài đặt cần thiết:
    - Đọc file .env chứa API key
    - Cấu hình trang web
    """
    load_dotenv(Path("./.env"))  # Đọc API key từ file .env
    setup_page()  # Thiết lập giao diện

def show_contact():
    """
    Hiển thị thông tin liên hệ
    """
    st.write("""
        Nếu bạn có bất kỳ câu hỏi nào hoặc cần hỗ trợ thêm, đừng ngần ngại liên hệ với tôi qua:
    """)
    st.write("📧 **Email**: your_email@example.com")
    st.write("📱 **Phone**: +123 456 789")
    st.write("🌐 **Website**: [yourwebsite.com](https://www.yourwebsite.com)")
    st.write("🔗 **LinkedIn**: [Your LinkedIn](https://www.linkedin.com/in/yourprofile)")

# === THANH CÔNG CỤ BÊN TRÁI ===
def setup_sidebar():
    """
    Tạo thanh công cụ bên trái với các tùy chọn
    """
    with st.sidebar:
        st.title("⚙️ Cấu hình")
        # Phần 1: Introduce
        st.header("🎓 Trợ Lý Tuyển Sinh Đại Học")
        st.markdown(
            """
            Hệ thống hỗ trợ tra cứu thông tin tuyển sinh của các trường đại học tại TP.HCM:
            - Đại học Nguyễn Tất Thành (NTTU)
            - Đại học Sư Phạm TP.HCM (HCMUE)
            - Đại học Y Dược TP.HCM (UPM)
            - Đại học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)
            - Đại học Văn Lang (VLU)
            - Và các trường khác...
            """
        )
        # Thêm nút "New Chat"
        if st.button("🆕 New Chat"):
            # Reset lịch sử tin nhắn
            st.session_state.messages = [
                {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
            ]
            st.success("Cuộc trò chuyện mới đã được tạo!")
            
        
        # Phần 1: Chọn Model để trả lời
        st.header("🤖 Model AI")
        model_choice = st.radio(
            "Chọn AI Model để trả lời:",
            ["Geminai", "OpenAI GPT-4", "OpenAI Grok", "Ollama (Local)"]
        )

        
        return model_choice


# === GIAO DIỆN CHAT CHÍNH ===
def setup_chat_interface(model_choice):
    st.title("💬 AI Assistant")
    
    # Caption động theo model
    if model_choice == "OpenAI GPT-4":
        st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và OpenAI GPT-4")
    elif model_choice == "OpenAI Grok":
        st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và X.AI Grok")
        
    elif model_choice == "OpenAI Grok":
        st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và X.AI Grok")
    else:
        st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và Ollama LLaMA2")
    
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
        ]
        msgs.add_ai_message("Tôi có thể giúp gì cho bạn?")

    for msg in st.session_state.messages:
        role = "assistant" if msg["role"] == "assistant" else "human"
        st.chat_message(role).write(msg["content"])
        
    return msgs


# === XỬ LÝ TIN NHẮN NGƯỜI DÙNG ===
def handle_user_input(prompt, msgs, agent_executor):
    """
    Xử lý khi người dùng gửi tin nhắn:
    1. Hiển thị tin nhắn người dùng
    2. Gọi AI xử lý và trả lời
    3. Lưu vào lịch sử chat
    """
    
    
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)
    msgs.add_user_message(prompt)

    # Xử lý và hiển thị câu trả lời
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        
        # Lấy lịch sử chat
        chat_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages[:-1]
        ]

        # Gọi AI xử lý
        response = agent_executor.invoke(
            {
                "input": prompt,
                "chat_history": chat_history
            },
            {"callbacks": [st_callback]}
        )

        # Lưu và hiển thị câu trả lời
        output = response["output"]
        st.session_state.messages.append({"role": "assistant", "content": output})
        msgs.add_ai_message(output)
        st.write(output)

# === XỬ LÝ TIN NHẮN NGƯỜI DÙNG ===

# === HÀM CHÍNH ===
def main():
    """
    Hàm chính điều khiển luồng chương trình
    """
    
    initialize_app()
    prompt = st.chat_input("Hãy hỏi tôi bất cứ điều gì về thôn tin tuyển sinh")
    tab1, tab2= st.tabs(["Chat", "Contact"])
    # agent_executor = None  # Đảm bảo biến được khởi tạo
    
    
    with tab1:
        model_choice= setup_sidebar()
        msgs = setup_chat_interface(model_choice)
        
        # Khởi tạo AI dựa trên lựa chọn model để trả lời
        
        # if model_choice == "OpenAI GPT-4":
        #     retriever = get_openai_retriever(collection_to_query)
        #     agent_executor = get_openai_agent(retriever, "gpt4")
        # elif model_choice == "OpenAI Grok":
        #     retriever = get_openai_retriever(collection_to_query)
        #     agent_executor = get_openai_agent(retriever, "grok")
        if model_choice == "Geminai":
            agent_executor = get_llm_and_agent()
            
        # else:
        #     retriever = get_ollama_retriever(collection_to_query)
        #     agent_executor = get_ollama_agent(retriever)

        if prompt:
            handle_user_input(prompt, msgs, agent_executor)

    with tab2:
        
        show_contact()

# Chạy ứng dụng
if __name__ == "__main__":
    main() 