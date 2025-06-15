

from agentbuilder.mcp.clients.multi_mcp_client import mcp_servers
from langchain_mcp_adapters.client import MultiServerMCPClient
from agentbuilder.logger import uvicorn_logger as logger

mcp_client=None

def get_mcp_client():
     return mcp_client

async def initialize_mcp_client():
    global mcp_client
    mcp_client= MCPClient()
    await mcp_client.initialize()
    return mcp_client

class MCPClient:

    def __init__(self):
            self.mcp_tools=[]
            self.mcp_prompts=[]

    async def initialize(self):
        async with MultiServerMCPClient(
                mcp_servers
            ) as client:
            try:
                server_name_to_tools= client.server_name_to_tools
                self.mcp_tools= [setattr(tool, 'metadata',{"mcp_server": name}) or tool  for name, tools in server_name_to_tools.items() for tool in tools]
                for name,session in client.sessions.items():
                    try:
                        all_prompts= await session.list_prompts()
                        if all_prompts:
                            for mcp_prompt in all_prompts.prompts:
                                content=await session.get_prompt(mcp_prompt.name)
                                message=next(message for message in content.messages if message.role=="user")
                                mcp_prompt.content=message.content.text if message else ""
                            self.mcp_prompts= self.mcp_prompts + all_prompts.prompts
                    except Exception as exc:
                         print(exc)

            except Exception as exc:
                logger.error(f"Error: {str(exc)}")
                raise exc
        
