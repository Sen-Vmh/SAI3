import streamlit as st
from processing.query import load_resources

@st.cache_resource(show_spinner="Loading document index...")
def load_resources_component():
        return load_resources()
