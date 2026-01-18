import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="FOR YOU", page_icon="😊")

st.title("FOR YOU 😊")
st.write("Hii I'm Raya.")

# 1. TRY TO GET KEY FROM STREAMLIT SECRETS
# This looks into the .streamlit/secrets.toml file we just created.
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except FileNotFoundError:
    st.error("⚠️ The .streamlit/secrets.toml file was not found.")
    st.stop()
except KeyError:
    st.error("⚠️ The OPENAI_API_KEY is missing inside secrets.toml.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2. THE FORM
with st.form("mood_form"):
    user_input = st.text_input("How was your day?")
    submitted = st.form_submit_button("Bolo❤️")

if submitted and user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "      "},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            st.success("Compass:")
            st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")