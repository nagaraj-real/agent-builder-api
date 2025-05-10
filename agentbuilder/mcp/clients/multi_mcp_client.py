
from langchain_mcp_adapters.client import MultiServerMCPClient
from agentbuilder.logger import uvicorn_logger as logger
import sys
from pathlib import Path


current_dir = Path(__file__).parent.parent
mcp_servers={
                    "math": {
                        "command": sys.executable,
                        "args": [f"{current_dir}\\servers\\math.py"],
                        "transport": "stdio",
                    },
                    "weather":{
                         "command": sys.executable,
                        "args": [f"{current_dir}\\servers\\weather.py"],
                        "transport": "stdio",
                    }
                }

async def get_multi_mcp_client()->MultiServerMCPClient:
   
    async with MultiServerMCPClient(
                mcp_servers
            ) as client:
        try:
            return client
        except Exception as exc:
            print(exc)
            logger.error(f"Error: {str(exc)}")
            raise exc


async def invoke_mcp_client(params,callback)->MultiServerMCPClient:
    async with MultiServerMCPClient(
                 mcp_servers
            ) as client:
        try:
           res=await callback(params,client)
           return res
        except Exception as exc:
            print(exc)
            logger.error(f"Error: {str(exc)}")
            raise exc


