

from agentbuilder.agents.BaseAgentBuilder import AgentBuilderParams, BaseAgentBuilder
from agentbuilder.agents.params import AgentParams
from agentbuilder.factory.tool_factory import greeting_tool,temperature_sensor_tool,weather_clothing_tool,temperature_tool
from agentbuilder.tools.repl_tool import repl_tool

def default_agent():
    return AgentParams(name="default_agent",
            preamble= "You are a greeter assistant withh access to greeting tool",
            tools= [greeting_tool]
    )

def weather_agent():
    return AgentParams(
            name="weather_agent",
            preamble= "You are a powerful weather assistant with access to weather tools",
            tools= [temperature_tool,temperature_sensor_tool,weather_clothing_tool]
    )

def python_agent():
     return AgentParams(
            name="python_agent",
            tools= [repl_tool]
     )

def git_agent():
      return AgentParams(
            name="git_agent",
            preamble= "You are very powerful code assistant,with access to various git tools, using them to come up with simple solutions. One such solution is to provide commit message",
            tools=  ["git_diff_tool"]
      )


def get_all_agents():
    return [
            default_agent(),
            weather_agent(),
            python_agent(),
            git_agent()
    ]

def get_agent_builder(params:AgentBuilderParams):
    agent_name= params.name
    match agent_name:
        case "graph_agent":
            from agentbuilder.agents.BaseGraphAgentBuilder import BaseGraphAgentBuilder
            return BaseGraphAgentBuilder(params)
        case _:
            return BaseAgentBuilder(params)






