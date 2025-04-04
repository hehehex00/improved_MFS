"""Read and display the markdown file for the tool."""
from pathlib import Path

import streamlit as st


def tool_about_section(about_markdown_path, instructions_markdown_path):
    """Display the informative documentation about a tool.

    Parameters
    ----------
    about_markdown_path : str
        Path to the tools "about.md" file.

    instructions_markdown_path : str
        Path to the tools "instructions.md" file.

    Returns
    -------
    None

    """
    about_markdown = read_markdown_file(about_markdown_path)
    instructions_markdown = read_markdown_file(instructions_markdown_path)
    # About this tool
    st.markdown(about_markdown, unsafe_allow_html=True)
    st.write("") # small spacer
    # How it works
    with st.expander("How this tool works", expanded=False):
        st.markdown(instructions_markdown, unsafe_allow_html=True)
    st.divider()

def read_markdown_file(markdown_file):
    """"Read and return the contents of the markdown file.

    Parameters
    ----------
    markdown_file : str
        The path to the markdown file to be read.

    Returns
    -------
    str
        The text in the markdown file.

    """
    return Path(markdown_file).read_text(encoding="utf-8")
