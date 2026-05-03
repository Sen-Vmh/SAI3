import streamlit as st
from components.chat import render_chat
from components.sidebar import render_sidebar
from components.survey import render_survey
from core.state import init_session_state

# 1. Page Config
st.set_page_config(page_title="Finance RAG", layout="centered")

# 2. Initialize State
init_session_state()

# 3. Routing / Conditional Rendering
if not st.session_state.survey_complete:
    render_survey()

else:
    render_sidebar()
    render_chat()