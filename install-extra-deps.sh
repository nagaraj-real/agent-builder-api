#!/bin/sh

# Add extra dependencies to install based on your LLM provider and tools usage

# EXTRA_DEPS="openai,cohere,gemini,anthropic,nvidia,vectordb,mongodb,langgraph,guardrails,ui"

if [ -n "$EXTRA_DEPS" ]; then
  echo "installing extra dependencies" "$EXTRA_DEPS"
  pip install -e .[${EXTRA_DEPS}]
fi