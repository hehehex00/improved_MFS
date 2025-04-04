"""File Router."""
from data_toolbox.multi_file_search.file_router import (
    search_csv,
    search_docx,
    search_pdf,
    search_pptx,
    search_txt,
    search_xls,
    search_xlsx,
)


def get_extension(file) -> str:
    """Return a file's extension."""
    return file.name.split(".")[-1].lower()

def router(file, search_terms, search_options):
    """Router for files.

    Args:
    ----
        file (file): a file uploaded through streamlit's UI
        search_terms (list): Keywords to search the file for
        search_options (dictionary): configuration for search

    Returns:
    -------
        list: search results

    """
    match get_extension(file):
        case "csv":
            search_results = search_csv(file, search_terms, search_options)
        case "xls":
            search_results = search_xls(file, search_terms, search_options)
        case "xlsx":
            search_results = search_xlsx(file, search_terms, search_options)
        case "docx":
            search_results = search_docx(file, search_terms, search_options)
        case "pdf":
            search_results = search_pdf(file, search_terms, search_options)
        case "pptx":
            search_results = search_pptx(file, search_terms, search_options)
        case "txt":
            search_results = search_txt(file, search_terms, search_options)
    return search_results
