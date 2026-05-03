import streamlit as st

from processing.query import suggest_questions
from utils import get_survey_summary

def suggest_questions_component():
    if len(st.session_state.get("suggested_questions", [])) == 0:
        with st.spinner("Generating suggested questions..."):
            survey_summary = get_survey_summary(st)
            st.session_state.suggested_questions = suggest_questions(survey_summary)

    if st.session_state.suggested_questions and not st.session_state.messages:
        st.markdown("**Suggested questions based on your portfolio:**")
        for q in st.session_state.suggested_questions:
            if st.button(q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()