from pathlib import Path
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field



internet_search = TavilySearchResults()
internet_search.name = "internet_search"
internet_search.description = "Returns a list of relevant document snippets for a textual query retrieved from the internet."


class TavilySearchInput(BaseModel):
   query: str = Field(description="Query to search the internet with")

internet_search.args_schema = TavilySearchInput
internet_search.metadata= {"file_path": str(Path(__file__).absolute())}