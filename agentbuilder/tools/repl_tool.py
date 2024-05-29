from pathlib import Path
from langchain.agents import Tool
from pydantic.v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()
repl_tool = Tool(
   name="python_repl",
   description="Executes python code and returns the result. The code runs in astatic sandbox without interactive mode, so print output or save output to a file.",
   func=python_repl.run,
)
repl_tool.name = "python_interpreter"

# from langchain_core.pydantic_v1 import BaseModel, Field
class ToolInput(BaseModel):
   code: str = Field(description="Python code to execute.")


repl_tool.args_schema = ToolInput
repl_tool.metadata= {"file_path": str(Path(__file__).absolute())}