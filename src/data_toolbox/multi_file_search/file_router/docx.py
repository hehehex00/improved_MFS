"""DOCX File Handler."""
import docx2txt

from data_toolbox.multi_file_search.utils.utils import (
    document_search,
)


def search_docx(file, search_terms, search_options):
    """Search DOCX for Search Terms.

    Args:
    ----
        file (file): a DOCX file uploaded through streamlit's UI
        search_terms (list): Keywords to search the file for
        search_options (dictionary): configuration for search

    Returns:
    -------
        list: search results

    """
    try:
        # Read document
        document_string = docx2txt.process(file)
        # Create a list from the document content:
        document_list = document_string.split("\n")
    except Exception:  # noqa: BLE001
        return [{
            "file": file.name,
            "location": "Error reading file",
        }]

    # use generic document search function
    return document_search(
        file_name=file.name,
        line_list=document_list,
        search_terms=search_terms,
        search_options=search_options,
        location_context="",
    )
