from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from pydantic import BaseModel
from Grader import RetrievalGrader, HallucinationGrader, AnswerGrader
from QueryRouter import QueryRouter
from QueryTransformation import QueryTransformation
from Retrieval import UniversityRetrievalStrategy
from Serve import Serve
from websearch import WebSearching
from typing_extensions import TypedDict

class AgentState(TypedDict):
    """Represents the state of our agent during execution"""
    message: str
    current_query: str
    sub_queries: List[str]
    retrieved_docs: List[Any]
    final_response: Optional[str]

class AdaptiveAgent:
    def __init__(self):
        self.router = QueryRouter()
        self.transformation = QueryTransformation()
        self.serve = Serve()
        self.retriever = UniversityRetrievalStrategy()
        self.retriever_grader = RetrievalGrader()
        self.hallucinationGrader = HallucinationGrader()
        self.answer_grader = AnswerGrader()
        self.searcher = WebSearching()
    
    def _route_query(self, state: AgentState) -> Dict:
        state["current_query"] = state["message"]
        routing_result = self.router.classify(state["current_query"])
        
        if routing_result.datasource == "vectorstore":
            print("Route question to vectorstore")
            return {"next": "vectorstore", **state}
        else:
            print("Route question to web_search")
            return {"next": "web_search", **state}
    
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
        if score < 5:
            print("---DOCUMENT NOT RELEVANT---")
            return {"next": "transform", **state}
        else:
            print("---Document relevant---")
            return {"next": "generate", **state}

    def _generate_response(self, state: AgentState) -> Dict:
        print("\n---------Generating--------------")
        docs = state["retrieved_docs"]
        query = state["current_query"]
        response = self.serve.__call__(query, docs)
        
        return {
            "next": "check_hallucination",
            **state,
            "final_response": response
        }
    
    def _decide_generate_response(self, state: AgentState) -> Dict:
        print("\n---Hallucination process---")
        query = state["current_query"]
        answer = state["final_response"]
        docs = state["retrieved_docs"]
        
        hallucination = self.hallucinationGrader.grade(query, answer, docs)
        if hallucination == "no":
            return {"next": "generate", **state}
        else:
            answer_grader = self.answer_grader.grade(query, answer)
            if answer_grader == "yes":
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
    
    def websearch(self, state: AgentState) -> Dict:
        question = state["current_query"]
        search_results = self.searcher.search(question)
        
        return {
            "next": "generate",
            **state,
            "retrieved_docs": search_results
        }
    
    def _create_workflow(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("route", self._route_query)
        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("grade_docs", self._grade_docs)
        workflow.add_node("generate", self._generate_response)
        workflow.add_node("check_hallucination", self._decide_generate_response)
        workflow.add_node("transform", self._transform_query)
        workflow.add_node("websearch", self.websearch)
        
        workflow.add_edge(START, "route")
        workflow.add_conditional_edges(
            "route",
            lambda x: x["next"],
            {
                "web_search": "websearch",
                "vectorstore": "retrieve",
            },
        )
        workflow.add_edge("websearch", "generate")
        workflow.add_edge("retrieve", "grade_docs")
        workflow.add_conditional_edges(
            "grade_docs",
            lambda x: x["next"],
            {
                "transform": "transform",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform", "retrieve")
        workflow.add_conditional_edges(
            "check_hallucination",
            lambda x: x["next"],
            {
                "generate": "generate",
                "transform": "transform",
                "finish": END
            },
        )
        
        return workflow.compile()
    
    def run(self, query: str) -> str:
        workflow = self._create_workflow()
        initial_state = {
            "message": query,
            "current_query": "",
            "sub_queries": [],
            "retrieved_docs": [],
            "final_response": None
        }
        
        try:
            final_state = workflow.invoke(initial_state)
            return final_state["final_response"] or "No response generated"
        except Exception as e:
            print(f"Error during execution: {e}")
            return f"An error occurred: {str(e)}"
        
agent = AdaptiveAgent()
query = "Tuyển sinh đại học Tôn Đức Thắng 2024"
answer = agent.run(query)
print(answer)