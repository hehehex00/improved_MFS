"""Components.

A collection of custom streamlit UI components used in the multi-file-search tool.
"""
import streamlit as st


def case_sensitive_checkbox():
    """Case Sensitive Checkbox.

    A Streamlit UI component for displaying a "case-sensitive" checkbox.
    """
    label="Case Sensitive"
    key="case_sensitive"
    help_message = """
        When checked, the search will **not** match uppercase with lowercase
        letters. The word "Apple" will not match with "apple".
        """
    return st.checkbox(label, key=key, help=help_message)

def whole_word_search_checkbox():
    """Whole Word Search Checkbox.

    A Streamlit UI component for displaying a "whole word" checkbox.
    """
    label="Whole Word"
    key="whole_word"
    help_message = """
        When checked, the search will **only** match complete words.
        The word "hour" will not match with "hourglass".
        """
    return st.checkbox(label, key=key, help=help_message)

def step_component(message, help_message=None):
    """Step Component.

    A Streamlit UI component for displaying step-by-step directions.
    """
    return st.markdown(f"**:gray[{message}]**", help=help_message)

def multi_file_uploader():
    """Multi File Uploader.

    Streamlit UI Component for uploading files.
    This code should be edited as new file types are supported
    """
    valid_search_files=["docx", "pdf", "pptx", "txt", "xls", "xlsx", "csv"]
    return st.file_uploader(
        "Upload files to be searched here",
        label_visibility="collapsed",
        type=valid_search_files,
        accept_multiple_files=True,
    )
