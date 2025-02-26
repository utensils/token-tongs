#!/bin/bash

# Check if API key is provided as an argument
if [ "$1" != "" ]; then
    export OPENROUTER_API_KEY="$1"
    echo "Using provided API key"
# Check if API key is already set in environment
elif [ "$OPENROUTER_API_KEY" != "" ]; then
    echo "Using existing API key from environment"
# Prompt for API key if not provided
else
    echo -n "Enter your OpenRouter API key: "
    read -s API_KEY
    echo ""
    export OPENROUTER_API_KEY="$API_KEY"
    echo "API key set"
fi

# Run the application
./token_tongs.py
