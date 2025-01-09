from typing import Dict, List, Optional, Any, Union
from langgraph.graph import END, StateGraph, START
from pydantic import BaseModel
from Grader import RetrievalGrader, HallucinationGrader, AnswerGrader
from QueryRouter import QueryRouter
from QueryTransformation import QueryTransformation
from Retrieval import UniversityRetrievalStrategy
from Serve import Serve
from websearch import WebSearching

class AgentState(BaseModel):
    """Represents the state of our agent during execution"""
    message: str
    current_query: str = ""  # Initialize with default value
    sub_queries: List[str] = []
    retrieved_docs: List[Any] = []
    final_response: Optional[str] = None

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
    
    def _route_query(self, state: AgentState) -> str:
        state.current_query = state.message
        routing_result = self.router.classify(state.current_query)
        if routing_result.datasource == "vectorstore":
            print("Route question to vectorstore")
            return "vectorstore"
        elif routing_result.datasource == "web_search":
            print("Route question to web_search")
            return "web_search"
    
    def _retrieve_documents(self, state: AgentState) -> str:
        print("-----Retrieving Process-----")
        all_docs = []
        queries = state.sub_queries if state.sub_queries else [state.current_query]
        for query in queries:
            docs = self.retriever.retrieve(query)
            all_docs.extend(docs)
        state.retrieved_docs = all_docs
        return "grade_docs"  # Changed from grade_document to match node name
    
    def _grade_docs(self, state: AgentState) -> str:
        print("------Check document relevance to question------")
        query = state.current_query
        docs = state.retrieved_docs
        if self.retriever_grader(query, docs) < 5:
            print("---DOCUMENT NOT RELEVANT---")
            return "transform"
        else:
            print("---Document relevant---")
            return "generate"

    def _generate_response(self, state: AgentState) -> str:
        print("----Generating-----")
        docs = state.retrieved_docs
        query = state.current_query
        response = self.serve.__call__(query, docs)
        state.final_response = response
        return "check_hallucination"  # Changed from hallucinations to match node name
    
    def _decide_generate_response(self, state: AgentState) -> str:
        print("---Hallucination process---")
        query = state.current_query
        answer = state.final_response
        docs = state.retrieved_docs
        hallucination = self.hallucinationGrader.grade(query, answer, docs)
        if hallucination == "no":
            return "generate"
        else:
            answer_grader = self.answer_grader.grade(query, answer)
            if answer_grader == "yes":
                return "finish"
            else:
                return "transform"

    def _transform_query(self, state: AgentState) -> str:
        enhanced_query = self.transformation.enhancing_query(state.current_query)
        state.current_query = enhanced_query
        sub_queries = self.transformation.decomposition_query(enhanced_query)
        state.sub_queries = sub_queries
        return "retrieve"
    
    def websearch(self, state: AgentState) -> str:
        question = state.current_query
        state.retrieved_docs = self.searcher.search(question)
        return "generate"  # Changed from finish to match flow
    
    def _create_workflow(self):  # Removed state parameter
        workflow = StateGraph(AgentState)  # Changed to use AgentState class

        workflow.add_node("route", self._route_query)
        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("grade_docs", self._grade_docs)
        workflow.add_node("generate", self._generate_response)
        workflow.add_node("check_hallucination", self._decide_generate_response)
        workflow.add_node("transform", self._transform_query)
        workflow.add_node("websearch", self.websearch)
        workflow.add_edge(START, "route")
        # Fixed edges syntax
        workflow.add_conditional_edges(
            "route",
            self._route_query,
            {
                "web_search": "websearch",
                "vectorstore": "retrieve",
            }
        )
        workflow.add_edge("websearch", "generate")
        workflow.add_edge("retrieve", "grade_docs")
        workflow.add_conditional_edges(
            "grade_docs",
            self._grade_docs,
            {
                "transform": "transform",
                "generate": "generate",
            }
        )
        workflow.add_edge("transform", "retrieve")
        workflow.add_conditional_edges(
            "generate",
            self._decide_generate_response,
            {
                "generate": "generate",
                "transform": "transform",
                "finish": END
            }
        )
        
        return workflow.compile()

    