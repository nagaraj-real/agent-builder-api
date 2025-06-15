
import asyncio
from agentbuilder.db import pesist_db
from agentbuilder.factory.tool_factory import get_all_tools
from agentbuilder.factory.agent_factory import get_all_agents
from agentbuilder.logger import uvicorn_logger as logger

async def migrate_to_db():
        try:
            code_agents = {params.name:params  for params in get_all_agents()}
            pesist_db.set_code_agents(code_agents)
            all_tools = get_all_tools()
            await pesist_db.update_tools(all_tools)
            await pesist_db.update_agents()
        except Exception as exc:
            logger.error(f"Error: {str(exc)}")

def migrate():
      asyncio.run(migrate_to_db())


if __name__ == "__main__":
   migrate()