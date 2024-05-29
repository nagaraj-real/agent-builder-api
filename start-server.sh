#!/bin/sh

DEFAULT_UVICORN_OPTIONS="--host 0.0.0.0 --port 8080 --reload --log-level info --workers 1 --log-config log_config.yml"

echo "starting server using options" "${UVICORN_OPTIONS:-$DEFAULT_UVICORN_OPTIONS}"
uvicorn agentbuilder.main:app ${UVICORN_OPTIONS:-$DEFAULT_UVICORN_OPTIONS}
