from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

_search = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the web for facts, statistics, and sources to support arguments."""
    print(f"  🔍 [Search] {query}")
    try:
        return _search.invoke(query)
    except Exception as e:
        return f"Search failed: {str(e)}"
