from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from Serve import Serve
from websearch import WebSearching
from typing_extensions import TypedDict
from IPython.display import display, Image


class AgentState(TypedDict):
     message: str
     retrieved_docs: List[Any]
     final_response: Optional[str]

class WebSearchingAgent:
     def  __init__(self):
          self.searcher = WebSearching()
          self.serve = Serve()
     
     def websearch(self, state: AgentState) -> Dict:
        print("-------Web Searching---------")
        question = state["message"]
        search_results = self.searcher.search(question)
        
        return {
            "next": "generate",
            **state,
            "retrieved_docs": search_results
        }
     def generate_websearching(self, state: AgentState) -> dict:
          print("\n---------Generating--------------")
          docs = state["retrieved_docs"]
          question = state["message"]
          response = self.serve.run(question, docs)
          
          return {
               "next": "finish",
               **state,
               "final_response": response
          }
     
     def _create_workflow(self):
          workflow = StateGraph(AgentState)

          workflow.add_node("search", self.websearch)
          workflow.add_node("generate", self.generate_websearching)

          workflow.add_edge(START, "search")
          workflow.add_edge("search", "generate")
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

if __name__ == "__main__":   
     agent = WebSearchingAgent()
     agent.display()
     query = "Chủ tịch Hồ Chí Minh sinh năm bao nhiêu"
     print(agent.run(query))