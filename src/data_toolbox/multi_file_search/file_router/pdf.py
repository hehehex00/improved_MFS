"""PDF File Handler."""
import pypdf

from data_toolbox.multi_file_search.utils.utils import (
    document_search,
)


def search_pdf(file, search_terms, search_options):
    """Search PDF for Search Terms.

    Args:
    ----
        file (file): a PDF file uploaded through streamlit's UI
        search_terms (list): Keywords to search the file for
        search_options (dictionary): configuration for search

    Returns:
    -------
        list: search results

    """
    results = []

    # Read the file
    try:
        pdf_reader = pypdf.PdfReader(file)
    except Exception:  # noqa: BLE001
        return [{
            "file": file.name,
            "location": "Error reading file",
        }]

    # Search each page in the PDF
    for page in range(len(pdf_reader.pages)):
        # read page content
        page_content = pdf_reader.pages[page].extract_text()
        # Create a list from the page content
        lines = page_content.split("\n")
        # use generic document search function (treat each page as a document)
        results.extend(document_search(
            file_name=file.name,
            line_list=lines,
            search_terms=search_terms,
            search_options=search_options,
            location_context=f"Page {page + 1},",
        ))
    return results
