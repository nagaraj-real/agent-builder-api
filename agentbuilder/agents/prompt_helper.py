from langchain import hub
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate

def get_default_agent_prompt(preamble=None):
    return ChatPromptTemplate.from_messages(
    [
        (
            "system",
            preamble or "You are a helpful assistant. Make use of the tools available.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

def get_structured_agent_prompt(preamble):
    prompt = hub.pull("hwchase17/structured-chat-agent")
    if(preamble and prompt.messages and isinstance(prompt.messages[0],SystemMessagePromptTemplate)):
      prompt.messages[0].prompt.template= replace_until_separator(prompt.messages[0].prompt.template,
                                                                  "You have access to the following tools:",preamble)
    return prompt
    

def get_json_agent_prompt(preamble):
    prompt = hub.pull("hwchase17/react-multi-input-json")
    if(preamble and prompt.messages and isinstance(prompt.messages[0],SystemMessagePromptTemplate)):
      prompt.messages[0].prompt.template= replace_until_separator(prompt.messages[0].prompt.template,
                                                                  "You have access to the following tools:",preamble)
    return prompt
    
def get_react_agent_prompt(preamble):
   prompt = hub.pull("hwchase17/react-chat")
   if(preamble and prompt.template):
      prompt.template= replace_until_separator(prompt.template,"Assistant has access to the following tools:",preamble)
   return prompt

def get_vector_search_prompt():
   prompt_template = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}""")
   return prompt_template

def replace_until_separator(original_string, separator, replacement):
    parts = original_string.split(separator, 1)
    if len(parts) > 1:
        return replacement + separator + parts[1]
    else:
        return original_string