from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from data_toolbox.application_layout import embed_in_application_layout
from data_toolbox.st_components.tool_gallery import tool_gallery
from data_toolbox.st_components.vertical_space import vertical_space
from data_toolbox.utils import determine_file_extensions, file_upload_result_to_file_list
from data_toolbox.utils.tool_extensions import supports_all_file_types
from data_toolbox.utils.uploaded_file_extensions import (
    store_uploaded_files_for_page_switch,
)
from tool_dictionary import tool_list

if TYPE_CHECKING:
    from tool_metadata import ToolMetadata


def tool_wizard():
    """Display the tool wizard.

    The wizard allows you to choose a tool applicable to the file(s) you upload.
    The uploads are stored using `store_uploaded_files_for_page_switch`
    and can be restored using one of:
    - `restore_uploaded_files`
    - `restore_first_uploaded_file`

    Returns
    -------
    None

    """
    st.markdown("""
    The tool wizard looks at your uploaded file(s)
    and based on that recommends you tools applicable to the provided dataset.
    """)

    uploaded_files = st.file_uploader("Just drop a file and let him work his magic. ✨",
                                      accept_multiple_files=True, key="script_runner")
    store_uploaded_files_for_page_switch(uploaded_files)

    file_list = file_upload_result_to_file_list(uploaded_files)
    if len(file_list) <= 0:
        st.info("You need to upload at least one file.", icon="ℹ️")
        return

    vertical_space(1)

    file_extensions: set[str] = determine_file_extensions(file_list)
    applicable_tools: list[ToolMetadata] = \
        [tool for tool in tool_list() if supports_all_file_types(tool, file_extensions)
         and tool.get_category() != "admin" and tool.get_visibility()]

    # Sort tools by their name in ascending order
    applicable_tools = sorted(applicable_tools, key=lambda tool: tool.get_tool_name())

    if len(applicable_tools) > 0:
        st.subheader("Tool compatible with uploaded file(s):")
        tool_gallery(applicable_tools)
    else:
        st.warning("Oh no, no tools are compatible with uploaded files.", icon="😱")


def tool_wizard_page():
    """Display "Tool Wizard" component.

    Returns
    -------
    None

    """
    st.title("🧙🏽‍♂️ Tool Wizard")

    tool_wizard()


if __name__ == "__main__":
    # Track Current Page
    st.session_state["current_page"] = "Tool Wizard"
    embed_in_application_layout(
        tool_wizard_page,
        page_title="Data Toolbox - 🧙🏽‍♂️ Tool Wizard",
    )
