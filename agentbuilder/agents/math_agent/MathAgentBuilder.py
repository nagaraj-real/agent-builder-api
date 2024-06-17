from pathlib import Path
from agentbuilder.agents.base_nemo_guard_rails_builder import BaseNemoGuardRailsBuilder
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

class MathAgentBuilder(BaseNemoGuardRailsBuilder):
    guardrails = None 
    config:RailsConfig = None
    def __init__(self,params):
        super().__init__(params=params)
        config = RailsConfig.from_path(str(Path(__file__).parent)+"./config")
        self.guardrails = RunnableRails(config,llm=self.chat_llm,tools=self.builder_params.tools,verbose=True)