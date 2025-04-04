"""Regex Search User Interface."""

import re

import pandas as pd
import streamlit as st
from streamlit_tags import st_tags

from data_toolbox.multi_file_search.user_interface.components import (
    multi_file_uploader,
    step_component,
)
from data_toolbox.utils import (
    display_restored_uploaded_files,
    restore_uploaded_files,
    were_files_restored,
)


def regex_search():
    """User Interface for Regex Search Mode."""
    search_options={
        "mode": "regex",
        "case-sensitive": False,
        "whole-word": False,
    }
    st.write("#") # large spacer
    step_component("2. Upload files to be searched")
    uploaded_files = restore_uploaded_files()
    if were_files_restored(uploaded_files):
        display_restored_uploaded_files(uploaded_files)
    else:
        uploaded_files = multi_file_uploader()
    step_component(
        "3. Type in a regular expression and *press enter*",
        "Example: `\d{3}\d{3}\d{4}`",  # noqa: W605
        )
    search_terms = st_tags(
        label="",
        text="Type in regular expression and press enter to add it",
        key="search_terms", # matches the key to basic search intentionally
        )
    valid_regex_patterns = []
    display_patterns = []
    for term in search_terms:
        try:
            re.compile(term)
            valid_regex_patterns.append(term)
            display_patterns.append({"Regex Pattern": term, "Valid Pattern": "✅"})
        except re.error:  # noqa: PERF203
            display_patterns.append({"Regex Pattern": term, "Valid Pattern": "❌"})

    st.write(pd.DataFrame(display_patterns))
    return (uploaded_files, valid_regex_patterns, search_options)
