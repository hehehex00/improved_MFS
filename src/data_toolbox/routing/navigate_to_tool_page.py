import streamlit as st

session_state_key__selected_tool_name = "selected_tool_name"

def navigate_to_tool_page(tool_name: str):
    """Navigate the user to the "Tool" page.

    Parameters
    ----------
    tool_name : str
        The name of the tool to use

    Returns
    -------
    None

    """
    st.session_state[session_state_key__selected_tool_name] = tool_name
    st.switch_page("pages/tools.py")
