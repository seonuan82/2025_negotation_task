import streamlit as st
from utils.llm import get_llm_response

st.title("Negotiation Agent")

user_input = st.text_input("Your question to the agent:")
if user_input:
    response = get_llm_response(user_input)
    st.write("Agent:", response)