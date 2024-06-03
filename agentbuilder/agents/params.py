from dataclasses import dataclass
from langchain.tools import BaseTool
from typing import Callable, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from agentbuilder.helper.env_helper import get_default_agent_type

@dataclass
class AgentParams:
    name: str
    tools: list[BaseTool|str|Callable]
    preamble: str|None="You are very powerful assistant, with access to tools that can help you answer questions"
    source_type: Literal['code','ui'] = "code"
    agent_type: Literal['tool_calling','structured','react','json'] = get_default_agent_type()
    prompt: ChatPromptTemplate|None=None


@dataclass
class SerializedAgentParams:
    name: str
    tools: list[str]
    preamble: str|None="You are very powerful assistant, with access to tools that can help you answer questions"
    source_type: Literal['code','ui'] = "code"
    agent_type: Literal['tool_calling','structured','react','json'] = "tool_calling"

@dataclass
class AgentBuilderParams:
    name: str
    agent_type:Literal['tool_calling', 'structured', 'react', 'json']
    tools: list[BaseTool]
    preamble: str|None=""
    prompt:ChatPromptTemplate|None=None
    chat_llm:BaseChatModel|None= None
