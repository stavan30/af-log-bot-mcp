Artifactory Logs query Slack-bot. A test project. With MCP Server.

# Artifactory Log Query Bot

This project simulates real-time Artifactory logs and allows querying them through a FastAPI-based MCP backend. It includes manual and natural language query support via CLI and Streamlit interfaces.

## How to Run

1. Install dependencies  
   `pip install -r requirements.txt`

2. Start the log simulator  
   `python simulator/artifactory_log_simulator.py`

3. Start the MCP server  
   `uvicorn app.main:app --reload`

4. Start the Streamlit chatbot interface  
   `streamlit run chatbot_ui.py`

## Using Docker

To build and run the project using Docker:

1. Build the Docker image

   docker build -t artifactory-log-bot .

2. Run the container

   docker run -p 8000:8000 -p 8501:8501 artifactory-log-bot

The MCP API will be available at http://localhost:8000  
The Streamlit UI will be available at http://localhost:8501


## STEP1: MCP Server Setup

Created a FastAPI server with a /query endpoint.  
It reads logs from a CSV file and filters them by:  
- username  
- response code  
- keyword  
- time window  

## STEP2: CLI Bot Integration

Created a CLI-based bot to interact with the MCP server.  
Users enter filters manually, and the bot prints matching logs in the terminal.

## STEP3: NLP-Based Query Parsing

Built an NLP parser to extract filters from natural language.  
Integrated into the CLI bot so users can ask questions like:  
"Show me 404 errors by john.wick in the last 10 minutes"

## STEP4: Streamlit Chatbot Interface

Created a web interface using Streamlit.  
Supports both manual filters and natural language queries.  
Connects to the MCP server and displays logs in a chat-like view.
