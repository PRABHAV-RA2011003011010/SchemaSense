import streamlit as st
import requests
import uuid
import json
import os

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="SchemaSense",
    page_icon="💬",
    layout="wide"
)

CHAT_FILE = "chat_history.json"

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
}

.stChatMessage {
    border-radius: 10px;
}

.chat-title {
    font-size: 20px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD / SAVE CHATS
# =========================

def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chats():
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chats, f, indent=2)

# =========================
# SESSION INIT
# =========================

if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat" not in st.session_state:

    if st.session_state.chats:
        st.session_state.current_chat = list(
            st.session_state.chats.keys()
        )[0]
    else:
        chat_id = str(uuid.uuid4())

        st.session_state.chats[chat_id] = {
            "title": "New Chat",
            "messages": []
        }

        st.session_state.current_chat = chat_id

# =========================
# SIDEBAR
# =========================

st.sidebar.title("💬 SchemaSense")

backend_url = st.sidebar.text_input(
    "Backend URL",
    "http://127.0.0.1:8000/query/"
)

st.sidebar.divider()

if st.sidebar.button("➕ New Chat", use_container_width=True):

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = chat_id
    save_chats()
    st.rerun()

st.sidebar.subheader("Chats")

for chat_id, chat in list(st.session_state.chats.items()):

    col1, col2 = st.sidebar.columns([4, 1])

    with col1:
        if st.button(
            chat["title"],
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            st.session_state.current_chat = chat_id
            st.rerun()

    with col2:
        if st.button(
            "🗑️",
            key=f"delete_{chat_id}"
        ):
            del st.session_state.chats[chat_id]

            if not st.session_state.chats:
                new_id = str(uuid.uuid4())

                st.session_state.chats[new_id] = {
                    "title": "New Chat",
                    "messages": []
                }

                st.session_state.current_chat = new_id
            else:
                st.session_state.current_chat = list(
                    st.session_state.chats.keys()
                )[0]

            save_chats()
            st.rerun()

# =========================
# CURRENT CHAT
# =========================

current_chat = st.session_state.chats[
    st.session_state.current_chat
]

st.title("💬 SchemaSense Chatbot")

# =========================
# DISPLAY HISTORY
# =========================

for msg in current_chat["messages"]:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================

user_input = st.chat_input(
    "Ask something..."
)

if user_input:

    current_chat["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:

            with st.spinner("Thinking..."):

                response = requests.post(
                    backend_url,
                    json={
                        "query": user_input,
                        "chat_id": st.session_state.current_chat
                    },
                    timeout=300
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No response received."
                )

                placeholder.markdown(answer)

        except Exception as e:

            answer = f"❌ Backend Error:\n\n{str(e)}"

            placeholder.markdown(answer)

    current_chat["messages"].append({
        "role": "assistant",
        "content": answer
    })

    # Auto-title first message
    if current_chat["title"] == "New Chat":
        current_chat["title"] = user_input[:40]

    save_chats()

# =========================
# EXPORT CHAT
# =========================

st.sidebar.divider()

chat_export = json.dumps(
    current_chat,
    indent=2
)

st.sidebar.download_button(
    label="⬇ Export Current Chat",
    data=chat_export,
    file_name="chat.json",
    mime="application/json",
    use_container_width=True
)