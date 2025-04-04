"""Search Term File Search User Interface."""
import pandas as pd
import streamlit as st

from data_toolbox.multi_file_search.user_interface.components import (
    case_sensitive_checkbox,
    multi_file_uploader,
    step_component,
    whole_word_search_checkbox,
)
from data_toolbox.multi_file_search.utils.utils import search_term_file_to_list
from data_toolbox.utils import (
    display_restored_uploaded_files,
    restore_uploaded_files,
    were_files_restored,
)


def search_term_file_search():
    """User Interface for Search Term File Upload Mode."""
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
    step_component(
        "3. Upload search term file",
        "The program will only read the first column in the excel",
        )
    uploaded_search_term_file = st.file_uploader(
        "Upload search term file",
        label_visibility="collapsed",
        type=["xlsx","xls"],
        accept_multiple_files=False,
    )
    search_terms=[]
    if uploaded_search_term_file:
        try:
            search_terms = search_term_file_to_list(uploaded_search_term_file)
        except Exception as e:  # noqa: BLE001
            st.error(f"Error reading search terms from Excel file: {str(e)}")
    search_terms_df = pd.DataFrame({"Uploaded Search Terms": search_terms})
    st.write(search_terms_df)

    return (uploaded_files, search_terms, search_options)
