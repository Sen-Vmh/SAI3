from processing.query import break_down_query, search_database
from prompts import BREAKDOWN_USER_PROMPT_INTO_SUB_PROMPTS
from utils import get_survey_summary


def decompose_query(question, collection, bm25, st):
    survey_summary = get_survey_summary(st)
    sub_questions = break_down_query(BREAKDOWN_USER_PROMPT_INTO_SUB_PROMPTS.format(user_question=question, user_profile=survey_summary))
    
    st.session_state.sub_questions = sub_questions

    print(st.session_state.sub_questions)

    st.markdown("**Sub-questions generated:**")
    for idx, q in enumerate(sub_questions):
        st.markdown(f"**{idx + 1}. {q['question']}**")
        st.markdown("Relevant queries:")
        for jdx, query in enumerate(q["queries"]):
            st.markdown(f"- {query}")
            results = search_database(query, collection, bm25)

            st.session_state.sub_questions[idx]["queries"][jdx] = [
                st.session_state.sub_questions[idx]["queries"][jdx],
                results
            ]

            print(st.session_state.sub_questions)