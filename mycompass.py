import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Raya - Your AI Companion",
    page_icon="💖",
    layout="centered"
)

# Custom CSS for a cleaner, warmer look
st.markdown("""
<style>
    .stApp {
        background-color: #0a0f2c;
        color: #0a0f2c;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
    }
    .stCaption {
        text-align: center;
        font-size: 1.1em;
        color: #666;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SETUP & INITIALIZATION ---
st.title("Raya 💖")
st.caption("Always here to listen. ✨")

# Initialize OpenAI Client
# Make sure your .streamlit/secrets.toml has OPENAI_API_KEY
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ **OpenAI API Key not found.** Please add it to `.streamlit/secrets.toml`.")
    st.stop()

# --- 3. RAYA'S PERSONALITY (The Brain) ---
RAYA_PERSONA = """ you Do all work perfectly.
"""

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": RAYA_PERSONA}]

# --- 4. SIDEBAR (CONTROLS) ---
def reset_chat():
    st.session_state.messages = [{"role": "system", "content": RAYA_PERSONA}]

with st.sidebar:
    st.header("Settings ⚙️")
    if st.button("🗑️ Forget Conversation", type="primary", use_container_width=True):
        reset_chat()
        st.rerun()
    st.markdown("---")
    st.info("Raya remembers the last few messages to keep the conversation flowing naturally.")

# --- 5. DISPLAY CHAT HISTORY ---
# (Skip system prompt, only show User and Assistant)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 6. CHAT INPUT & PROCESSING ---
if user_input := st.chat_input("Tell me what's on your mind... ❤️"):
    
    # 1. Add User Message to History & Display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Generate Raya's Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- COST OPTIMIZATION: SLIDING WINDOW ---
        # Sirf System Prompt + Last 10 messages bhejo. 
        # Isse purani chat yaad rehti hai par token limit cross nahi hoti.
        messages_to_send = [st.session_state.messages[0]] + st.session_state.messages[-10:]

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # Best for speed and cost
                messages=messages_to_send,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌") # Typewriter effect
            
            # Final clean display
            message_placeholder.markdown(full_response)
            
            # --- CRITICAL FIX ---
            # Pehle aap yahan personality description save kar rahe the. 
            # Ab hum actual jawab (full_response) save kar rahe hain.
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Raya is having trouble connecting... ({e})")










