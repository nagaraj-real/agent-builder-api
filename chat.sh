#!/bin/bash

# Default values
QUERY=""
AGENT_NAME="default"
CHAT_ID=""
IMAGE_DATA=""
PROJECT_PATH=""
# File to store the session chat ID. This makes conversations persistent.
CHAT_ID_FILE="./.chat_session"

# Function to display usage
usage() {
  echo "Usage: $0 [-q <query>] [-a <agent_name>] [-c <chat_id>] [-i <image_data>] [-I <project_path>] [-h]"
  echo "Options:"
  echo "  -q: The query to send to the chat agent."
  echo "  -a: The name of the agent to use (default: default)."
  echo "  -c: The chat ID for conversation history. Overrides the session file."
  echo "  -i: Image data to send with the query."
  echo "  -I: Initialize the environment. Provide the project path."
  echo "  -h: Display this help message."
  exit 1
}

# Parse command-line options
while getopts "q:a:c:i:I:h" opt; do
  case $opt in
    q) QUERY="$OPTARG" ;;
    a) AGENT_NAME="$OPTARG" ;;
    c) CHAT_ID="$OPTARG" ;;
    i) IMAGE_DATA="$OPTARG" ;;
    I) PROJECT_PATH="$OPTARG" ;;
    h) usage ;;
    ?) echo "Invalid option: -$OPTARG" >&2; usage ;;
  esac
done

# If CHAT_ID was not provided via -c, try to load it from the session file.
if [ -z "$CHAT_ID" ]; then
  if [ -f "$CHAT_ID_FILE" ]; then
    CHAT_ID=$(cat "$CHAT_ID_FILE")
  fi
fi

# Handle init option
if [ -n "$PROJECT_PATH" ]; then
  echo "Initializing environment..."
  # Stop and remove existing container
  docker stop alpine_runner >/dev/null 2>&1 && docker rm alpine_runner >/dev/null 2>&1
  
  # Start new container
  docker run -d \
  --name alpine_runner \
  --user root \
  -w /root/projects/app \
  -v "$PROJECT_PATH":/root/projects/app \
  -v "$PROJECT_PATH/logs":/var/log \
  alpine:latest \
  sh -c "mkdir -p /var/log && : > /var/log/vibe.log && tail -f /var/log/vibe.log"
  
  echo "Environment initialized."
  exit 0
fi

# Check if query is provided for chat
if [ -z "$QUERY" ]; then
  usage
fi

# Construct JSON payload using jq
JSON_PAYLOAD=$(jq -n \
  --arg query "$QUERY" \
  --arg agentName "$AGENT_NAME" \
  --arg chatId "$CHAT_ID" \
  --arg imageData "$IMAGE_DATA" \
  '{"query": $query, "agentName": $agentName, "chatId": $chatId} + if $imageData != "" then {"imageData": $imageData} else {} end')

# Make the curl request and store the response
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$JSON_PAYLOAD" http://host.docker.internal:8080/api/chat)

# Extract chatId from the response and save it to the session file for subsequent requests.
# This allows for maintaining a continuous conversation without manually passing the chat ID.
CHAT_ID_FROM_RESPONSE=$(echo "$RESPONSE" | jq -r '.chatId')
if [ -n "$CHAT_ID_FROM_RESPONSE" ] && [ "$CHAT_ID_FROM_RESPONSE" != "null" ]; then
  echo "$CHAT_ID_FROM_RESPONSE" > "$CHAT_ID_FILE"
fi

# Print only the chatResponse to stdout, keeping the script's output clean.
echo "$RESPONSE" | jq -r '.chatResponse'
