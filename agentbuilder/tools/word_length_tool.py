# type: ignore
from pathlib import Path
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def word_length_tool(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

word_length_tool.name="word_length_operation"
word_length_tool.description="calculates word length"

class word_length_inputs(BaseModel):
   a: int = Field(description="The word")

word_length_tool.args_schema = word_length_inputs
word_length_tool.metadata= {"file_path": str(Path(__file__).absolute())}