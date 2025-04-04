"""Common header format for all tools."""
import base64
from pathlib import Path

import streamlit as st


def tool_about_section(about_markdown_path, readme_markdown_path):
    """Display the informative documentation about a tool.

    Parameters
    ----------
    about_markdown_path : str
        Path to the tools "about.md" file.

    readme_markdown_path : str
        Path to the tools "readme.md" file.

    Returns
    -------
    None

    """
    about_markdown = read_markdown_file(about_markdown_path)
    readme_markdown = read_markdown_file(readme_markdown_path)
    # About this tool
    st.markdown(about_markdown, unsafe_allow_html=True)
    st.write("") # small spacer
    # How it works
    with st.expander("How this tool works", expanded=False):
        st.markdown(readme_markdown, unsafe_allow_html=True)
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
    return Path(markdown_file).read_text()

def tool_header(title, uses, nickname=None, logo_path=None, logo_size=120):
    """Top level function to format the tool webpage.

    Parameters
    ----------
    title : str
        The name of the tool.
    uses : str
        A comma separated string of tool uses (e.g. "phone numbers, crypto").
    nickname : str
        The nickname of the tool.
    logo_path : str
        Absolute path of the logo you would like the tool to present.
    logo_size : int
        The square size of the tool logo.

    Returns
    -------
    None

    """
    if logo_path:
        display_logo(logo_path, logo_size)
    display_title(title)
    if nickname:
        display_nickname(nickname)
    display_uses(uses)

def display_logo(png_file, logo_size=120):
    """Print logo to tool page.

    Parameters
    ----------
    png_file : str
        Path to the logo file.
    logo_size : int
        The size square you would like the logo.

    Returns
    -------
    None

    """
    set_png_as_page_bg(png_file, logo_size)

def get_base64_of_bin_file(bin_file):
    """Read a file and base64 encode the data found within.

    Parameters
    ----------
    bin_file : str
        The binary file you want read and encoded.

    Returns
    -------
    str
        Base64 encoded string.

    """
    with Path.open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file, height):
    """Stylize and present a .png file as the background of the page.

    Parameters
    ----------
    png_file : str
        The image.png you would like presented.

    height : int
        The size to display the image.png as.

    Returns
    -------
    None

    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
        <div style="text-align: center;">
        <img src="data:image/png;base64,{bin_str}" style="height:{height}px;">
        </div>
        """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def display_nickname(nickname):
    """Create an element in the webpage to display the tools nickname.

    Parameters
    ----------
    nickname : str
        The nickname of the tool that you would like displayed.

    Returns
    -------
    None

    """
    nickname_html = f"""
        <div style="text-align: center; color: silver;">
            "{nickname}"
        </div>
        """
    st.markdown(nickname_html, unsafe_allow_html=True)

def display_title(title):
    """Create an element in the webpage to display the tools title.

    Parameters
    ----------
    title : str
        The title of the tool you would like displayed.

    Returns
    -------
    None

    """
    title_html = f"""
        <h2 style="text-align: center; padding-bottom: 5px;">
            {title}
        </h2>
        """
    st.markdown(title_html, unsafe_allow_html=True)

def display_uses(uses):
    """Create an element in the webpage to present tool usage info.

    Parameters
    ----------
    uses : str
        A comma separated string of tool uses (e.g. "phone numbers, crypto").

    Returns
    -------
    None

    """
    uses_html = f"""
        <div style="text-align: center; color: orange;">
            {uses}
        </div>
        """
    st.markdown(uses_html, unsafe_allow_html=True)
