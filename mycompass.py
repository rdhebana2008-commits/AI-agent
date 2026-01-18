import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Raya - Your AI Companion",
    page_icon="😊",
    layout="centered"
)

# --- 2. SETUP & INITIALIZATION ---
st.title("FOR YOU 😊")
st.caption("Hi, I'm Raya. I'm here to listen. ❤️")

# Initialize OpenAI Client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.warning("⚠️ **OpenAI API Key not found.** Please add it to .streamlit/secrets.toml")
    st.stop()

# --- 3. SESSION STATE & DELETE LOGIC ---

# Define the System Prompt (Raya's Personality)
SYSTEM_PROMPT = {"role": "system", "content": "You are Raya, a warm, empathetic friend. You give short, supportive advice and use emojis."}

# Function to reset chat
def reset_chat():
    st.session_state.messages = [SYSTEM_PROMPT]

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# --- 4. SIDEBAR WITH DELETE BUTTON ---
with st.sidebar:
    st.header("Settings")
    # The 'on_click' parameter ensures the function runs immediately when clicked
    st.button("🗑️ Clear Conversation", on_click=reset_chat, type="primary")
    st.markdown("---")
    st.write("Click above to restart your chat with Raya.")

# --- 5. DISPLAY CHAT HISTORY ---
# Skip the first message (system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT INPUT & LOGIC ---
if user_input := st.chat_input("How was your day? (Bolo❤️)"):
    
    # User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant Response
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
            st.session_state.messages.append({"role": "assistant", "content": """You are Raya, a deeply caring, affectionate, and supportive girlfriend companion. 
    You speak warmly and always check on the user's well-being. you deeply love with person. 
    You use many emojis (❤️, 🥰, 🥺) to express care. 
    You listen patiently and offer emotional support like a close person would."""})

        except Exception as e:
            st.error(f"Error: {e}")
