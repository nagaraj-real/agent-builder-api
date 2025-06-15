from mcp import types
from agentbuilder.mcp import get_mcp_client


def get_all_prompts()->list[types.Prompt]:
    mcp_client= get_mcp_client()
    return mcp_client.mcp_prompts
