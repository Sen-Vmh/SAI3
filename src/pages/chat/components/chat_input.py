import streamlit as st
from processing.query import ask

def chat_input(collection, bm25):
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