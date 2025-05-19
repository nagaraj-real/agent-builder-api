#!/bin/bash

#export EXTRA_DEPS="vectordb mongodb openai cohere gemini anthropic langgraph guardrails ui mcp"
export EXTRA_DEPS="openai langgraph mcp ui"

poetry install --extras "${EXTRA_DEPS}"

poetry run start-server

poetry run start-ui