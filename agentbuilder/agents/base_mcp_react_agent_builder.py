from langgraph.prebuilt import create_react_agent
from agentbuilder.agents.agent_tracer import PrintFileCallbackHandler
from agentbuilder.agents.params import AgentBuilderParams
from agentbuilder.agents.prompt_helper import get_default_agent_prompt, get_image_agent_prompt,get_react_agent_prompt
from agentbuilder.llm import chat_llm as default_llm
from langchain_core.messages import AIMessage,ToolMessage,BaseMessage,HumanMessage
from langchain_core.agents import AgentAction

from agentbuilder.mcp.clients.multi_mcp_client import invoke_mcp_client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.callbacks.tracers import ConsoleCallbackHandler



class BaseMCPReactAgentBuilder:

    chat_llm=None
    intermediate_steps=[]
    def __init__(self,params:AgentBuilderParams):
        self.builder_params=params
        self.intermediate_steps=[]
        self.chat_llm = self.builder_params.chat_llm or default_llm

    def compile(self,client:MultiServerMCPClient|None):
        mcp_tools= [] if client is None else client.get_tools()
        tools=[]
        for tool in self.builder_params.tools:
            if  tool.metadata and tool.metadata.get("mcp_server") is not None:
                for mcp_tool in mcp_tools:
                    if mcp_tool.name == tool.name:
                        tools.append(mcp_tool)
            else:
                tools.append(tool)
        self.builder_params.tools=tools
        agent = create_react_agent(model=self.chat_llm,tools=self.builder_params.tools)
        return agent
    
    def convert_messages_to_steps(self,messages: list[BaseMessage]):
        for message in messages:
            if isinstance(message,AIMessage) and message.tool_calls:
                for tool in message.tool_calls:
                    self.intermediate_steps.append({"tool_call_id":tool['id'],"tool":tool["name"],"tool_input":tool["args"],"tool_output":""})
            if isinstance(message,ToolMessage):
                t = next((item for item in self.intermediate_steps if item['tool_call_id'] == message.tool_call_id),None)
                if t is not None:
                    t['tool_output'] = message.content

       
        return [(AgentAction(tool=step["tool"],
                             tool_input=step["tool_input"],log=""),
                             step["tool_output"]) for step in self.intermediate_steps]

    
    def input_parser(self,params):
        preamble = self.builder_params.preamble
        input = params["input"]
        chat_history= params["chat_history"]
        if "image_data" in params and params["image_data"]:
            image_data= params["image_data"]
            prompt = get_image_agent_prompt(preamble)
            human_msg= HumanMessage(
            content=[
                {"type": "text", "text": "{input}"},
                {
                    "type": "image",
                    "source_type": "base64",
                    "data": image_data.base64,
                    "mime_type": image_data.mimeType,
                 } 
            ])
            messages = prompt.format_messages(input=input,
                                              chat_history=chat_history,
                                              human_msg=[human_msg])
        else:
            prompt = get_default_agent_prompt(preamble)
            messages = prompt.format_messages(input=input,chat_history=chat_history)
        return {"messages":messages}
    
    def get_intermediate_steps(self,messages=[]):
        return self.convert_messages_to_steps(messages)
    
    def astream(self,params):
        self.intermediate_steps=[]
        response= self.amcpstream(params,None)
        return response
    
    def amcpstream(self,params,client:MultiServerMCPClient|None):
        runnable=  self.compile(client)
        response= runnable.astream(self.input_parser(params),stream_mode="updates")
        async def gen():
            async for output in response:
                for _, value in output.items():
                    if "messages" in value:
                        _=self.get_intermediate_steps(value["messages"])
                    output_dict= self.message_output_parser(value)
                    if(output_dict):
                        yield output_dict
            steps=[(AgentAction(tool=step["tool"],
                             tool_input=step["tool_input"],log=""),
                             step["tool_output"]) for step in self.intermediate_steps]
            yield {"intermediate_steps":steps}
        return gen()
    
    def message_output_parser(self,messages_dict:dict):
         if "messages" in messages_dict:
            messages = messages_dict['messages']
            if messages and isinstance(messages[-1],AIMessage):
                message:AIMessage=messages[-1]
                return {"output":message.content}

    async def ainvokemcp(self,params,client:MultiServerMCPClient):
        runnable=  self.compile(client)
        response = await runnable.ainvoke(self.input_parser(params), config={"callbacks": [PrintFileCallbackHandler()],"recursion_limit":50})
        messages_dict = response
        parsed_response = self.message_output_parser(messages_dict)
        parsed_response["intermediate_steps"] = self.get_intermediate_steps(messages_dict.get("messages",[]))
        return parsed_response
    
    async def ainvoke(self,params):
        self.intermediate_steps=[]
        return await invoke_mcp_client(params,self.ainvokemcp)
        
    def create_prompt(self):
        preamble= self.builder_params.preamble
        return get_react_agent_prompt(preamble)

