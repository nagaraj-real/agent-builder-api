from pathlib import Path
from agentbuilder.agents.BaseNemoGuardRailsBuilder import BaseNemoGuardRailsBuilder
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

class MathAgentBuilder(BaseNemoGuardRailsBuilder):
    guardrails = None 
    config:RailsConfig = None
    def __init__(self,params):
        super().__init__(params=params)
        config = RailsConfig.from_path(str(Path(__file__).parent)+"./config")
        self.guardrails = RunnableRails(config,llm=self.builder_params.chat_llm,tools=self.builder_params.tools,verbose=True)