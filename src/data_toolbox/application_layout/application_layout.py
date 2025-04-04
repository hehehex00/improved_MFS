import os
from typing import Callable

import streamlit as st

from data_toolbox.analytics_integration.analytics_context import *  # noqa: F403
from data_toolbox.st_components.sidebar_navigation.sidebar_navigation import (
    sidebar_navigation,
)
from data_toolbox.utils import get_loading_message


def embed_in_application_layout(body: Callable[[], None],
                                page_title: str = "Data Toolbox",
                                page_icon: str = "./images/data-team-redder.png"):
    """Create an application layout around the provided body.

    Sets the title and icon for the page.

    Parameters
    ----------
    body : Callable[[], None]
        Function that is called for adding content to the application body.
    page_title : str
        The title of the page which will be displayed in the browser tab.
    page_icon : str
        The icon of the page which will be displayed in the browser tab.

    Returns
    -------
    None

    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    sidebar_navigation()

    analytics_context = get_analytics_context() # noqa: F405
    if analytics_context is not None:
        with analytics_context:
            body()
    else:
        body()

    #caption = "Current version: " + os.environ.get("VERSION") + "   |   " + "Built with \U00002764 by the Data Team"

    #st.caption("<div style='text-align: center'>" + caption + "</div>", unsafe_allow_html=True)

def print_welcome_message():
    """Print a welcome message to the console."""
    # There has to be weird offsets to get it to display properly... don't know why.
    print("                                        Welcome to the                                               ")
    print(" ____              __                        ______               ___    __                          ")
    print("/\  _ `\          /\ \__                    /\__  _\             /\_ \  /\ \                         ")  # noqa: W605
    print("\ \ \/\ \     __  \ \ ,_\    __             \/_/\ \/   ___     ___\/\ \ \ \ \____    ___   __  _     ")  # noqa: W605
    print(" \ \ \ \ \  /'__`\ \ \ \/  /'__`\              \ \ \  / __`\  / __`\ \ \ \ \ '__`\  / __`\/\ \/'\    ")  # noqa: W605
    print("  \ \ \_\ \/\ \L\.\_\ \ \_/\ \L\.\_             \ \ \/\ \L\ \/\ \L\ \_\ \_\ \ \L\ \/\ \L\ \/>  </    ")  # noqa: W605
    print("   \ \____/\ \__/. \_\ \_ \ \__/.\_\             \ \_\ \____/\ \____//\____\ \_,__/\ \____//\_/\_\   ")  # noqa: W605
    print("    \/___/  \/__/\/_/ \/__/\/__/\/_/              \/_/\/___/  \/___/ \/____/\/___/  \/___/ \//\/_/   ")  # noqa: W605

    print("\n\n" + get_loading_message.get_loading_message())

print_welcome_message()
