import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from utils import call_wolfram_llm_api


# Custom CSS for styling (from main.py)
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Streamlit Chat Interface
st.title("Helpfull Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Replacing response logic with Wolfram LLM API call
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        appid = st.secrets["Wolfram-App-ID"]
        result = call_wolfram_llm_api(prompt, appid)

        if result.startswith('Error:'):
            st.error(result)
        else:
            lines = result.split('\n')
            for line in lines:
                if line.startswith('image:'):
                    image_url = line.split('image:')[1].strip()
                    image_response = requests.get(image_url)
                    img = Image.open(BytesIO(image_response.content))
                    st.image(img, use_column_width=True)
                else:
                    st.markdown(f'<p class="big-font">{line}</p>', unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": result})
