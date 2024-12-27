from langchain.tools.retriever import create_retriever_tool
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from seed_data import seed_milvus, connect_to_milvus
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


def get_retriever(collection_name: str = "data_test") -> EnsembleRetriever:
    """
    Tạo một ensemble retriever kết hợp vector search (Milvus) và BM25
    Args:
        collection_name (str): Tên collection trong Milvus để truy vấn
    Returns:
        EnsembleRetriever: Retriever kết hợp với tỷ trọng:
            - 70% Milvus vector search (k=4 kết quả)
            - 30% BM25 text search (k=4 kết quả)
    """
    try:
        # Kết nối với Milvus và tạo vector retriever
        vectorstore = connect_to_milvus('http://localhost:19530', collection_name)
        milvus_retriever = vectorstore.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 4}
        )

        # Tạo BM25 retriever từ toàn bộ documents
        documents = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in vectorstore.similarity_search("", k=100)
        ]
        
        if not documents:
            raise ValueError(f"Không tìm thấy documents trong collection '{collection_name}'")
            
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 4

        # Kết hợp hai retriever với tỷ trọng
        ensemble_retriever = EnsembleRetriever(
            retrievers=[milvus_retriever, bm25_retriever],
            weights=[0.7, 0.3]
        )
        return ensemble_retriever
        
    except Exception as e:
        print(f"Lỗi khi khởi tạo retriever: {str(e)}")
        # Trả về retriever với document mặc định nếu có lỗi
        default_doc = [
            Document(
                page_content="Có lỗi xảy ra khi kết nối database. Vui lòng thử lại sau.",
                metadata={"source": "error"}
            )
        ]
        return BM25Retriever.from_documents(default_doc)



def get_llm_and_agent(retriever):
    """
    Khởi tạo LLM và agent với Ollama
    """
    # Tạo retriever tool
    tool = create_retriever_tool(
        retriever,
        "find_documents",
        "Search for information of Stack AI."
    )

    # Khởi tạo ChatOllama
    llm = ChatOllama(
        model="llama2",  # hoặc model khác tùy chọn
        temperature=0,
        streaming=True
    )

    tools = [tool]

    # Thiết lập prompt template
    system = """You are an expert at AI. Your name is AISnape. For Stack AI questions call the find_document tool"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Tạo agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# Khởi tạo retriever và agent với collection mặc định
retriever = get_retriever()
agent_executor = get_llm_and_agent(retriever)