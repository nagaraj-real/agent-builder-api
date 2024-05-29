#!/bin/sh

if [ -n "$EXTRA_DEPS" ]; then
  echo "installing extra dependencies" "$EXTRA_DEPS"
  pip install -e .[${EXTRA_DEPS}]
fi