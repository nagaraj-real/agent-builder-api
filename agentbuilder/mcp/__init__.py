

from agentbuilder.mcp.clients.multi_mcp_client import get_multi_mcp_client


async def get_mcp_client():
    client = await get_multi_mcp_client()
    return client