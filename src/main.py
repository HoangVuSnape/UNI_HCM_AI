# Version 2 front end
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from gemi_agent_v1 import get_llm_and_agent1 as agentV1
from gemi_agent_v2 import get_llm_and_agent2 as agentV2
import warnings
from load_key import EnvLoader

warnings.filterwarnings("ignore")

env_loader = EnvLoader()
env_loader.load_all()
# === THIẾT LẬP TRANG WEB ===
def setup_page():
    """
    Cấu hình giao diện trang web
    """
    st.set_page_config(
        page_title="University Admission Assistant",
        page_icon="🎓",
        layout="wide"
    )

# === KHỞI TẠO ỨNG DỤNG ===
def initialize_app():
    """
    Khởi tạo ứng dụng, bao gồm các biến và giao diện
    """
    setup_page()

    # Khởi tạo danh sách lịch sử trò chuyện
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = []

    # Khởi tạo lịch sử tin nhắn hiện tại
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
        ]

# === THANH CÔNG CỤ BÊN TRÁI ===
def setup_sidebar():
    """
    Tạo thanh công cụ bên trái với các tùy chọn
    """
    with st.sidebar:
        st.title("⚙️ Cấu hình")
        st.header("🎓 Trợ Lý Tuyển Sinh Đại Học")
        st.markdown(
            """
            Hệ thống hỗ trợ tra cứu thông tin tuyển sinh của các trường đại học tại TP.HCM:
            - Xem thêm tại phần giới thiệu
            """
        )

        # Nút tạo mới cuộc trò chuyện
        if st.button("🆕 New Chat"):
            if st.session_state.messages:
                st.session_state.chat_histories.append(st.session_state.messages)
            st.session_state.messages = [
                {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
            ]
            
            st.session_state.reset_msgs = True
            st.success("Cuộc trò chuyện mới đã được tạo!")

        # Chọn model AI
        st.header("🤖 Model AI")
        model_choice = st.radio(
            "Chọn phiên bản để trả lời:",
            ["Version 1", "Version 2"]
        )

        return model_choice

# === HIỂN THỊ LỊCH SỬ TRÒ CHUYỆN ===
def show_chat_histories():
    """
    Hiển thị danh sách lịch sử các cuộc trò chuyện
    """
    st.header("📜 Lịch sử cuộc trò chuyện")
    if st.session_state.chat_histories:
        for i, chat in enumerate(st.session_state.chat_histories):
            with st.expander(f"Cuộc trò chuyện {i+1}"):
                for msg in chat:
                    role = "👤 Người dùng" if msg["role"] == "human" else "🤖 AI"
                    st.markdown(f"**{role}:** {msg['content']}")
    else:
        st.write("Chưa có lịch sử cuộc trò chuyện nào.")

def introduction():
    st.title("AI Hỗ Trợ Tuyển Sinh - 15 Trường Đại Học TP.HCM")
    
    st.markdown("""
    ## Giới thiệu
    Hệ thống AI hỗ trợ tuyển sinh giúp so sánh, tra cứu thông tin về 15 trường đại học tại TP.HCM:
    
    1. **Trường Đại học Nguyễn Tất Thành** (NTTU)  
    2. **Trường Đại học Sư Phạm TP HCM** (HCMUE)  
    3. **Trường Đại học Y Dược TP HCM** (UMP)  
    4. **Trường Đại học Tài Chính - Marketing** (UFM)  
    5. **Trường Đại học Văn Lang** (VLU)  
    6. **Trường Đại học Y Khoa Phạm Ngọc Thạch** (PNTU)  
    7. **Trường Đại học Sư Phạm Kỹ Thuật TP HCM** (HCMUTE)  
    8. **Trường Đại học Ngoại Thương TP HCM** (FTU2)  
    9. **Trường Đại học Tôn Đức Thắng** (TDTU)  
    10. **Trường Đại học Kinh Tế TP HCM** (UEH)  
    11. **Trường Đại học FPT** (FPTU)  
    12. **Trường Đại học Bách Khoa TP HCM** (BKU)  
    13. **Trường Đại học Khoa Học Tự Nhiên TP HCM** (HCMUS)  
    14. **Trường Đại học Mở TP HCM** (OU)  
    15. **Trường Đại học Công Nghệ Thông Tin TP HCM** (UIT)  
    """)
    
    st.markdown("""
    ## Phiên bản Hệ thống AI
    Hệ thống hỗ trợ hai phiên bản:
    - **Phiên bản 1:** Adaptive RAG
    - **Phiên bản 2:** Corrective RAG
    
    API sử dụng:
    - **Gemini AI** (Model: Gemini 1.5 Pro)
    - **Groq AI** (Model: Llama 3.3 70B Versatile)
    """)
    
    st.markdown("""
    ## Liên hệ sản phẩm
    **521H0385 - Trần Quốc An (KHMT)**  
    **521H0517 - Hoàng Đình Quý Vũ**  
    📧 Email: hoangdinhquyvu.snape.22@gmail.com
    """)


def setup_chat_interface(model_choice):
    st.title("💬 AI Assistant")
    
    # Caption động theo model
    if model_choice == "Version 1":
        st.caption("🚀 Trợ lý AI Tuyển sinh sử dụng Adaptive RAG")
    else:
        st.caption("🚀 Trợ lý AI Tuyển sinh sử dụng Corrective RAG")
    
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    
    if st.session_state.get("reset_msgs"):
        msgs.clear()  # Reset lịch sử tin nhắn trong LangChain
        st.session_state.reset_msgs = False
        
        
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
        
        # Lấy lịch sử chat để cùng với prompt tạo thành 1 context. 
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

# === HÀM CHÍNH ===
def render():
    """
    Hàm chính điều khiển luồng chương trình
    """
    initialize_app()
    prompt = st.chat_input("Hãy hỏi tôi bất cứ điều gì về thôn tin tuyển sinh")
    tab1, tab2, tab3 = st.tabs(["Giới thiệu","Chat", "Lịch sử chat"])
    
    with tab1:
        introduction()
        
    with tab2:
        # Thiết lập sidebar
        model_choice= setup_sidebar()
        msgs = setup_chat_interface(model_choice)

        if model_choice == "Version 1":
            agent_executor = agentV1()
        else:
            agent_executor = agentV2()

        if prompt:      
            handle_user_input(prompt, msgs, agent_executor)

    with tab3:
        # Hiển thị lịch sử trò chuyện
        show_chat_histories()

# Chạy ứng dụng
if __name__ == "__main__":
    render()