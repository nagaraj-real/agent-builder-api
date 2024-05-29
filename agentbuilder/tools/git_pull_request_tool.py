from pathlib import Path
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import requests

def git_pull_request_diff(url: str):
   """Provides the code diff for a pull request"""
   if url:
      res = requests.get(url+".diff")
      if res.content:
         return res.content.decode("utf-8")
   return ""
   
git_pull_request_diff_tool = StructuredTool.from_function(
    func=git_pull_request_diff,
    name="git_pull_request_diff_tool",
    description="Provides the code diff for a pull request",
    metadata= {"file_path": str(Path(__file__).absolute())}
    
)

class GitPullRequestDiffInputs(BaseModel):
   url: str = Field(description="url of the pull request")

git_pull_request_diff_tool.args_schema = GitPullRequestDiffInputs


