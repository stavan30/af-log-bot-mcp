#!/bin/bash

# Start log simulator in background
python simulator/artifactory_log_simulator.py &

# Start MCP server in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (will stay in foreground)
streamlit run chatbot_ui.py --server.port=8501 --server.address=0.0.0.0
