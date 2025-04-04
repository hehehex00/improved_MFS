"""CSV File Handler.""" # noqa: A005
import pandas as pd

from data_toolbox.multi_file_search.utils.utils import (
    detect_encoding,
    tabular_search,
)


def search_csv(file, search_terms, search_options):
    """Search CSV for Search Terms.

    Args:
    ----
        file (file): a CSV file uploaded through streamlit's UI
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
        csv_df = pd.read_csv(file, encoding=encoding, index_col=None, header=None)
    except Exception:  # noqa: BLE001
        return [{
            "file": file.name,
            "location": "Error reading file",
        }]

    return tabular_search(
            file_name=file.name,
            df=csv_df,
            search_terms=search_terms,
            search_options=search_options,
            sheet_name="",
        )

