import streamlit as st
from modules.live_interview import start_live_interview
from modules.full_pipeline import run_full_interview_analysis

st.set_page_config(page_title="Interview Intelligence System", layout="centered")

st.title("🎤 Live Mock Interview Intelligence System")

# ---- SESSION STATE INITIALIZATION ----
if "candidate" not in st.session_state:
    st.session_state.candidate = ""

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "interview_done" not in st.session_state:
    st.session_state.interview_done = False

# ---- INPUTS ----
st.session_state.candidate = st.text_input(
    "Candidate Name",
    value=st.session_state.candidate
)

st.session_state.topic = st.text_input(
    "Interview Topic",
    value=st.session_state.topic
)

# ---- START INTERVIEW ----
if st.button("Start Live Mock Interview"):
    st.info("Interview started. Answer the questions on screen.")
    start_live_interview()
    st.session_state.interview_done = True
    st.success("Interview completed!")

# ---- ANALYZE INTERVIEW ----
if st.button("Analyze Interview & Generate Report"):
    if not st.session_state.interview_done:
        st.warning("Please complete the mock interview first.")
    elif st.session_state.candidate.strip() == "" or st.session_state.topic.strip() == "":
        st.warning("Please enter candidate name and topic.")
    else:
        results, report = run_full_interview_analysis(
            st.session_state.candidate,
            st.session_state.topic
        )

        st.subheader("📊 Interview Performance")
        for k, v in results.items():
            st.write(f"**{k}**: {v[0]} ({v[1]})")

        st.success("📄 PDF Report Generated Successfully!")
        st.write(report)
