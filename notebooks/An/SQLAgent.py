from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from Serve import Serve
from typing_extensions import TypedDict
from IPython.display import display, Image
from QueryToSQL import SQL_Constructor

class AgentState(TypedDict):
     message: str
     retrieved_docs: List[Any]
     final_response: Optional[str]

class SQLAgent:
     def __init__(self):
          self.sql_constructor = SQL_Constructor()
          self.serve = Serve()

     def retrive_docs(self, state: AgentState):
          print("---------Retrive with SQL query-----------")
          query = state['message']
          docs = []
          docs.append(self.sql_constructor.run(query))
          
          return {
               "next": "generate",
               **state,
               "retrived_docs": docs
          }
     
     def generate(self, state: AgentState):
          print("---------Generating-----------")
          docs = state['retrieved_docs']
          query = state['message']
          response = self.serve.run(query, docs)

          return {
               "next": "finish",
               **state,
               "final_response": response
          }

     def _create_workflow(self):
          workflow = StateGraph(AgentState)

          workflow.add_node("retrive", self.retrive_docs)
          workflow.add_node("generate", self.generate)

          workflow.add_edge(START, "retrive")
          workflow.add_edge("retrive", "generate")
          workflow.add_edge("generate", END)
          
          return workflow.compile()     
     
     def display(self):
        workflow = self._create_workflow()
        with open("websearch_agent.png", 'wb') as f:
            f.write(workflow.get_graph().draw_mermaid_png())
        
     
     def run(self, query: str) -> str:
        workflow = self._create_workflow()
        initial_state = {
            "message": query,
            "retrieved_docs": [],
        }
        
        try:
            final_state = workflow.invoke(initial_state)
            return final_state["final_response"] or "No response generated"
        except Exception as e:
            print(f"Error during execution: {e}")
            return f"An error occurred: {str(e)}"
        
agent = SQLAgent()
agent.display()
# query = "Điểm chuẩn THPT ngành Công Nghệ Thông Tin đại học Tôn Đức Thắng 2021"
# print(agent.run(query))