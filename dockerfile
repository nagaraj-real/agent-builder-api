FROM python:3.12-slim

RUN apt update && apt install git -y

WORKDIR /app

COPY pyproject.toml .

COPY ./agentbuilder ./agentbuilder

RUN pip install .

COPY ./.vscode ./.vscode

COPY ./install-extra-deps.sh ./start-server.sh ./log_config.yml .env .

ENV EXTRA_DEPS="openai mongodb"

CMD ["sh", "-c", "/app/install-extra-deps.sh && /app/start-server.sh"]
