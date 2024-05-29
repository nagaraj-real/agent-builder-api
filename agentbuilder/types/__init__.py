from pydantic import BaseModel


class ChatRequest(BaseModel):
    chatId: str| None= None
    query: str = ""
    agentName: str|None= None
    stream:bool|None=False

class ErrorResponse(BaseModel):
    error: str| None= None

class ChatResponse(BaseModel):
    chatId: str| None= None
    chatResponse: str | None = None

class AgentData(BaseModel):
    name: str
    tools: list[str]
    preamble: str|None=None
    source_type: str|None = "ui"
    agent_type:str|None = "tool_calling"


class ToolData(BaseModel):
    name: str
    description: str
    metadata: dict|None
    params: dict|None