import streamlit as st
import google.generativeai as genai
import os
import json
from streamlit_lottie import st_lottie

os.environ["GOOGLE_API_KEY"] = "AIzaSyAM_VBEDuud6PEmN5kB-KhUAry5L7UYifc"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

container = st.container()
try:
    with container:
        @st.cache_data(ttl=60 * 60)
        def load_lottie_file(filepath : str):
            with open(filepath, "r") as f:
                gif = json.load(f)
            st_lottie(gif, speed=1, width=650, height=450)
                
        load_lottie_file("robot.json")
except:
    print("Don't raise exception")

st.title("Gemini AI chatbot using API key")

with st.chat_message("assistant",avatar="🤖"): # windows + . to get the emojies
    st.write("Hey there how can I help you today👋😊")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar="👨🏻‍💻"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar="🤖"):
            st.markdown(message["content"])

prompt = st.chat_input(key='my_text')

if prompt:
    with st.chat_message("user",avatar="👨🏻‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    model = genai.GenerativeModel("gemini-pro")  # Load a pre-trained Generative
    try:
        response = model.generate_content(prompt).text
    except:
        print("Not found")

    with st.chat_message("assistant",avatar="🤖"):
        st.markdown(response)
    st.session_state.messages.append({"role":"assistant","content":response})

