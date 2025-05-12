from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lancedb.rerankers import LinearCombinationReranker
from langchain_community.vectorstores import LanceDB
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults

from data_models.models import RagToolSchema

@tool(args_schema=RagToolSchema)
def retriever_tool(question):
    """retriever tool"""
    return ""


@tool(args_schema=RagToolSchema)
def tavily_tool(question:str):
    """tavily tool"""
    return TavilySearchResults(question,
                               max_results = 5,
                               serch_Depth = "advanced",
                               include_answer = True,
                               include_raw_content = True,)



@tool
def create_polygon_tool():
    """polygon tool"""
    return PolygonFinancials(api_wrapper=PolygonAPIWrapper())


@tool## converts this function to langchain tool so that we can invoke this method/function
def create_bing_tool():
    """bing tool"""
    return BingSearchResults()


def get_all_tool(question):
    return [retriever_tool(question),
            tavily_tool,
            create_polygon_tool,
            create_bing_tool
            ]

if __name__ == "__main__":
    print(get_all_tool("my question"))