import streamlit as st
from chromadb.api.models.Collection import Collection
from processing.query import BM25, build_index, get_collection

@st.cache_resource(show_spinner="Loading document index...")
def load_resources() -> tuple[Collection, BM25]:
        collection = get_collection()
        bm25 = build_index(collection)
        return collection, bm25