import streamlit as st

session_state_key__selected_tool_name = "selected_tool_name"


def navigate_to_featured_tools_page():
    """Navigate the user to the "Featured Tools" page.

    Returns
    -------
    None

    """
    st.session_state["current_page"] = "Featured Tools"
    st.switch_page("pages/featured_tools.py")
