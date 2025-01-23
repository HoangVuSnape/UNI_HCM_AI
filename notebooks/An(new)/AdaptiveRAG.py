from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from Grader import RetrievalGrader, AnswerGrader
from QueryRouter import QueryRouter
from QueryTransformation import QueryTransformation
from Retrieval import UniversityRetrievalStrategy
from Serve import Serve
from websearch import WebSearching
from typing_extensions import TypedDict
from IPython.display import display, Image
from QueryToSQL import SQL_Constructor
from websearch import WebSearching



class AgentState(TypedDict):
    """Represents the state of our agent during execution"""
    message: str
    current_query: str
    sub_queries: List[str]
    retrieved_docs: List[Any]
    final_response: Optional[str]
    limit : int

class AdaptiveAgent:
     def __init__(self):
          self.router = QueryRouter()
          self.transformation = QueryTransformation()
          self.serve = Serve()
          self.retriever = UniversityRetrievalStrategy()
          self.retriever_grader = RetrievalGrader()
          self.answer_grader = AnswerGrader()
          self.searcher = WebSearching()
          self.router = QueryRouter()
          self.sql_constructor = SQL_Constructor()
          self.searcher = WebSearching()

     
     def route_query(self, state: AgentState) -> Dict:
          state['current_query'] = state["message"]
          datasource = self.router.classify(state['current_query']).datasource
          if datasource == "vectorstore":
               return {
                    'next': 'RAG_retrive'
                    **state
               }
          elif datasource == "SQL":
               return{
                    'next': 'SQL_retrieve',
                    **state
               }
          else:
               return{
                    'next': 'websearching',
                    **state
               }
          
     
     def _retrieve_documents(self, state: AgentState) -> Dict:
          
          print("\n-----Retrieving Process-----")
          all_docs = []
          queries = state["sub_queries"] if state["sub_queries"] else [state["current_query"]]
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
          query = state["current_query"]
          docs = state["retrieved_docs"]
          score = int(self.retriever_grader.grade(query, docs))
          if score < 3:
               print("---DOCUMENT NOT RELEVANT---")
               return {"next": "transform", **state}
          else:
               print("---Document relevant---")
               return {"next": "RAG_generator", **state}

     def _generate_response(self, state: AgentState) -> Dict:
          print("\n---------Generating--------------")
          docs = state["retrieved_docs"]
          query = state["current_query"]
          state["limit"] +=1
          response = self.serve.__call__(query, docs)
          if state['limit'] >= 3:
               return{
                    "next": "finish",
                    **state,
                    "final_response": response
               }
          else:
               return {
                    "next": "check_answer",
                    **state,
                    "final_response": response
               }
     
     def _decide_generate_response(self, state: AgentState) -> Dict:
          print("\n---Grading Answer---")
          query = state["current_query"]
          answer = state["final_response"]
          answer_score = int(self.answer_grader.grade(query, answer))

          if answer_score >= 3 or state["limit"] >=3:
               return {"next": "finish", **state}
          else:
               return {"next": "transform", **state}
               

     def _transform_query(self, state: AgentState) -> Dict:
          print("\n------------Transform Query-------------")
          enhanced_query = self.transformation.enhancing_query(state["current_query"])
          sub_queries = self.transformation.decomposition_query(enhanced_query)
          return {
               "next": "retrieve",
               **state,
               "current_query": enhanced_query,
               "sub_queries": sub_queries
          }
     
     def SQL_retrive(self, state: AgentState):
          print("---------Retrive with SQL query-----------")
          query = state["current_query"]
          docs = []
          docs.append(self.sql_constructor.run(query))
          
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
        question = state['current_query']
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

          #add all node into Graph
          workflow.add_node("router", self.route_query)
          workflow.add_node("RAG_retrieve", self._retrieve_documents)
          workflow.add_node("grade_docs", self._grade_docs)
          workflow.add_node("RAG_generator", self._generate_response)
          workflow.add_node("check_answer", self._decide_generate_response)
          workflow.add_node("transform", self._transform_query)
          workflow.add_node('SQL_retrieve', self.SQL_retrive)
          workflow.add_node('SQL_generator', self.SQL_generator)
          workflow.add_node('websearching', self.websearch)
          workflow.add_node('websearch_generator', self.websearch_generator)
     
          #Add edges for RAG Agent 
          workflow.add_edge(START, "router")
          workflow.add_conditional_edges(
               "router",
               lambda x: x["next"],
               {
                    "RAG_retrive": "RAG_retrieve",
                    "SQL": "SQL_retrieve",
                    "websearching": "websearching"
               },
          )

          workflow.add_edge("RAG_retrieve", "grade_docs")
          
          workflow.add_conditional_edges(
               "grade_docs",
               lambda x: x["next"],
               {
                    "transform": "transform",
                    "generate": "RAG_generator",
               },
          )
          workflow.add_conditional_edges(
               "RAG_generator", 
               lambda x: x["next"],
               {
                    "finish": END,
                    "check_answer": "check_answer"
               }
          )
          workflow.add_edge("transform", "RAG_retrieve")

          workflow.add_conditional_edges(
               "check_answer",
               lambda x: x["next"],
               {
                    "transform": "transform",
                    "finish": END
               },
          )

          #Add edges for SQL Agent
          workflow.add_edge("SQL_retrieve", "SQL_generator")
          workflow.add_edge("SQL_generator", END)

          #Add edges for websearching Agent
          workflow.add_edge("websearching", "websearch_generator")
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
               "current_query": "",
               "sub_queries": [],
               "retrieved_docs": [],
               "final_response": None,
               "limit" : 0
          }
          
          try:
               final_state = workflow.invoke(initial_state)
               return final_state["final_response"] or "No response generated"
          except Exception as e:
               print(f"Error during execution: {e}")
               return f"An error occurred: {str(e)}"

if __name__ == "__main__":         
     agent = AdaptiveAgent()
     agent.display()
     # query = "Chỉ tiêu tuyển sinh đại học Nguyễn Tất Thành 2022?"
     # answer = agent.run(query)
     # print(answer)