import streamlit as st
import requests
# Function to call the Wolfram LLM API (from main.py)
def call_wolfram_llm_api(query, appid, maxchars=6800):
    with st.spinner('Fetching data from Wolfram LLM...'):
        base_url = 'https://www.wolframalpha.com/api/v1/llm-api'
        params = {
            'input': query,
            'appid': 'TQP77L-39TXXX3KAY',
            'maxchars': maxchars
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return f'Error: Status Code {response.status_code}\n{response.text}'