from agentbuilder.agents.base_agent_builder import AgentBuilderParams, BaseAgentBuilder
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

def resume_vector_agent():
    return AgentParams(
            name="resume_vector_agent",
            preamble= """
            You are very powerful code assistant,with access to resume and job description tools.
            """,
            tools=  ["resume_search_tool","job_description_tool","save_skill_tool"],
            agent_type= get_default_agent_type()
      )

def rating_agent():
    return AgentParams(
            name="rating_agent",
            preamble= """
            You are very powerful interview rating assistant,with access to save rating tools.
            """,
            tools=  ["interview_answers_tool","save_rating_tool","save_evaluation_tool"],
            agent_type= get_default_agent_type()
      )

def interview_agent():
    return AgentParams(
            name="interview_agent",
            preamble= """
            You are very powerful interview preparation agent.
            """,
            tools=  [],
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
            resume_vector_agent(),
            rating_agent(),
            interview_agent()
    ]

def get_agent_builder(params:AgentBuilderParams):
    agent_name= params.name
    match agent_name:
        case "graph_agent":
            from agentbuilder.agents.base_graph_agent_builder import BaseGraphAgentBuilder
            return BaseGraphAgentBuilder(params)
        case "interview_agent":
            from agentbuilder.agents.interview.interview_agent import InterviewAgentBuilder
            return InterviewAgentBuilder(params)
        case "math_agent_guard":
            from agentbuilder.agents.math_agent import MathAgentBuilder
            return MathAgentBuilder.MathAgentBuilder(params)
        case "doctor_agent_guard":
            from agentbuilder.agents.doctor_agent import DoctorAgentBuilder
            return DoctorAgentBuilder.DoctorAgentBuilder(params)
        case _:
            return BaseAgentBuilder(params)





