import streamlit as st

from data_toolbox.routing import navigate_to_tool_page
from data_toolbox.st_components.vertical_space import vertical_space
from data_toolbox.tag_manager.singletons import coordinator, manager
from tool_metadata import ToolMetadata


def tool_preview(tool: ToolMetadata):
    """Render a preview of the tool metadata.

    Parameters
    ----------
    tool : ToolMetadata
        The metadata of the tool to preview.

    Returns
    -------
    None

    """
    with st.container(border=True):
        image_colum, text_colum = st.columns([1,3])

        with image_colum:
            if tool.get_image_path():
                st.image(tool.get_image_path(), width=80)

        with text_colum:
            text = _format_tool_text(tool)
            st.markdown(text)
            tags = _format_tags(tool)
            st.markdown(tags, unsafe_allow_html=True)

        tool_name = tool.get_tool_name()
        select_tool = st.button(
            "Open " + tool_name,
            use_container_width=True,
            args=[tool.get_tool_name()],
            type="primary",
            key={tool.get_tool_name()},
        )
        if select_tool:
            navigate_to_tool_page(tool.get_tool_name())

    vertical_space(2)

def _format_tool_text(tool) -> str:
    """Ensure tool description text is formatted similarly.

    Previously when displayed, the boxes created would be of differing sizes.
    This irritated Mark so he felt the need to figure out the formatting.

    Parameters
    ----------
    tool : ToolMetadata
        The tools metadata to be formatted.

    Returns
    -------
    str
        A nicely formatted string to be written using st.markdown()

    """
    tool_name = _format_tool_name(tool.get_tool_name())

    return (f"#### {tool_name}  \n"
            f":orange[{tool.get_uses()}]  \n"
            f":gray[{tool.get_accepted_file_types().lower()}]  \n"
            )

def _format_tool_name(tool_name: str) -> str:
    """Ensure the tool name fits nicely in its display box.

    Parameters
    ----------
    tool_name : str
        The name of the tool to be formatted.

    Returns
    -------
    str
        The formatted tool name.

    """
    char_count = 25
    formatted_tool_name = tool_name

    # Tool name is short enough it can fit
    if len(formatted_tool_name) < char_count:
        pass

    else: # otherwise allows as many full words in the name as possible.
        counter = 0
        formatted_tool_name = ""
        words_in_name = tool_name.split(" ")
        word_count = len(words_in_name)

        # Start adding words in the name stopping before it gets too long.
        while (counter < word_count
               and len(formatted_tool_name + " " + words_in_name[counter]) < char_count):

            formatted_tool_name = formatted_tool_name + " " + words_in_name[counter]
            counter += 1

    return formatted_tool_name

def _format_tags(tool) -> str:
    """Construct HTML for the tool's associated tags.

    Parameters
    ----------
    tool : ToolMetadata
        The tools metadata to be formatted.

    Returns
    -------
    str
        A nicely formatted string to be written using st.markdown()

    """
    tags_markup = ""
    association = coordinator.get_association(tool.get_tool_name())
    for tag_id in association.tags:
        tag = manager.get_tag_by_id(tag_id)
        if tag:
            tags_markup = tags_markup + tag.to_html()
    return tags_markup
