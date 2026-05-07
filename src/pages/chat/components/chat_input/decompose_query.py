from processing.query import break_down_query, search_database
from prompts import BREAKDOWN_USER_PROMPT_INTO_SUB_PROMPTS
from utils import get_survey_summary


def decompose_query(question, collection, bm25, st) -> list[dict]:
    """Break question into sub-questions, retrieve chunks per sub-question.

    Returns a list of {"question": str, "results": list[dict]} — one entry
    per sub-question, with its own deduplicated retrieved chunks.
    """
    survey_summary = get_survey_summary(st)
    sub_questions = break_down_query(
        BREAKDOWN_USER_PROMPT_INTO_SUB_PROMPTS.format(
            user_question=question, user_profile=survey_summary
        )
    )
    st.session_state.sub_questions = sub_questions

    grouped: list[dict] = []

    st.markdown("**Sub-questions generated:**")
    for q in sub_questions:
        st.markdown(f"**{q['question']}**")
        st.markdown("Relevant queries:")

        seen_ids: set[str] = set()
        results: list[dict] = []

        for query in q["queries"]:
            st.markdown(f"- {query}")
            for chunk in search_database(query, collection, bm25):
                if chunk["id"] not in seen_ids:
                    seen_ids.add(chunk["id"])
                    results.append(chunk)

        grouped.append({"question": q["question"], "results": results})

    return grouped