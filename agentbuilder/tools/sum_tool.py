# type: ignore
from pathlib import Path
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def sum_tool(a: int, b: int):
 """Calculates the sum of 2 inputs."""
 return a + b

sum_tool.name="sum_operation"
sum_tool.description="calculates sum"

class sum_inputs(BaseModel):
   a: int = Field(description="First input")
   b: int = Field(description="Second input")

sum_tool.args_schema = sum_inputs
sum_tool.metadata= {"file_path": str(Path(__file__).absolute())}
