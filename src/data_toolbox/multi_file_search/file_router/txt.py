"""TXT File Handler."""

from data_toolbox.multi_file_search.utils import (
    detect_encoding,
    document_search,
)


def search_txt(file, search_terms, search_options):
    """Search TXT for Search Terms.

    Args:
    ----
        file (file): a TXT file uploaded through streamlit's UI
        search_terms (list): Keywords to search the file for
        search_options (dictionary): configuration for search

    Returns:
    -------
        list: search results

    """
    try:
        # Determine the file encoding:
        encoding = detect_encoding(file)
        # Read the file:
        txt_reader = file.getvalue().decode(encoding)
        # Create a list from the document content:
        line_list = txt_reader.split("\n")
    except Exception:  # noqa: BLE001
        return [{
            "file": file.name,
            "location": "Error reading file",
        }]

    return document_search(
        file_name=file.name,
        line_list=line_list,
        search_terms=search_terms,
        search_options=search_options,
        location_context="",
    )


