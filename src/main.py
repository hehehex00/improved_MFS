# noqa: INP001 Don't want __init__.py in the top level for pytest
"""Start point for the streamlit app."""
from __future__ import annotations

import logging
import os

# Supress TensorFlow warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

logging.basicConfig(level=logging.INFO)
import random
import warnings
from pathlib import Path

# Supress more warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")

import streamlit as st

from data_toolbox.application_layout.application_layout import embed_in_application_layout
from data_toolbox.tag_manager.singletons import coordinator, manager
from data_toolbox.utils import Greeting, greetings
from pages.tool_wizard import tool_wizard
from toolbox_logging import (
    toolbox_logger,  #, attach_identity_cookie, log_activity, get_all_cookies
)

toolbox_logger.setup_logging()
log = logging.getLogger("Toolbox")


def display_home_page():
    """Display "Home" Component.

    Returns
    -------
    None

    """
    #attach_identity_cookie()
    #log_activity("example")
    display_international_greeting()

    st.divider()
    
    st.subheader("Welcome to the Data Toolbox 🧰")
    st.write("""
    Get started by selecting one of the navigation options in the sidebar
    or using the 🧙🏽‍♂️ Tool Wizard below.
    """)

    tool_wizard()

def display_international_greeting():
    """Display a greeting in a language of one of the participating countries.

    Returns
    -------
    None

    """
    #log_activity("international greeting display")
    greeting: Greeting \
        = random.choice(greetings)  # noqa: S311 - not used for security related task
    st.title(":flag-" + greeting["iso_code"] + ": " + greeting["greeting"])
    st.caption("That is 'Hello' in {} ({}) as spoken in {} ({})".format(
        greeting["language"], greeting["language_in_english"],
        greeting["country"], greeting["country_in_english"]),
    )

# Run the Streamlit application
if __name__ == "__main__":
    # Track Current Page.

    st.session_state["current_page"] = "Home Page"
    tag_file = Path(Path(__file__).parent,
                    "data_toolbox",
                    "tag_manager",
                    "tags.jsonl").resolve()

    manager.import_tags(tag_file)
    association_file = Path(Path(__file__).parent,
                            "data_toolbox",
                            "tag_manager",
                            "associations.jsonl").resolve()

    coordinator.import_associations(association_file)
    embed_in_application_layout(display_home_page)
