import streamlit as st
import requests

# Sidebar
st.sidebar.title("SchemaSense Settings")
st.sidebar.markdown("Configure your chatbot here:")
backend_url = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000/query/")
st.sidebar.markdown("---")
st.sidebar.write("Chat History")
if "history" not in st.session_state:
    st.session_state.history = []

# Main UI
st.title("💬 SchemaSense Chatbot")

# Chat input
user_input = st.chat_input("Type your query...")

if user_input:
    # Call FastAPI backend
    try:
        response = requests.post(backend_url, json={"query": user_input})
        data = response.json()
        answer = data.get("answer", "No answer returned")

        # Save to history
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

# Display chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
