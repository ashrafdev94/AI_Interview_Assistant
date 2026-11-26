import streamlit as st
from groq import Groq
st.set_page_config(page_title='AI Interview Assistant', page_icon='🎯', layout='centered')
st.title('🎯 AI Interview Assistant')
st.caption('Practice interviews with AI-generated question and constructive feedback.')
st.caption('Developed by : ASHRAF ALI 😉')
try:
  client = Groq(api_key=st.secrets['GROQ_API_KEY'])
  st.write("API connection is successfull')
expect (KeyError, FileNotFoundError):
  st.error('GROQ_API_KEY is missing, Add it to Stramlit Cloud -> App setting secrets')
  st.stop()
