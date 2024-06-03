

from agentbuilder.agents.BaseAgentBuilder import AgentBuilderParams, BaseAgentBuilder
from agentbuilder.agents.params import AgentParams
from agentbuilder.factory.tool_factory import greeting_tool,temperature_sensor_tool,weather_clothing_tool,temperature_tool
from agentbuilder.factory.tool_factory import  git_pull_request_diff_tool,sum_tool,json_tools
from agentbuilder.tools.repl_tool import repl_tool
from agentbuilder.helper.env_helper import get_default_agent_type


def default_agent():
    return AgentParams(name="default_agent",
            preamble= "You are a greeter assistant withh access to greeting tool",
            tools= [greeting_tool],
            agent_type= get_default_agent_type()
    )

def weather_agent():
    return AgentParams(
            name="weather_agent",
            preamble= "You are a powerful weather assistant with access to weather tools",
            tools= [temperature_tool,temperature_sensor_tool,weather_clothing_tool],
            agent_type= get_default_agent_type()
    )

def python_agent():
     return AgentParams(
            name="python_agent",
            tools= [repl_tool],
            agent_type= get_default_agent_type()
     )

def sum_agent():
     return AgentParams(
            name="sum_agent",
            preamble= "You are a powerful assistant with access to tools that help you calculate sum of 2 numbers",
            tools= [sum_tool],
            agent_type= get_default_agent_type()
     )

def rest_api_agent():
     return AgentParams(
            name="rest_api_agent",
            preamble= "You are a powerful assistant with access to json openapi tools",
            tools= json_tools,
            agent_type= get_default_agent_type()
     )


def git_agent():
      return AgentParams(
            name="git_agent",
            preamble= """You are very powerful code assistant,with access to various git tools, using them to come up with simple solutions. 
            One such solution is to provide Pull request message
            Prompt the user to enter pull request url if not given
            """,
            tools=  [git_pull_request_diff_tool],
            agent_type= get_default_agent_type()
      )


def get_all_agents():
    return [
            default_agent(),
            weather_agent(),
            git_agent(),
            sum_agent(),
            rest_api_agent(),
            python_agent(),

    ]

def get_agent_builder(params:AgentBuilderParams):
    agent_name= params.name
    match agent_name:
        case "graph_agent":
            from agentbuilder.agents.BaseGraphAgentBuilder import BaseGraphAgentBuilder
            return BaseGraphAgentBuilder(params)
        case _:
            return BaseAgentBuilder(params)






