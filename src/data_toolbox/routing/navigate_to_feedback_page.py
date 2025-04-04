import streamlit as st

session_state_key__selected_tool_name = "selected_tool_name"


def navigate_to_feedback_page():
    """Navigate the user to the "Feedback" page.

    Returns
    -------
    None

    """
    st.session_state["current_page"] = "Feedback"
    st.switch_page("pages/feedback.py")
