import streamlit as st
from pages.chat.components.chat_input.decompose_query import decompose_query
from processing.query import synthesize_answer
from utils import get_survey_summary

def chat_input(collection, bm25):
    pending = st.session_state.pop("pending_question", None)
    typed = st.chat_input("What do you want to know?")
    question = pending or typed

    if question:
        st.session_state.messages = []  # fresh context every question
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching and generating..."):
                grouped = decompose_query(question, collection, bm25, st)

            user_profile = get_survey_summary(st)
            answer_parts: list[str] = []
            all_sources: list[dict] = []
            seen_source_ids: set[str] = set()

            for item in grouped:
                with st.spinner(f"Answering: {item['question']}"):
                    part = synthesize_answer(item["question"], item["results"], user_profile)

                st.markdown(f"**{item['question']}**")
                st.markdown(part)
                st.divider()

                answer_parts.append(f"**{item['question']}**\n{part}")

                for chunk in item["results"]:
                    if chunk["id"] not in seen_source_ids:
                        seen_source_ids.add(chunk["id"])
                        all_sources.append(chunk)

            full_answer = "\n\n---\n\n".join(answer_parts)

            with st.expander("Sources"):
                for s in all_sources:
                    st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                    st.caption(s["text"][:300] + "...")

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_answer,
            "sources": all_sources,
        })