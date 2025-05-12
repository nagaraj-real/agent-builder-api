FROM python:3.12.10-slim

RUN apt update && apt install git -y

WORKDIR /app

COPY pyproject.toml .

COPY ./agentbuilder ./agentbuilder

RUN pip install .

COPY ./.vscode ./.vscode

COPY ./install-extra-deps.sh ./start-server.sh ./log_config.yml README.md .

COPY ./.env.docker ./.env

ENV EXTRA_DEPS="openai mongodb langgraph mcp"

CMD ["sh", "-c", "/app/install-extra-deps.sh && /app/start-server.sh"]
