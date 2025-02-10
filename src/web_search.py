from typing import List, Dict, Optional
from langchain.docstore.document import Document
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import os
from pathlib import Path
import langdetect

load_dotenv(Path("../.env"))
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

class WebSearching:
    def __init__(self, max_result: int = 3, search_depth: str = "basic"):
        self.searcher = TavilySearchResults(
            max_results=  max_result,
            search_depth= search_depth,
            include_answer=True,
            include_raw_content=True,
            include_images=False,
        )

    
    def search(self, query: str) -> List[Document]:
        response = self.searcher.invoke({"query": query})
        docs = []
        for result in response:
            content = result['content']
            # Lọc kết quả chỉ lấy nội dung bằng tiếng Việt
            if langdetect.detect(content) == 'vi':
                docs.append(result['url'] + "\n" + content)
        return docs
    
    def format(self, docs: List[Document]) -> str:
        """Hợp nhất các tài liệu thành một chuỗi duy nhất."""
        merged_content = "\n\n".join(docs)
        return merged_content

    def run(self, query: str) -> str:
        """Thực hiện tìm kiếm và định dạng kết quả."""
        docs = self.search(query)
        merged_content = self.format(docs)
        return merged_content
    
if __name__ == "__main__":   
    searching = WebSearching()
    query = "Giới thiệu ông Phạm Minh Chính"
    
    # Chạy hàm run để tìm kiếm và định dạng kết quả
    result = searching.run(query)
    
    print("Merged Content:")
    print(result)