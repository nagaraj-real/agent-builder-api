#!/bin/bash

#export EXTRA_DEPS="vectordb mongodb openai cohere gemini anthropic langgraph guardrails ui"
export EXTRA_DEPS="openai"

poetry install --extras "${EXTRA_DEPS}"

poetry run start-server

poetry run start-ui