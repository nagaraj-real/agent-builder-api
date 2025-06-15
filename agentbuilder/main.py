from dotenv import load_dotenv
from agentbuilder.factory.prompt_factory import get_all_prompts
from agentbuilder.helper.env_helper import get_log_level
import uuid
from fastapi.exceptions import RequestValidationError
import uvicorn
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import JSONResponse,StreamingResponse
from langchain_core.messages import HumanMessage,BaseMessage,AIMessage
from agentbuilder.chat import chat,chat_stream
from agentbuilder.db import pesist_db
from agentbuilder.factory.tool_factory import get_all_tools
from agentbuilder.factory.agent_factory import get_all_agents
from agentbuilder.llm import load_chat_llm
from starlette.exceptions import HTTPException as StarletteHTTPException
from agentbuilder.mcp import initialize_mcp_client
from agentbuilder.types import AgentData, ChatRequest, ChatResponse, ToolData
from agentbuilder.logger import uvicorn_logger as logger

log_level = get_log_level()

async def migrate_to_db():
        try:
            await initialize_mcp_client()
            code_agents = {params.name:params  for params in get_all_agents()}
            pesist_db.set_code_agents(code_agents)
            all_tools = get_all_tools()
            await pesist_db.update_tools(all_tools)
            await pesist_db.update_agents()
        except Exception as exc:
            raise exc

@asynccontextmanager
async def lifespan(app: FastAPI):
   load_dotenv(override=True)
   load_chat_llm()
   await migrate_to_db()
   yield

app = FastAPI(lifespan=lifespan)
chat_memory_dict:dict[str,list[BaseMessage]]={}


def retrieveOrCreateChatMemory(chat_id:str,query:str):
    memory= chat_memory_dict.get(chat_id)
    if memory:
        return memory
    else:
        memory = []
        chat_memory_dict[chat_id]=memory
        return memory
    

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"Error: {str(exc)}")
    return JSONResponse({"error":str(exc)}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Error: {str(exc)}")
    return JSONResponse({"error":str(exc)}, status_code=400)

    
@app.get("/api/healthz")
def health():
    return "healthy"

@app.post("/api/chat")
async def post_chat(chat_query:ChatRequest)->ChatResponse:
    chat_id = str(uuid.uuid1()) if chat_query.chatId is None else chat_query.chatId
    chat_history = retrieveOrCreateChatMemory(chat_id,chat_query.query)
    response= await chat(chat_query.query,chat_history,chat_query.agentName,chat_query.imageData)
    chat_history.extend([HumanMessage(content=chat_query.query),AIMessage(content=response)])
    chat_response = ChatResponse(chatResponse=response,chatId=chat_id)
    logger.debug(f"Chat Response: {chat_response}")
    return chat_response
    
@app.post("/api/chat/stream")
async def post_chat_stream(chat_query:ChatRequest)->StreamingResponse:
    chat_id = str(uuid.uuid1()) if chat_query.chatId is None else chat_query.chatId
    chat_history = retrieveOrCreateChatMemory(chat_id,chat_query.query)
    async def gen()->AsyncGenerator:
        try:
            final_output=""
            response= await chat_stream(chat_query.query,chat_history,chat_query.agentName,chat_query.imageData)
            yield chat_id
            async for payload in response:
                time.sleep(0.01)
                if "output" in payload:
                    final_output += payload["output"]
                    yield final_output
            chat_history.extend([HumanMessage(content=chat_query.query),AIMessage(content=final_output)])
            logger.debug(f"Chat Response: {final_output}")
        except Exception as exc:
            logger.error(f"Error: {str(exc)}")
            yield "ERROR"
    return StreamingResponse(gen())
    
@app.get("/api/agents")
async def get_agents()-> dict|dict[str,AgentData]:
    agents= await pesist_db.get_agents()
    return agents
    
@app.get("/api/steps")
async def get_agents_steps():
    agents= await pesist_db.get_steps()
    return agents
    
@app.post("/api/agents")
async def save_agents(agentsWithParams:list[AgentData]):
    agents= {params.name:params for params in agentsWithParams}
    await pesist_db.update_agents(agents)
    return JSONResponse({"data": "Agent Saved"})
    
@app.get("/api/tools")
async def get_tools()->dict[str,ToolData]:
    tools= await pesist_db.get_tools()
    return tools

@app.get("/api/prompts")
async def get_prompts()->list:
    return get_all_prompts()
    
@app.delete("/api/chatHistory/{chat_id}")
def deleteChatHistory(chat_id:str):
    chat_history= chat_memory_dict.get(chat_id)
    if chat_history:
        del chat_history
        return JSONResponse({"chatResponse": f"{chat_id} deletion complete"})
    else:
        return JSONResponse({"chatResponse": f"{chat_id} not found to delete"},status_code=404)

def start_api():
    uvicorn.run("agentbuilder.main:app", host="0.0.0.0", port=8080,workers=1,reload=False,log_level=log_level)

if __name__ == "__main__":
    start_api()