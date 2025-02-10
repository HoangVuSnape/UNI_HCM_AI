from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from grader import RetrievalGrader2
from query_router import QueryRouter
from query_transformation import QueryTransformation
from retrieval_hybrid import UniversityRetrievalStrategy
from serve import Serve
from web_search import WebSearching
from typing_extensions import TypedDict
from IPython.display import display, Image
from query_to_sql import SQL_Constructor


class AgentState(TypedDict):
    """Represents the state of our agent during execution"""
    message: str
    current_query: List[str]
    retrieved_docs: List[Any]
    final_response: Optional[str]

class CorrectiveRag:
     def __init__(self):
          self.transformation = QueryTransformation()
          self.serve = Serve()
          self.retriever = UniversityRetrievalStrategy()
          self.retriever_grader = RetrievalGrader2()
          self.searcher = WebSearching()
          self.router = QueryRouter()
          self.sql_constructor = SQL_Constructor()

     
     def route_query(self, state: AgentState) -> Dict:
          state['current_query'].append(state["message"])
          query = state["message"]
          datasource = self.router.classify(query).datasource
          if datasource == "vectorstore":
               return {
                    'next': 'RAG',
                    **state
               }
          elif datasource == "SQL":
               return{
                    'next': 'SQL',
                    **state
               }
          else:
               return{
                    'next': 'websearch',
                    **state
               }
          
     
     def RAG_retriever(self, state: AgentState) -> Dict:
          
          print("\n----- RAG Retrieving Process-----")
          all_docs = []
          queries = state["current_query"]
          for query in queries:
               docs = self.retriever.retrieve(query)
               all_docs.extend(docs)
          
          return {
               "next": "grade_docs",
               **state,
               "retrieved_docs": all_docs
          }
     
     def _grade_docs(self, state: AgentState) -> Dict:
          print("\n------Check document relevance to question------")
          query = [state["current_query"][0] if len(state["current_query"]) == 1 else state["message"]]
          docs = state["retrieved_docs"]
          relevant_docs = []
          next = "RAG_generator"
          for doc in docs:
               score = int(self.retriever_grader.grade(query, doc))
               if score >= 3:
                    print("---DOCUMENT RELEVANT---")
                    relevant_docs.append(doc.page_content)
               else:
                    print("---DOCUMENT NOT RELEVANT---")
                    next = "transform"

          return {"next": next, **state, "retrieved_docs": relevant_docs}

     def RAG_generator(self, state: AgentState) -> Dict:
          print("\n---------Generating--------------")
          docs = state["retrieved_docs"]
          query = [state["current_query"][0] if len(state["current_query"]) == 1 else state["message"]]
          
          response = self.serve.run(query, docs)
          return{
               "next": "finish",
               **state,
               "final_response": response
          }
               
     def _transform_query(self, state: AgentState) -> Dict:
          print("\n------------Transform Query-------------")
          query = [state["current_query"][0] if len(state["current_query"]) == 1 else state["message"]]
          transformed_query = self.transformation.transformAll(query)
          state["current_query"] = transformed_query
          return {
               "next": "websearch_crag",
               **state,
          }
     def web_search_crag(self, state: AgentState) -> Dict:
          print("---------Webseearching process-----------")
          queries = state["current_query"]
          all_docs = state['retrieved_docs']
          for query in queries:
               search_results = self.searcher.search(query)
               all_docs.extend(search_results)
          print(all_docs)
          return {
               "next": "RAG_generator",
               **state,
               "retrieved_docs": all_docs
          }

     def SQL_retriever(self, state: AgentState):
          print("---------Retrive with SQL query-----------")
          query = state["message"]
          docs = []
          docs.append(self.sql_constructor.run(query))
          print(docs)
          return {
               "next": "SQL_generator",
               **state,
               "retrieved_docs": docs
          }
     
     def SQL_generator(self, state: AgentState):
          print("---------Generating-----------")
          docs = state['retrieved_docs']
          query = state["current_query"]
          response = self.serve.run(query, docs)
          return {
               "next": "finish",
               **state,
               "final_response": response
          }
     
     def websearch(self, state: AgentState) -> Dict:
        print("-------Web Searching---------")
        question = state['message']
        search_results = self.searcher.search(question)
        
        return {
            "next": "websearch_generator",
            **state,
            "retrieved_docs": search_results
          }
     
     def websearch_generator(self, state: AgentState) -> dict:
          print("\n---------Generating--------------")
          docs = state["retrieved_docs"]
          question = state['current_query']
          response = self.serve.run(question, docs)
          
          return {
               "next": "finish",
               **state,
               "final_response": response
          }

     def _create_workflow(self):
          workflow = StateGraph(AgentState)

          workflow.add_node("router", self.route_query)
          workflow.add_node("RAG_retriever", self.RAG_retriever)
          workflow.add_node("grader", self._grade_docs)
          workflow.add_node("RAG_generator", self.RAG_generator)
          workflow.add_node("transform_query", self._transform_query)
          workflow.add_node("websearch_crag", self.web_search_crag)
          workflow.add_node("SQL_retriever", self.SQL_retriever)
          workflow.add_node("SQL_generator", self.SQL_generator)
          workflow.add_node("websearch_retriever", self.websearch)
          workflow.add_node("websearch_generator", self.websearch_generator)

          workflow.add_edge(START, "router")

          workflow.add_conditional_edges(
               "router",
               lambda x: x["next"],
               {
                    "RAG": "RAG_retriever",
                    "SQL": "SQL_retriever",
                    "websearch": "websearch_retriever"
               },
          )

          workflow.add_edge("RAG_retriever", "grader")
          workflow.add_conditional_edges(
               "grader",
               lambda x: x["next"],
               {
                    "RAG_generator": "RAG_generator",
                    "transform": "transform_query"
               },
          )
          workflow.add_edge("transform_query", "websearch_crag")
          workflow.add_edge("websearch_crag", "RAG_generator")
          workflow.add_edge("RAG_generator", END)

          workflow.add_edge("SQL_retriever", "SQL_generator")
          workflow.add_edge("SQL_generator", END)

          workflow.add_edge("websearch_retriever", "websearch_generator")
          workflow.add_edge("websearch_generator", END)

          return workflow.compile()
     def display(self):
          workflow = self._create_workflow()
          # display(Image(workflow.get_graph().draw_mermaid_png()))
          with open("adaptive_rag.png", 'wb') as f:
               f.write(workflow.get_graph().draw_mermaid_png())
          
     
     def run(self, query: str) -> str:
          workflow = self._create_workflow()
          initial_state = {
               "message": query,
               "current_query": [],
               "retrieved_docs": [],
               "final_response": None,
          }
          
          
          final_state = workflow.invoke(initial_state)
          return final_state["final_response"] or "No response generated"

if __name__ == "__main__":         
     agent = CorrectiveRag()
     #agent.display()
     #query = "Giới thiệu trường đại học Tôn Đức Thắng"
     #query = "Chỉ tiêu tuyển sinh năm 2021 VLU"
     #query = "Điểm chuẩn phương thức thpt ngành Công nghệ sinh học trường đại học Tôn Đức Thắng 2022"
    #  query = "Giới thiệu ông Phạm Minh Chính"
     query = "Điểm chuẩn thpt khoa học máy tính 2024"
     answer = agent.run(query)
     print(answer)