import streamlit as st
import requests
from bot.nlp_parse import extract_filters_from_query

st.set_page_config(page_title="Artifactory Log Bot", page_icon="📄", layout="wide")
st.title("Artifactory Log Query Bot")
st.subheader("Query real-time logs using filters or natural language")

API_URL = "http://localhost:8000/query"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar to select mode
mode = st.sidebar.radio("Choose Query Mode", ["Manual Filters", "Natural Language"])

def submit_manual_form():
    filters = {
        "username": st.session_state.username or None,
        "resp_code": int(st.session_state.resp_code) if st.session_state.resp_code else None,
        "keyword": st.session_state.keyword or None,
        "last_n_minutes": int(st.session_state.last_n_minutes) if st.session_state.last_n_minutes else 10,
    }

    return filters

def display_results(filters):
    try:
        response = requests.post(API_URL, json=filters)
        if response.status_code == 200:
            logs = response.json().get("results", [])
            if logs:
                message = f"Found {len(logs)} matching log(s):"
                for i, log in enumerate(logs[:5], 1):
                    message += f"\n\n[{i}] {log['timestamp']} | {log['username']} | {log['resp_code']} | {log['artifact']}"
                    message += f"\n     Status: {log['status']} | Action: {log['action']} | Host: {log['host']}"
            else:
                message = "No matching logs found."
        else:
            message = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        message = f"Could not connect to MCP server: {e}"

    st.session_state.chat_history.append(("bot", message))

# --- Manual Mode ---
if mode == "Manual Filters":
    with st.form("manual_query_form"):
        st.text_input("Username", key="username")
        st.text_input("Response Code (e.g. 404)", key="resp_code")
        st.text_input("Keyword", key="keyword")
        st.text_input("Look back (minutes)", value="10", key="last_n_minutes")
        submitted = st.form_submit_button("Send Query")
        if submitted:
            st.session_state.chat_history.append(("user", f"Manual Query: {st.session_state.username}, {st.session_state.resp_code}, {st.session_state.keyword}, {st.session_state.last_n_minutes}"))
            filters = submit_manual_form()
            display_results(filters)

# --- NLP Mode ---
else:
    user_input = st.text_input("Ask your question (natural language):", key="user_input")
    if st.button("Send NLP Query"):
        st.session_state.chat_history.append(("user", user_input))
        filters = extract_filters_from_query(user_input)
        display_results(filters)

# --- Chat History ---
st.markdown("---")
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
    st.markdown("---")
