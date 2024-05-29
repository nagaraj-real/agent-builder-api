# Agent Builder API 

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nagaraj-real/agent-llm-api?devcontainer_path=.devcontainer%2Fcodespaces%2Fdevcontainer.json) 

## 🚀 Quick Start

You can start the API server using docker containers or manually cloning and building this repository.
Refer this [section](#dependency-packs-and-environment-configuration) on how to use environment variables to configure dependencies and LLM model specifications (model name, API keys).

### Dev Containers Setup

1. Enable Dev Containers in vscode by following the steps in [official documentation](https://code.visualstudio.com/docs/devcontainers/containers#_installation).

2. Click on the badge below to run the API in an isolated container environment.

   [![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nagaraj-real/agent-llm-api)

   This will clone the repo and start API and Mongo DB container services.

3. Set model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

4. Execute **F1 > Dev Containers: Rebuild Container** to restart the container with updated environment configuration.

5. Open AgentBuilder Dev Container to make file updates with live reload.

   ![agentbuilder-reload](https://github.com/nagaraj-real/agent-llm-api/assets/17967313/7f98c42f-16e2-4943-9bde-1a4c2cdc2b8f)

6. [Optional] Monitor container logs

   ![container-log](https://github.com/nagaraj-real/agent-llm-api/assets/17967313/8ef8ea30-e35c-48fe-8d67-9a57de5475d2)



### Manual Setup

1. Set up a Python virtualenv and install dependencies

   ```sh
   python -m venv --prompt agent-llm-api venv
   source venv/bin/activate
   # venv/Scripts/activate (Windows)
   pip install -r requirements.txt
   ```

2. Set model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

3. Start server in new terminal

   ```sh
   python -m agentbuilder.main
   ```

#### [Optional] Start using Poetry

For fine grained dependency management, use [Poetry](https://python-poetry.org/) to pick and choose dependency packs based on your LLM model provider and tool features.

1. Follow the [Offical Instruction Guide](https://python-poetry.org/docs/#installation) to install Poetry.

2. Pick and choose dependency packs to install.

   ```sh
   poetry install --extras "openai gemini cohere anthropic mongodb vectordb langgraph"
   ```

3. Set model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

4. Start server in new terminal

   ```sh
   poetry run start-server
   ```

> [!NOTE]
> Poetry will create virtual environment for us.

#### [Optional] Enable MongoDB

By default, data is stored as Json files. Enable storage in Mongo DB by setting url using envrironment variable.

```env
MONGODB_URL="mongodb://localhost:27017/llmdb"
```

Refer [Configuring Models](#configuring-models) for information on how to configure other providers including Ollama.

## Customization

### Dependency packs and environment configuration

Dependency packs allow fine grained package installations based on your requirement.
Use environment variable EXTRA_DEPS to update these packs.

For example the below environment configuration will install dependencies for Gemini model,
Mongo DB, Langchain Graph and VectorDB

```env
EXTRA_DEPS="gemini,mongodb,langgraph,vectordb"
```

> [!TIP]
> Start with basic depedency pack to support your model and add other features incrementally

Following models are supported with its dependency pack

|   Model   | Dependency pack |   ENV key name    |
| :-------: | :-------------: | :---------------: |
|  OPEN AI  |     openai      |  OPENAI_API_KEY   |
|  GEMINI   |     gemini      |  GOOGLE_API_KEY   |
|  COHERE   |     cohere      |  COHERE_API_KEY   |
| ANTHROPIC |    anthropic    | ANTHROPIC_API_KEY |

Some pre-configured tools require extra dependencies or API keys to get enabled.

|        Tool        | Dependency pack |   ENV key name   |
| :----------------: | :-------------: | :--------------: |
|  internet_search   |        -        |  TAVILY_API_KEY  |
| vectorstore_search |    vectordb     | EMBED_MODEL_NAME |

### Adding Tools

Add custom [Tools](https://python.langchain.com/v0.2/docs/how_to/custom_tools/) or [Toolkits](https://python.langchain.com/v0.2/docs/integrations/toolkits/) using tool factory module (_agentbuilder/factory/tool_factory_).

1. [Create your tool](https://python.langchain.com/v0.2/docs/how_to/custom_tools/)

   _agentbuilder/tools/my_custom_tool.py_

   ```py

   from pathlib import Path
   from langchain_core.tools import tool
   from pydantic import BaseModel, Field

   @tool
   def my_custom_tool(a: int, b: int):
   """Custom Tool Description"""
   return a + b

   my_custom_tool.name="custom_tool_name"
   my_custom_tool.description="Custom Tool Description"

   class field_inputs(BaseModel):
   a: int = Field(description="First input")
   b: int = Field(description="Second input")

   my_custom_tool.args_schema = sum_inputs
   my_custom_tool.metadata= {"file_path": str(Path(__file__).absolute())}
   ```

2. Add your tool in _get_all_tools_ method in tool_factory module.

   _agentbuilder/factory/tool_factory.py_

   ```diff
   def get_all_tools()->Sequence[BaseTool]:

       return get_vectordb_tools()+ get_websearch_tools() + json_tools + [
               directly_answer_tool,
               weather_clothing_tool,
               temperature_tool,
               temperature_sensor_tool,
               sum_tool,greeting_tool,
               git_diff_tool,
               repl_tool,
   +           my_custom_tool
               ]
   ```

### Adding Agents

Agents can be created using Extension UI or declared in code.
Add your agents using Agent Factory Module (_agentbuilder/factory/agent_factory_).

1. Create your agent

   ```python
   def my_agent():
     return AgentParams(
           name="my_agent",
           preamble= "You are a powerful agent that uses tools to answer Human questions",
           tools=  ["my_custom_tool"],
           agent_type= 'tool_calling'
     )
   ```

2. Add your agent in _get_all_agents_ method.

   ```diff
   def get_all_agents():
   return [
           default_agent(),
           weather_agent(),
           python_agent(),
           git_agent(),
   +       my_agent()
   ]
   ```

### Custom Agent Builder and Graphs

Customize your own Agent Workflow using custom prompts and graphs.
Filter the agent using agent name to apply customizations.

For example, the following code applies graph builder worlflow for the Agent named "graph_agent"

```py
def get_agent_builder(params:AgentBuilderParams):
    agent_name= params.name
    match agent_name:
        case "graph_agent":
            from agentbuilder.agents.BaseGraphAgentBuilder import BaseGraphAgentBuilder
            return BaseGraphAgentBuilder(params)
        case _:
            return BaseAgentBuilder(params)
```

> [!IMPORTANT]
> Dependency pack "langgraph" needs to installed for BaseGraphAgentBuilder.

## Configuring models

Update model configuration using environment variables.

Supports _{Provider}/{ModelName}_ format

- Gemini

  Create API keys https://aistudio.google.com/app/apikey

  ```env
   MODEL_NAME="gemini/gemini-pro"
   EMBED_MODEL_NAME="gemini/embedding-001"
   GOOGLE_API_KEY=<GOOGLE_API_KEY>
  ```

- Cohere

  Create API keys https://dashboard.cohere.com/api-keys

  ```env
   MODEL_NAME="cohere/command"
   EMBED_MODEL_NAME="cohere/embed-english-v3.0"
   COHERE_API_KEY=<COHERE_API_KEY>
  ```

- Open AI

  Create API keys https://platform.openai.com/docs/quickstart/account-setup

  ```env
   MODEL_NAME="openai/gpt-4o"
   EMBED_MODEL_NAME="openai/text-embedding-3-large"
   OPENAI_API_KEY=<OPENAI_API_KEY>
  ```

- Anthropic

  Create API keys https://www.anthropic.com/ and https://www.voyageai.com/

  ```env
   MODEL_NAME="anthropic/claude-3-opus-20240229"
   EMBED_MODEL_NAME="voyageai/voyage-2"
   ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
   VOYAGE_API_KEY=<VOYAGE_API_KEY>
  ```

- Ollama

  Use local models for function calls.

  Install [Ollama](https://ollama.com/) and pull model.

  ```sh
  ollama pull mistral:v0.3
  ```

  Set environment variable.

  ```env
  MODEL_NAME="ollama/mistral:v0.3"
  ```

> [!TIP]
> Use JSON chat agent type for better compatibility with local models.