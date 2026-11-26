import streamlit as st
from groq import Groq
st.set_page_config(page_title='AI Interview Assistant', page_icon='🎯', layout='centered')
st.title('🎯 AI Interview Assistant')
st.caption('Practice interviews with AI-generated question and constructive feedback.')
st.caption('Developed by : ASHRAF ALI 😉')
try:
  client = Groq(api_key=st.secrets['GROQ_API_KEY'])
  st.write("API connection is successful")
except (KeyError, FileNotFoundError):
  st.error('GROQ_API_KEY is missing , add it to streamlit cloud -> app settings secrets')
  st.stop()
