from __future__ import annotations

from pathlib import Path

import streamlit as st

from data_toolbox.application_layout.application_layout import embed_in_application_layout
from data_toolbox.routing import (
    navigate_to_feedback_page,
    navigate_to_home_page,
    session_state_key__selected_tool_name,
)
from data_toolbox.tag_manager.singletons import coordinator, manager
from tool_dictionary import tool_list


def determine_tool_name() -> str | None:
    """Determine the name of the selected tool name.

    Selection is based on either Streamlit's session_state or query parameter.

    Returns
    -------
    str or None

    """
    tool_name: str | None = None

    if "tool" in st.query_params:
        tool_name = st.query_params["tool"]
    elif session_state_key__selected_tool_name in st.session_state:
        tool_name = st.session_state[session_state_key__selected_tool_name]

    # reset session_state to ensure it does not conflict with the query parameter
    st.session_state[session_state_key__selected_tool_name] = None
    st.session_state["current_page"] = tool_name

    return tool_name

selected_tool_name: str = determine_tool_name()

def display_tool():
    """Display the tool out of the toolbox that was selected.

    Returns
    -------
    None

    """
    if not selected_tool_name:
        st.header("No tool selected ️🤷‍♀️")
        st.markdown("""
        It seems like no tool was selected.
        If you think that's an error, please provide feedback.
        Otherwise, you may want to return to the home page.
        """)
        feedback_button = st.button(label="💬 Give Feedback", type="primary")
        if feedback_button:
            navigate_to_feedback_page()
        home_button = st.button(label="🏠🚶🏻‍♀️ Go home",
                                type="primary",
                                key="script_runner")
        if home_button:
            navigate_to_home_page()

    else:
        # add tool selection as query parameter, to hyperlink can be shared / bookmarked
        st.query_params["tool"] = selected_tool_name
        # Reference app selection from URL
        for tool in tool_list():
            if selected_tool_name == tool.get_tool_name():
                # If we have a defined port, tool is hosted in a separate docker image.
                if tool.get_port() is not None:
                    tool.get_tool()(tool.get_port())
                else:
                    tool.get_tool()()
                break

if __name__ == "__main__":
    tag_file = (Path(__file__).parent.parent /
        "data_toolbox" /
        "tag_manager" /
        "tags.jsonl")
    manager.import_tags(tag_file)

    association_file = (Path(__file__).parent.parent /
                "data_toolbox" /
                "tag_manager" /
                "associations.jsonl")
    coordinator.import_associations(association_file)
    embed_in_application_layout(
        display_tool,
        page_title="Data Toolbox - 🔨" + (selected_tool_name or "Tool"),
    )
