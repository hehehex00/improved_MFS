"""Common navigation interface between separated tools.

Must be imported into Dockerfile for apps running separately.
"""
import streamlit as st

from config.config import get_tool_url


def redirect_to_tool(port):
    """Redirect user to tool given port.

    Entry function used by all tools hosted in separate containers.

    Parameters
    ----------
    port : int
        The port the tool's docker container uses.

    Returns
    -------
    None

    """
    match port:
        case 8501:
            tool_name = "datatoolbox"
        case 8503:
            tool_name = "diarization"
        case 8504:
            tool_name = "text_extractor"
        case 8505:
            tool_name = "image_to_text"
        case 8506:
            tool_name = "arab_dialect_id"
        case 8507:
            tool_name = "cem_search"
        case 8508:
            tool_name = "image_triage"
        case 8509:
            tool_name = "hijri_calendar_converter"
        case 8515:
            tool_name = "translation-api"
        case 8510:
            tool_name = "cure"
        # 8516 = mongrel_api
        case _:
            tool_name = "datatoolbox"
        # 8515 = translation-api
        # 8516 = mongrel_api
        # 8519 = hijri_calendar_converter_api
            

    nav_script = f"""
        <meta http-equiv="refresh" content="0; url={get_tool_url(tool_name)}">
    """
    st.write(nav_script, unsafe_allow_html=True)

def redirect_to_home():
    """Redirect users back to home page.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    redirect_to_tool(-1)


def home_button():
    """Create a standard button to navigate back to the Main Streamlit App.

    Paremeters
    ----------
    None

    Returns
    -------
    None

    """
    sidebar = st.sidebar
    with sidebar:
        #Be sure to add/copy the image to your dockerfile in order for this import to work
        st.sidebar.image(
            "./components/data_team_header.webp")
        st.sidebar.divider()

        st.button("Return to Tool Browser", on_click=redirect_to_home,
                   use_container_width=True)
