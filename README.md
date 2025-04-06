# Agent Builder API

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nagaraj-real/agent-builder-api?devcontainer_path=.devcontainer%2Fcodespaces%2Fdevcontainer.json)

## 🚀 Quick Start

You can start the API server using docker containers or manually cloning and building this repository.

[Manual setup](#manual-setup): Clone this repository in your local machine and start the python FAST API server. Optionally, install and set up Mongo DB.

[Dev Container Setup](#dev-containers-setup): Dev Containers allow you to automate the environment setup.
Use this setup to install and run container services in an isolated environment with extensions preinstalled.
You can also open GitHub Codespaces in a remote environment/browser using secrets to pass Model API keys.

### Manual Setup

1. Set up a Python virtualenv and install dependencies

   ```sh
   python -m venv --prompt agent-builder-api venv
   source venv/bin/activate
   # venv/Scripts/activate (Windows PS)
   pip install -r requirements.txt
   ```

2. Set the model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

3. Start the server in the new terminal

   ```sh
   python -m agentbuilder.main
   ```

#### [Optional] Start using Poetry

For fine-grained dependency management, use [Poetry](https://python-poetry.org/) to pick and choose dependency packs based on your LLM model provider and tool features.

1. Follow the [Offical Instruction Guide](https://python-poetry.org/docs/#installation) to install Poetry.

2. Pick and choose dependency packs to install.

   ```sh
   poetry install --extras "openai gemini cohere anthropic mongodb vectordb langgraph guardrails ui"
   ```

3. Set the model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

4. Start the server in the new terminal

   ```sh
   poetry run start-server
   ```

> [!NOTE]
> Poetry will create a virtual environment for us.

#### [Optional] Enable MongoDB

By default, data is stored as JSON files. Enable storage in Mongo DB by setting url using the environment variable.

```env
MONGODB_URL="mongodb://localhost:27017/llmdb"
```

### Dev Containers Setup

1. Enable Dev Containers in vscode by following the steps in [official documentation](https://code.visualstudio.com/docs/devcontainers/containers#_installation).

2. Click on the badge below to run the services in an isolated container environment in a local machine.

   This will clone the repo and start the API and Mongo DB container services.

   [![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nagaraj-real/agent-builder-api)

> [!TIP]
> Use URL _mongodb://mongodb:27017/llmdb_ in Mongo DB vscode extension to view storage data.

4. Execute **F1 > Dev Containers: Attach to Running Container..** and select _agent-builder-container_.
5. Set the model name and API key in **.env** file

   ```env
   OPENAI_API_KEY="sk----"
   MODEL_NAME="openai"
   ```

## Customization

### Dependency packs and environment configuration

Dependency packs allow fine-grained package installations based on your requirements.
Use the environment variable EXTRA_DEPS in the docker-compose file to update.

_install-extra-deps.sh_ script can be used in dev container mode if docker-compose is not available.

For example, the below environment configuration will install dependencies for the Gemini model,
Mongo DB, Langchain Graph, and VectorDB

```env
EXTRA_DEPS: "gemini,mongodb,langgraph,vectordb"
```

> [!TIP]
> Start with a basic dependency pack to support your model and add other features incrementally

The following models are supported by its dependency pack

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
Add your agents using the Agent Factory Module (_agentbuilder/factory/agent_factory_).

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

Customize your Agent Workflow using custom prompts and graphs.
Filter the agent using the agent name to apply customizations.

For example, the following code applies graph builder workflow for the Agent named "graph_agent"

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
> Dependency pack "langgraph" needs to be installed for BaseGraphAgentBuilder.

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

  > [!TIP]
  > Use JSON chat agent type for better compatibility with local models.

  Install [Ollama](https://ollama.com/) and pull the model.

  ```sh
  ollama pull mistral:v0.3
  ```

  Set environment variable.

  ```env
  MODEL_NAME="ollama/mistral:v0.3"
  ```
