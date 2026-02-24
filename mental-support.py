import streamlit as st
import ollama

import base64

st.set_page_config(page_title="SolaceAI 🌿") 

st.session_state.setdefault('conversation_history',[]) 
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role":"user", "content":user_input})
    response = ollama.chat(model="llama3.1:8b", messages=st.session_state['conversation_history'])

    ai_response = response['message']['content']
    st.session_state['conversation_history'].append({"role":"assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    prompt="Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    response = ollama.chat(model = "llama3.1:8b",messages=[{"role":"user","content":prompt}])
    return response['message']['content']

def generate_meditation_guide():
    prompt="Provide a 5-minute guided meditation script to help someone relax and reduce stress"
    response = ollama.chat(model = "llama3.1:8b",messages=[{"role":"user","content":prompt}])
    return response['message']['content']

def get_base64(background):
    with open(background,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode() 
bin_str = get_base64("background.png")

st.markdown(f"""
            <style>
                .stApp{{
                     background-image:url("data:image/png; base64, {bin_str}");
                     background-size: cover;
                     background-position: center;
                     background-repeat: no-repeat;
                }}
            </style>
            """, unsafe_allow_html=True)
              

st.title("SolaceAI🌿")
st.subheader("A safe space to share, reflect, and heal ❤️")

for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

user_message = st.text_input("How are you feeling today?")

if user_message:
    with st.spinner("Processing your feelings…"):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")


row1=st.container()

with row1:
    if st.button("Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

row2 = st.container()

with row2:
    if st.button("Give me a guided meditation"):
        meditation= generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation}")
