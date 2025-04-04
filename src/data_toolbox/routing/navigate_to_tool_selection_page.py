import streamlit as st

session_state_key__selected_tool_name = "selected_tool_name"


def navigate_to_tool_selection_page():
    """Navigate the user to the "Tool Section" page.

    Returns
    -------
    None

    """
    st.session_state["current_page"] = "Tool Selection"
    st.switch_page("pages/tool_selection.py")
