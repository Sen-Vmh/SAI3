import sys
from pages.chat.components.chat_input.chat_input import chat_input
from pages.chat.components.messages import messages
from pages.chat.components.load_resources import load_resources_component
from pages.chat.components.sidebar import render_sidebar
from pages.chat.components.suggest_question import suggest_questions_component
import streamlit as st
from pathlib import Path


def render_chat():
    render_sidebar()

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    # st.set_page_config(page_title="Finance RAG", layout="centered")
    st.title("Finance RAG")
    st.caption("Ask questions about your financial documents.")
    
    collection, bm25 = load_resources_component()

    suggest_questions_component()

    messages()

    chat_input(collection, bm25)

    
