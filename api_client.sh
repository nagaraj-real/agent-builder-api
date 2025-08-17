#!/bin/bash

# A script to interact with the agent builder API.

# Function to display usage
usage() {
  echo "Usage: $0 [--agents|--steps|--tools|--prompts|--history]"
  echo "Options:"
  echo "  --agents:  Fetch all agents."
  echo "  --steps:   Fetch all agent steps."
  echo "  --tools:   Fetch all tools."
  echo "  --prompts: Fetch all prompts."
  echo "  --history: Fetch all chat history."
  exit 1
}

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
  usage
fi

BASE_URL="http://host.docker.internal:8080/api"

# Parse command-line options
case $1 in
  --agents)
    curl -s "$BASE_URL/agents" | jq .
    ;;
  --steps)
    curl -s "$BASE_URL/steps" | jq .
    ;;
  --tools)
    curl -s "$BASE_URL/tools" | jq .
    ;;
  --prompts)
    curl -s "$BASE_URL/prompts" | jq .
    ;;
  --history)
    curl -s "$BASE_URL/chatHistory" | jq .
    ;;
  *)
    echo "Invalid option: $1" >&2
    usage
    ;;
esac
