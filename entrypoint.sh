#!/bin/bash
# entrypoint.sh
while true; do
  echo "Starting Telegram bot..."
  python chatbot.py
  
  EXIT_CODE=$?
  echo "Bot exited with code $EXIT_CODE"
  
  if [ $EXIT_CODE -eq 0 ]; then
    echo "Clean shutdown requested"
    break
  fi
  
  echo "Restarting in 5 seconds..."
  sleep 5
done