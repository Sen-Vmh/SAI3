import streamlit as st

def messages():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                        st.caption(s["text"][:300] + "...")