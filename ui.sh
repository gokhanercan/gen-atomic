#!/bin/bash

# Run Streamlit and keep terminal open if it fails
streamlit run --server.runOnSave true src/APIExplorerUI.py

# Capture exit code
exit_code=$?

# If there was an error, print it and wait for user input
if [ $exit_code -ne 0 ]; then
  echo "Streamlit exited with error code $exit_code"
  read -p "Press Enter to exit..."
fi
