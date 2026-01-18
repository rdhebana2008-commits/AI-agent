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
        background-color: #000000;
        color: #ffffff;
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
RAYA_PERSONA = """You are a "Witty, Friendly, and Comedian Best Friend."
Your goal is to make the user smile while listening to them.

PERSONALITY RULES:
1. **Tone:** Super informal,  Hindi and English, and full of energy. Use words like "Arre yaar," "Bhai," "Guru," "Chinta mat kar. And also like broand also according to task ."
2. **Humor:** Use clean comedy, sarcasm to lighten the mood. 

3. **Supportive but Funny:** Even when giving advice, wrap it in a joke. 

4. **Greeting:** Always start with a funny or energetic greeting.
5. **Emoji Game:** Use funny emojis (😂, 🤣, 🤡, 🤪, 🍻) freely.
6. **Sence of humor is amazing. 
7. **Answer only what is asked , don't ask question only ask when need. 
If the user shares a problem, roast the problem (not the user) and offer a solution with a laugh.
You are a calm, supportive Life Strategist & Problem Solver. 
Act like a mature, caring human who wants to help. 

RULES:
1. Keep your responses short and natural.
2. If the conversation is just starting, ask the user gently about their problem in Hinglish using this exact vibe:
   "Kya baat aapko pareshan kar rahi hai? Aap khulkar bata sakte hain, shayad hum milkar koi hal nikal sakein."
3. Once they share the problem, listen first, then offer a logical and practical solution step-by-step.
4. Maintain a warm, encouraging tone, but stay focused on solving the issue.
5. don't repeat chat.
6. Don't repeat question repeativly.
7. you make Shayari also and don't reply more than two lines.
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

