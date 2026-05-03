import streamlit as st

def init_session_state():
    """Initializes all required session state variables."""
    if "survey_complete" not in st.session_state:
        st.session_state.survey_complete = False
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggested_questions" not in st.session_state:
        st.session_state.suggested_questions = []