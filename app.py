
import streamlit as st
from groq import Groq

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# 2. CUSTOM STYLING
# --------------------------------

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stButton > button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #D93636;
    color: white;
}

h1 {
    color: #FF4B4B;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# 3. HEADER
# --------------------------------

st.title("🎯 AI Interview Assistant")

st.caption(
    "Practice interviews with AI-generated questions "
    "and constructive feedback."
)

st.caption("Developed by: ASHRAF ALI 😉")

st.divider()

# --------------------------------
# 4. GROQ API CONNECTION
# --------------------------------

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

except (KeyError, FileNotFoundError):
    st.error(
        "GROQ_API_KEY is missing. "
        "Add it to Streamlit Cloud → App Settings → Secrets."
    )
    st.stop()

# --------------------------------
# 5. SIDEBAR SETTINGS
# --------------------------------

st.sidebar.title("⚙️ Interview Settings")

role = st.sidebar.selectbox(
    "Select Job Role",
    [
        "Python Developer",
        "Java Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Software Engineer",
        "HR Executive",
        "AI Engineer",
        "Data Scientist"
    ]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty Level",
    [
        "Beginner 😊",
        "Intermediate 😎",
        "Advanced 😤"
    ]
)

experience = st.sidebar.selectbox(
    "Select Experience Level",
    [
        "Fresher",
        "0-1 Years",
        "1-3 Years",
        "3-5 Years",
        "5+ Years"
    ]
)

question_count = st.sidebar.slider(
    "Number of Questions",
    min_value=5,
    max_value=20,
    value=5,
    step=5
)

topics = st.sidebar.multiselect(
    "Select Technical Topics",
    [
        "Python",
        "OOP",
        "Data Structures",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "Problem Solving"
    ],
    default=["Python", "OOP"]
)

include_answers = st.sidebar.checkbox(
    "Include Expected Answers",
    value=True
)

# --------------------------------
# 6. MAIN INTERFACE
# --------------------------------

st.subheader("🚀 Generate Your Interview")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Selected Role:** {role}")

with col2:
    st.info(f"**Difficulty:** {difficulty}")

st.write(
    "Customize your interview settings from the sidebar "
    "and generate questions using AI."
)

# --------------------------------
# 7. SESSION STATE
# --------------------------------

if "interview_result" not in st.session_state:
    st.session_state.interview_result = None

# --------------------------------
# 8. GENERATE INTERVIEW QUESTIONS
# --------------------------------

if st.button("🚀 Generate Interview Questions"):

    if not topics:
        st.warning("Please select at least one technical topic.")

    else:

        prompt = f"""
        You are a professional technical interviewer.

        Generate {question_count} interview questions.

        Job Role: {role}
        Difficulty Level: {difficulty}
        Candidate Experience: {experience}
        Technical Topics: {", ".join(topics)}

        Instructions:

        1. Generate relevant interview questions.
        2. Arrange questions from easy to difficult.
        3. Include practical and real-world scenarios.
        4. Avoid repeating questions.

        {"5. Provide a clear expected answer after every question." if include_answers else "5. Generate questions only without answers."}

        Format the response professionally using:

        Question 1:
        Question:

        Expected Answer:
        (If requested)

        Keep answers simple, accurate and understandable.
        """

        try:

            with st.spinner(
                "🤖 AI is preparing your interview questions..."
            ):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an experienced technical "
                                "interviewer and career mentor."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_completion_tokens=5000
                )

                output = response.choices[0].message.content

                st.session_state.interview_result = output

        except Exception as e:

            st.error(f"Something went wrong: {e}")

# --------------------------------
# 9. DISPLAY RESULTS
# --------------------------------

if st.session_state.interview_result:

    st.divider()

    st.subheader("📋 Your Generated Interview Questions")

    st.markdown(st.session_state.interview_result)

    # Download questions

    st.download_button(
        label="⬇️ Download Interview Questions",
        data=st.session_state.interview_result,
        file_name="AI_Interview_Questions.txt",
        mime="text/plain"
    )

    if st.button("🔄 Generate New Interview"):
        st.session_state.interview_result = None
        st.rerun()

# --------------------------------
# 10. FOOTER
# --------------------------------

st.divider()

st.caption(
    "© 2026 AI Interview Assistant | Built with Python, "
    "Streamlit and Groq API | Ashraf Ali"
)
