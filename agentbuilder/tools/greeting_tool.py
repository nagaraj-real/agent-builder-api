# type: ignore
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from pathlib import Path

@tool
def greeting_tool(name:str):
 """Response for the user when they greet."""
 return f"Hello {name or "guest"}, I can use my existing knowledge and tools to answer your questions. Infact, I am currently using a tool 'Hello World' "

greeting_tool.name="greeting_tool"
greeting_tool.description="Response for the user when they greet."

class HelloWorldInput(BaseModel):
   name: str = Field(description="Name of the user")

greeting_tool.args_schema = HelloWorldInput
greeting_tool.metadata= {"file_path": str(Path(__file__).absolute())}