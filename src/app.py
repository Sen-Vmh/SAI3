import streamlit as st

from components.chat import render_chat
from components.sidebar import render_sidebar
from components.survey import render_survey

st.set_page_config(page_title="Finance RAG", layout="centered")

# --- SURVEY STATE ---
if "survey_complete" not in st.session_state:
    st.session_state.survey_complete = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# --- CONDITIONAL DISPLAY ---
if not st.session_state.survey_complete:
    render_survey()

else:
    render_sidebar()
    render_chat()