import streamlit as st
from langchain_groq import ChatGroq
import os
from pathlib import Path
from Serve import Serve
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path("./.env"))

# Initialize Groq LLM and Serve
@st.cache_resource
def initialize_serve():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1
    )
    return Serve(llm)

# Page configuration
st.set_page_config(
    page_title="University Admission Assistant",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Trợ Lý Tuyển Sinh Đại Học")
st.markdown("""
    Hệ thống hỗ trợ tra cứu thông tin tuyển sinh của các trường đại học tại TP.HCM:
    - Đại học Nguyễn Tất Thành (NTTU)
    - Đại học Sư Phạm TP.HCM (HCMUE)
    - Đại học Y Dược TP.HCM (UPM)
    - Đại học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)
    - Đại học Văn Lang (VLU)
    - Và các trường khác...
""")

# Initialize serve
serve = initialize_serve()

# Create the query interface
query = st.text_input("Nhập câu hỏi của bạn về thông tin tuyển sinh...", 
                     placeholder="Ví dụ: Chỉ tiêu và phương thức tuyển sinh Đại học Nguyễn Tất Thành 2021")

if st.button("Tìm kiếm"):
    if query:
        with st.spinner("Đang tìm kiếm thông tin..."):
            try:
                response = serve.__call__(query)
                st.markdown("### Kết quả:")
                st.markdown(response.answer)
            except Exception as e:
                st.error("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.")

# Sidebar with additional information
with st.sidebar:
    st.header("Hướng Dẫn Sử Dụng")
    st.markdown("""
    1. **Các loại câu hỏi có thể hỏi:**
        - Điểm chuẩn các năm
        - Chỉ tiêu tuyển sinh
        - Học phí
        - Thông tin ngành học
        - Phương thức xét tuyển
        
    2. **Ví dụ câu hỏi:**
        - "Điểm chuẩn Đại học Văn Lang năm 2021?"
        - "Chỉ tiêu tuyển sinh Đại học Nguyễn Tất Thành 2021?"
        - "Học phí Đại học Sư Phạm TPHCM?"
    """)

    st.divider()
    
    st.markdown("### Liên Hệ")
    st.markdown("""
        - 📧 Email: support@example.com
        - 📱 Hotline: 1900-xxx-xxx
    """)