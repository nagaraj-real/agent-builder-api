
from langchain_mcp_adapters.client import MultiServerMCPClient
from agentbuilder.logger import uvicorn_logger as logger
import sys
from pathlib import Path


current_dir = Path(__file__).resolve().parent.parent

mcp_servers = {
    "math": {
        "command": sys.executable,
        "args": [str(current_dir / "servers" / "mcp_math.py")],
        "transport": "stdio",
    },
    "weather": {
        "command": sys.executable,
        "args": [str(current_dir / "servers" / "weather.py")],
        "transport": "stdio",
    },
     "openvibe": {
        "command": sys.executable,
        "args": [str(current_dir / "servers" / "openvibe.py")],
        "transport": "stdio",
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "DEFAULT_MINIMUM_TOKENS": "6000"
      }
    }
}

async def get_multi_mcp_client()->MultiServerMCPClient:
   
    async with MultiServerMCPClient(
                mcp_servers
            ) as client:
        try:
            return client
        except Exception as exc:
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
            logger.error(f"Error: {str(exc)}")
            raise exc


