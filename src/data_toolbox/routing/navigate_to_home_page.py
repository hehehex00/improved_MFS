import streamlit as st

session_state_key__selected_tool_name = "selected_tool_name"


def navigate_to_home_page():
    """Navigate the user to the "Home" page.

    Returns
    -------
    None

    """
    st.session_state["current_page"] = "Home Page"
    st.switch_page("main.py")
