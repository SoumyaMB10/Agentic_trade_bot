from typing_extensions import TypedDict, Annotated
from langgraph .graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from utils.model_loader import ModelLoader
from toolkit.tools import *


class State(TypedDict):
    messages: Annotated[list, add_messages]

class Graphbuilder:

    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = [retriever_tool, financials_tool, tavilytool]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.graph = None


    def _chatbot_node(self, state:State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    def build(self):
        graph_builder = StateGraph(State)

        graph_builder.add_node("chatbot",self._chatbot_node)

        tool_node = ToolNode(tools= self.tools)
        graph_builder.add_node("tools",tool_node)

        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")
        
        self.graph = graph_builder.compile()


    def get_graph(self):
        if self.graph is None:
            raise ValueError("Graph not built")
        return self.get_graph