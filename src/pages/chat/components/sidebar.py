import streamlit as st

def render_sidebar():
    st.sidebar.success("Profile Loaded ✅")

    with st.sidebar.expander("🔍 Your Profile Summary"):
        profile = st.session_state.get("user_profile", {})
        if profile:
            for key, value in profile.items():
                clean_key = key.replace('_', ' ').title()
                if isinstance(value, dict):
                    st.write(f"**{clean_key}:**")
                    for k, v in value.items():
                        if isinstance(v, dict):
                            details = ", ".join(f"{dk}: {dv}" for dk, dv in v.items())
                            st.write(f"  - {k}: {details}")
                        else:
                            st.write(f"  - {k}: {v}")
                else:
                    st.write(f"**{clean_key}:** {value}")

    if st.sidebar.button("Retake Survey"):
        st.session_state.survey_complete = False
        st.rerun()