from pathlib import Path
import subprocess
from langchain_core.tools import StructuredTool

def git_diff():
   """provides the staged code diff just before commit"""
   process= subprocess.run(["git", "diff","--cached"],capture_output=True)
   if process.stdout:
      return process.stdout.decode("utf-8")
   else:
      return ""
   
git_diff_tool = StructuredTool.from_function(
    func=git_diff,
    name="git_diff_tool",
    description="Provides the staged code diff just before commit",
)

git_diff_tool.name="git_diff_tool"
git_diff_tool.description="provides the staged code diff just before commit"
git_diff_tool.metadata= {"file_path": str(Path(__file__).absolute())}


