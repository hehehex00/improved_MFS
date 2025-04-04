import random
from pathlib import Path

import streamlit as st

import tool_dictionary
from data_toolbox.application_layout.application_layout import embed_in_application_layout
from data_toolbox.st_components.tool_gallery import tool_gallery
from data_toolbox.st_components.vertical_space import vertical_space
from data_toolbox.tag_manager.singletons import coordinator, manager


def display_featured_tools():
    """Display "Featured Tools" Component.

    Annotate any number of tools as 'featured' but this function currently
    limits the number displayed to six.

    Returns
    -------
    None

    """
    st.title("🎉 Featured Tools")
    st.markdown("""
    Pick one of the featured tools deemed especially useful.
    """)
    vertical_space(1)

    # Limit number of tools to be presented to 6 so that it is aesthetically
    # pleasing and doesn't overwhelm the user.
    num_to_show = 6

    # List of tools we determined we want to display
    if "featured" not in st.session_state:
        set_app_list(num_to_show)

    tool_gallery(st.session_state["featured"][:num_to_show])


def set_app_list(num_to_show):
    """Set the list of featured tools in session state.

    The list is capped at a given number, and if the number of featured tools
    is less than the cap, the remaining spots are filled with random tools
    that are not in the "admin" category and are visible.

    Parameters
    ----------
    num_to_show : int
        The maximum number of tools to display on the page.

    """
    st.session_state["featured"] = [tool for tool in tool_dictionary.tool_list()
                                    if tool.get_featured()
                                    and tool.get_category() != "admin"
                                    and tool.get_visibility()]

    num_to_fill = num_to_show - len(st.session_state["featured"])
    if num_to_fill < 0:
        return

    other_tools = [tool for tool in tool_dictionary.tool_list()
                   if not tool.get_featured()
                   and tool.get_category() != "admin"
                   and tool.get_visibility()]

    other_tools = random.sample(other_tools, num_to_fill)
    st.session_state["featured"] = st.session_state["featured"] + other_tools


if __name__ == "__main__":
    # Track current Page
    st.session_state["current_page"] = "Featured Tools"
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
        display_featured_tools,
        page_title="Data Toolbox - 🎉 Featured Tools",
    )
