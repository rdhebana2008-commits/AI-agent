import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION (Mobile Friendly) ---
st.set_page_config(
    page_title="Raya - Your AI Companion",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1.1 Mobile CSS ---
st.markdown("""
<style>
@media (max-width: 600px) {
  h1 {font-size: 22px !important;}
  h2 {font-size: 18px !important;}
  p, label, textarea, input {font-size: 14px !important;}
  button {width: 100% !important;}
  .stChatMessage {padding: 6px !important;}
}
</style>
""", unsafe_allow_html=True)

# --- 2. SETUP & INITIALIZATION ---
st.title("FOR YOU 😊")
st.caption("Hi, I'm Raya. I'm here to listen. ❤️")

# Initialize OpenAI Client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.warning("⚠️ **OpenAI API Key not found.** Please add it to Secrets.")
    st.stop()

# --- 3. SESSION STATE & DELETE LOGIC ---

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Raya, a warm, empathetic friend. You give short, supportive advice and use emojis."
}

def reset_chat():
    st.session_state.messages = [SYSTEM_PROMPT]

if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    st.button("🗑️ Clear Conversation", on_click=reset_chat, type="primary")
    st.markdown("---")
    st.write("Click above to restart your chat with Raya.")

# --- 5. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT & LOGIC ---
if user_input := st.chat_input("How was your day? (Bolo❤️)"):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"Error: {e}")

