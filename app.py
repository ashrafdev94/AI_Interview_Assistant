import streamlit as st
from groq import Groq
st.set_page_config(page_title = 'AI Interview Assistant', page_icon='🎯', layout='centered')
st.title('🎯AI Interview Assistant')
st.caption('practice interviews with Ai-generated questions and constructive feedback.')
st.caption('Developed by : ASHRAF ALI 😉')
try: 
    client = Groq(api_key=st.secrets['GROQ_API_KEY'])
    st.write("API Connection successful")
except (keyError, FileNotFoundError):
    st.error('GROQ_API_KEY is missing.Add it to streamlit Clode->App setting secrets')
    st.stop()
role = st.selectbox("select Job Role",[
    "pyhton Developer",
    "Java Developer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Software Engineer",
    "HR Executive"
]) 
role2 = st.selectbox("select Difficulty level",[
    "Beginner",
    "Intermediate",
    "Difficulty",
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
    st.write(output)
