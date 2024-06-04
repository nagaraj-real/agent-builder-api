#!/bin/bash

# export EXTRA_DEPS="openai vectordb langgraph gemini cohere mongodb"
export EXTRA_DEPS="openai"

poetry install --extras "${EXTRA_DEPS}"

poetry run start-server