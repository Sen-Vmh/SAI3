import sys
from processing.query import ask, build_index, get_collection, suggest_questions
import streamlit as st
from pathlib import Path


def render_chat():
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    # st.set_page_config(page_title="Finance RAG", layout="centered")
    st.title("Finance RAG")
    st.caption("Ask questions about your financial documents.")


    @st.cache_resource(show_spinner="Loading document index...")
    def load_resources():
        collection = get_collection()
        bm25 = build_index(collection)
        return collection, bm25


    collection, bm25 = load_resources()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "suggested_questions" not in st.session_state:
        with st.spinner("Generating suggested questions..."):
            profile = st.session_state.get("user_profile", {})
            survey_summary = "\n".join(f"{k}: {v}" for k, v in profile.items())
            st.session_state.suggested_questions = suggest_questions(survey_summary)

    if st.session_state.suggested_questions and not st.session_state.messages:
        st.markdown("**Suggested questions based on your portfolio:**")
        for q in st.session_state.suggested_questions:
            if st.button(q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                        st.caption(s["text"][:300] + "...")

    if question := st.chat_input("What do you want to know?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching and generating..."):
                results, answer = ask(question, collection, bm25)
            st.markdown(answer)
            with st.expander("Sources"):
                for s in results:
                    st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                    st.caption(s["text"][:300] + "...")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": results,
        })
