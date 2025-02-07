import streamlit as st
from AdaptiveRAG import AdaptiveAgent
from pathlib import Path
from dotenv import load_dotenv
from QueryTransformation import QueryTransformation
# Load environment variables
load_dotenv(Path("./.env"))

# Khởi tạo AdaptiveAgent
@st.cache_resource
def initialize_agent():
    return QueryTransformation()



# Cấu hình giao diện trang
st.set_page_config(
    page_title="University Admission Assistant",
    page_icon="🎓",
    layout="wide"
)



# Hiển thị tiêu đề và mô tả
st.title("🎓 Trợ Lý Tuyển Sinh Đại Học")
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

agent = initialize_agent()
# query = "Tuyển sinh đại học Tôn Đức Thắng 2024"
# answer = agent.run(query)
# print(answer)

# Quản lý lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
    ]

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "assistant" else "human"
    st.chat_message(role).write(msg["content"])

# Nhập câu hỏi từ người dùng
prompt = st.text_input("Nhập câu hỏi của bạn:", key="user_input")
inputtest = {"query": prompt}

if st.button("Gửi") and prompt:
    # Lưu tin nhắn của người dùng vào lịch sử
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    # Xử lý câu hỏi với AdaptiveAgent
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                response = agent.enhancing_query(inputtest)
            except Exception as e:
                response = f"Đã xảy ra lỗi: {str(e)}"

        # Hiển thị và lưu phản hồi của hệ thống
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
