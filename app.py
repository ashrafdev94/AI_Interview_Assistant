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

role = st.selectbox("Select Job Role",[
    "Python developer",
    "Java developer",
    "Data Analyst",
    "Machine Learning Engineering",
    "Software Engineer",
    "HR Executive"
])

if st.button("Generate Interview Questions"):

    prompt = "Generate 5 interview questions for the role of " + role

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are an expert technical Interviewer"},
            {"role": "user", "content": prompt}
        ]
    )
output = response.choices[0].message.content
st.write(output
