# type: ignore
from pathlib import Path
from langchain_core.tools import tool

@tool
def directly_answer_tool() -> str:
 """"Directly answer"""
 return ""

directly_answer_tool.name="directly_answer"
directly_answer_tool.description="Model can provide direct answers"
directly_answer_tool.metadata= {"file_path": str(Path(__file__).absolute())}