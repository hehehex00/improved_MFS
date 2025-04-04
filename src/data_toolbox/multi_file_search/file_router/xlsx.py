"""XLSX File Handler."""
import pandas as pd

from data_toolbox.multi_file_search.utils import (
    tabular_search,
)


def search_xlsx(file, search_terms, search_options):
    """Search XLSX for Search Terms.

    Args:
    ----
        file (file): a XLSX file uploaded through streamlit's UI
        search_terms (list): Keywords to search the file for
        search_options (dictionary): configuration for search

    Returns:
    -------
        list: search results

    """
    results = []

    # Read the file
    try:
        file_data_frames = pd.read_excel(file, None, header=None)
    except Exception:  # noqa: BLE001
        return [{
            "file": file.name,
            "location": "Error reading file",
        }]

    # Search each sheet
    for sheet_name, sheet_df in file_data_frames.items():
        results.extend(tabular_search(
            file_name=file.name,
            df=sheet_df,
            search_terms=search_terms,
            search_options=search_options,
            sheet_name=sheet_name,
        ))

    return results
