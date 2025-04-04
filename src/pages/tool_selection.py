from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import extra_streamlit_components as stx
import streamlit as st
import streamlit_antd_components as sac
from thefuzz import fuzz

from data_toolbox.application_layout.application_layout import embed_in_application_layout
from data_toolbox.st_components.tool_gallery import tool_gallery
from data_toolbox.st_components.vertical_space import vertical_space
from data_toolbox.tag_manager.singletons import coordinator, manager
from tool_dictionary import tool_categories, tool_list

if TYPE_CHECKING:
    from tool_metadata import ToolMetadata

def display_tool_selection():
    """Display "Tool Selection" component.

    Allows users to search the catalogue of available tools.

    Returns
    -------
    None

    """
    st.title("🔎 Tool Search")
    st.markdown("""
    Select one of the tools available in the Data Toolbox.
    Use the filter options in the sidebar to narrow down the results.
    """)
    vertical_space(1)

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="All", description="Display all Tools"),
        stx.TabBarItemData(id=2, title="Data Manipulation", description="Files and Text"),
        stx.TabBarItemData(id=3, title="Translation & Media",
                           description="Languages & Media"),
        stx.TabBarItemData(id=4, title="Maps & Geospatial", description="GEO Tools"),
        stx.TabBarItemData(id=5, title="Social Media & Crypto",
                           description="Finance Tools"),
        stx.TabBarItemData(id=6, title="Machine Learning", description="Powerful Tools"),
        stx.TabBarItemData(id=7, title="Other", description="Everything Else"),
    ], default=1)

    id_dict = {
        1: "All",
        2: "Data Manipulation",
        3: "Translation & Media",
        4: "Maps & GEO Processing",
        5: "Social Media & Cryptocurrency",
        6: "Machine Learning & Data Science",
        7: "Other",
    }

    sac.divider(label=id_dict[int(chosen_id)], icon="house", align="center", color="gray")

    selected_tools: list[ToolMetadata]
    _, selected_tools = _load_available_tools()

    # Filter the tools based on a fuzzy search on their metadata
    search_query: str | None = st.sidebar.text_input(
        "Search Tools",
        placeholder="Search tools by metadata, e.g. name")
    if search_query:
        selected_tools = [tool for tool in selected_tools
                          if _matches_search_query(tool=tool, query_string=search_query)
                          or _is_in_tag(tool=tool, tag_names=[search_query])]
    # # Filter the tools based on a category selection
    if int(chosen_id) != 1:
        selected_tools = [tool for tool in selected_tools
                        if _is_in_category(tool=tool,
                                           category_name=id_dict[int(chosen_id)])]

    # Filter the tools based on their supported input filetypes
    accepted_file_types \
        = chain(*[tool.get_accepted_file_types_list() for tool in selected_tools])
    normalized_accepted_file_types \
        = sorted({category.lower() for category in accepted_file_types})
    selected_file_type: str | None = st.sidebar.selectbox(
        "Filter by Accepted File Type:",
        normalized_accepted_file_types,
        index=None, placeholder="Select Accepted File Type")
    if selected_file_type:
        selected_tools = [tool for tool in selected_tools if
                          selected_file_type.lower() in
                          [accepted_file_type.lower() for accepted_file_type in
                           tool.get_accepted_file_types_list()]]

    selected_tags: str | None = st.sidebar.multiselect(
        "Filter by Tag:",
        [tag.name for tag in manager.tags],
        placeholder="Select Tags")
    if selected_tags:
        selected_tools = [tool for tool in selected_tools if _is_in_tag(tool=tool,
                                                                        tag_names=selected_tags)]
    if len(selected_tools) == 0:
        st.info("Sadly, no tool available matched your search criteria.", icon="ℹ️")
        return

    # Sort tools by their name in ascending order
    selected_tools = sorted(selected_tools, key=lambda tool: tool.get_tool_name())

    # Display a button for each tool
    tool_gallery(selected_tools)


def _load_available_tools() -> tuple[list[str], list[ToolMetadata]]:
    """Initialize the available tools and tool categories and return them.

    Returns
    -------
    tuple[list[str], list[ToolMetadata]]

    """
    manager.reload_tags()
    coordinator.reload_associations()
    available_categories: list[str] = list(tool_categories.values())
    selected_tools: list[ToolMetadata] = tool_list()

    # Remove admin category and tools (if missing "admin" query parameter)
    if "admin" not in st.query_params:
        available_categories.remove("admin")
        selected_tools: list[ToolMetadata] = [tool for tool in selected_tools
                                              if not _is_in_category(tool=tool,
                                                                     category_name="admin")
                                              and tool.get_visibility()
                                              ]

    if "admin" in st.query_params:
        selected_tools = [tool for tool in selected_tools
                          if _is_in_category(tool=tool, category_name="admin")
                          ]

    return available_categories, selected_tools


def _matches_search_query(tool: ToolMetadata, query_string: str) -> bool:
    """Search for the query_string in the tool's metadata fuzzily.

    Returns True if there's a close enough match, else False.

    Parameters
    ----------
    tool : ToolMetadata
        The metadata of the tool to match against
    query_string : str
        The query text that must be found inside the tool's metadata

    Returns
    -------
    bool

    """
    ratio_threshold = 60
    return fuzz.partial_ratio(tool.get_tool_name(), query_string) >= ratio_threshold


def _is_in_category(tool: ToolMetadata, category_name: str) -> bool:
    """Check if the tool is in the category of the provided category_name.

    Parameters
    ----------
    tool : ToolMetadata
        The metadata of the tool to match against
    category_name : str
        The name of the category the tool needs to be in to match

    Returns
    -------
    bool

    """
    return tool.get_category() == category_name

def _is_in_tag(tool: ToolMetadata, tag_names: list[str]) -> bool:
    """Check if the tool is in the tag of the provided tag_name.

    Parameters
    ----------
    tool : ToolMetadata
        The metadata of the tool to match against
    tag_names : List[str]
        The list of tag names the tool needs to be in to match

    Returns
    -------
    bool

    """
    associated_tags = [manager.get_tag_by_id(tag_id) for tag_id in
                            coordinator.get_association(tool.get_tool_name()).tags]

    return any(tag.name in tag_names for tag in associated_tags)

if __name__ == "__main__":
    # Track Current Page
    st.session_state["current_page"] = "Tool Select"
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
        display_tool_selection,
        page_title="Data Toolbox - 🔎 Tool Search",
    )
