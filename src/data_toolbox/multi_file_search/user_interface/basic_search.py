"""Basic Search User Interface."""

import streamlit as st
from streamlit_tags import st_tags

from data_toolbox.multi_file_search.user_interface.components import (
    case_sensitive_checkbox,
    multi_file_uploader,
    step_component,
    whole_word_search_checkbox,
)
from data_toolbox.multi_file_search.utils.utils import strip_list
from data_toolbox.utils import (
    display_restored_uploaded_files,
    restore_uploaded_files,
    were_files_restored,
)


def basic_search():
    """User Interface for Basic Search Mode."""
    with st.expander("More Options"):
        case_sensitive = case_sensitive_checkbox()
        whole_word_search = whole_word_search_checkbox()
    search_options={
        "mode": "regular",
        "case-sensitive": case_sensitive,
        "whole-word": whole_word_search,
    }
    step_component("2. Upload files to be searched")
    uploaded_files = restore_uploaded_files()
    if were_files_restored(uploaded_files):
        display_restored_uploaded_files(uploaded_files)
    else:
        uploaded_files = multi_file_uploader()
    step_component("3. Type in search terms and *press enter*")
    search_terms = st_tags(
        label="",
        text="Type in search term and press enter to add it",
        key="search_terms",
    )
    # convert all values to strings and remove trailing whitespace
    preprocessed_search_terms = strip_list(search_terms)
    return (uploaded_files, preprocessed_search_terms, search_options)
