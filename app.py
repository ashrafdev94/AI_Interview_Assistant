
import streamlit as st
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: #0b0d12;
}
[data-testid="stSidebar"] {
    background: #12151d;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #ff4b4b;
}
.subtitle {
    color: #aab0bd;
    font-size: 16px;
}
div.stButton > button {
    background: #ff4b4b;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
}
div.stButton > button:hover {
    background: #d93636;
    color: white;
}
.metric-card {
    background: #171b26;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #292f3d;
}
</style>
""", unsafe_allow_html=True)

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "client" not in st.session_state:
    st.session_state.client = None

try:
    st.session_state.client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("GROQ_API_KEY is missing. Configure it in Streamlit Secrets.")
    st.stop()

client = st.session_state.client

st.sidebar.title("🎯 Interview Studio")
st.sidebar.caption("Customize your AI interview")

role = st.sidebar.selectbox(
    "Select Job Role",
    [
        "Python Developer",
        "Java Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "AI Engineer",
        "Data Scientist",
        "Software Engineer",
        "Frontend Developer",
        "Backend Developer",
        "HR Executive"
    ]
)

difficulty = st.sidebar.select_slider(
    "Difficulty Level",
    options=["Beginner", "Intermediate", "Advanced"],
    value="Intermediate"
)

experience = st.sidebar.selectbox(
    "Experience Level",
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
    5,
    20,
    5,
    step=5
)

topics = st.sidebar.multiselect(
    "Technical Topics",
    [
        "Python",
        "Java",
        "OOP",
        "DSA",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "Data Analysis",
        "Problem Solving",
        "Communication Skills"
    ],
    default=["Python", "OOP"]
)

include_answers = st.sidebar.toggle(
    "Include Expected Answers",
    value=True
)

st.sidebar.divider()

st.sidebar.subheader("📊 Interview Statistics")
st.sidebar.metric("Interviews Generated", len(st.session_state.history))

st.markdown(
    '<div class="main-title">🎯 AI Interview Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI-powered technical interview preparation platform.</div>',
    unsafe_allow_html=True
)

st.caption("Developed by ASHRAF ALI 😉")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "🚀 Generate Interview",
    "🧠 Answer Evaluation",
    "📈 Interview History"
])

with tab1:

    st.subheader("Configure Your Interview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**💼 Job Role**")
        st.info(role)

    with col2:
        st.markdown("**⚡ Difficulty**")
        st.info(difficulty)

    with col3:
        st.markdown("**🎓 Experience**")
        st.info(experience)

    if st.button("🚀 Generate Interview Questions", use_container_width=True):

        if not topics:
            st.warning("Please select at least one technical topic.")

        else:
            prompt = f"""
You are a senior technical interviewer and career mentor.

Create {question_count} unique interview questions.

Job Role: {role}
Difficulty: {difficulty}
Experience: {experience}
Topics: {", ".join(topics)}

Requirements:
1. Include conceptual questions.
2. Include practical coding questions where relevant.
3. Include real-world scenario questions.
4. Arrange questions from easy to difficult.
5. Avoid duplicate questions.
6. Make questions relevant to the selected experience level.

{"Include detailed expected answers after each question." if include_answers else "Generate questions only without answers."}

Use clear numbering and professional formatting.
"""

            try:
                with st.spinner("🤖 AI is preparing your interview..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert technical interviewer."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        max_completion_tokens=5000
                    )

                    result = response.choices[0].message.content

                    st.session_state.questions = result
                    st.session_state.feedback = ""

                    st.session_state.history.append({
                        "role": role,
                        "difficulty": difficulty,
                        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "questions": result
                    })

                    st.success("Interview questions generated successfully!")

            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

    if st.session_state.questions:

        st.divider()
        st.subheader("📋 Generated Interview Questions")

        st.markdown(st.session_state.questions)

        st.download_button(
            "⬇️ Download Interview Questions",
            data=st.session_state.questions,
            file_name="AI_Interview_Questions.txt",
            mime="text/plain",
            use_container_width=True
        )

with tab2:

    st.subheader("🧠 AI Answer Evaluation")

    st.write(
        "Submit your interview answer and let AI evaluate your technical knowledge."
    )

    question = st.text_area(
        "Interview Question",
        placeholder="Enter the interview question here...",
        height=100
    )

    answer = st.text_area(
        "Your Answer",
        placeholder="Write your answer here...",
        height=200
    )

    if st.button("📊 Evaluate My Answer", use_container_width=True):

        if not question.strip() or not answer.strip():
            st.warning("Please enter both the question and your answer.")

        else:

            evaluation_prompt = f"""
You are a strict but supportive professional technical interviewer.

Evaluate the candidate's answer.

Job Role: {role}
Difficulty: {difficulty}

Question:
{question}

Candidate Answer:
{answer}

Provide the following evaluation:

1. Score out of 10.
2. Technical accuracy.
3. Strengths.
4. Missing concepts.
5. Mistakes or misunderstandings.
6. Improved sample answer.
7. Suggestions to improve.

Be accurate, constructive and specific.
Do not award high marks for incorrect or incomplete answers.
"""

            try:
                with st.spinner("🔍 AI is evaluating your answer..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an experienced technical interviewer and evaluator."
                            },
                            {
                                "role": "user",
                                "content": evaluation_prompt
                            }
                        ],
                        temperature=0.4,
                        max_completion_tokens=2500
                    )

                    feedback = response.choices[0].message.content

                    st.session_state.feedback = feedback

                st.success("Answer evaluation completed!")

            except Exception as e:
                st.error(f"Evaluation failed: {str(e)}")

    if st.session_state.feedback:

        st.divider()
        st.subheader("📈 Your Performance Report")

        st.markdown(st.session_state.feedback)

        st.download_button(
            "⬇️ Download Evaluation",
            data=st.session_state.feedback,
            file_name="Interview_Evaluation.txt",
            mime="text/plain",
            use_container_width=True
        )

with tab3:

    st.subheader("📈 Interview History")

    if st.session_state.history:

        for index, item in enumerate(reversed(st.session_state.history), 1):

            with st.expander(
                f"Interview {index} | {item['role']} | {item['date']}"
            ):

                st.write("**Job Role:**", item["role"])
                st.write("**Difficulty:**", item["difficulty"])
                st.markdown(item["questions"])

    else:
        st.info("No interviews generated yet.")

    if st.session_state.history:

        if st.button("🗑️ Clear Interview History"):
            st.session_state.history = []
            st.rerun()

st.divider()

st.markdown(
    "<center>Built with ❤️ using Python, Streamlit and Groq AI</center>",
    unsafe_allow_html=True
)
