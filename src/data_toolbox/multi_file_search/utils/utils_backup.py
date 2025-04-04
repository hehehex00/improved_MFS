"""Utils.

A collection of utilities for the Multi-File Search tool.
"""
import re
from io import BytesIO
import concurrent.futures

import chardet
import pandas as pd
import numpy as np


def data_frame_to_excel(df):
    """Convert Data Frame to Excel.

    Args:
    ----
        df: Any DataFrame

    Returns:
    -------
        file: an excel file stored in memory

    """
    output_xlsx_file = BytesIO()
    #writes the data frames to the excel sheet
    with pd.ExcelWriter(output_xlsx_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output_xlsx_file.seek(0)
    return output_xlsx_file

def detect_encoding(file):
    """Detect a files encoding.

    Args:
    ----
        file: Any file

    Returns:
    -------
        string: name of file encoding

    """
    # note, this expects a streamlit uploaded file stored in memory (or similar situation)
    # There is no need to open / close the file

    # Read file contents
    content = file.read()
    # Detect character encoding
    encoding = chardet.detect(content)["encoding"]
    file.seek(0,0) # move back to the beginning of the file (otherwise it appears empty)
    return encoding

def tabular_search(file_name, df, search_terms, search_options, sheet_name=""):
    """Search a data frame.

    Args:
    ----
        file_name (string): The name of the file the data frame was created from
        df: A data frame without a defined column header (e.g. the first column is `1`)
        search_terms (list): Keywords used in search
        search_options (dictionary): Configurations for search
        sheet_name (string, optional): Worksheet name if available. Defaults to "".

    Returns:
    -------
        list: search results

    """
    results = []
    columns = df.columns.tolist()

    # Loop through each row in the worksheet
    for index, row in df.iterrows():
        # Loop through each column in the worksheet
        for column in columns:
            # Find the cell using column and row
            cell = row[column]
            cell_value = str(cell).strip()
            # Skip empty cells
            if cell_value == "":
                continue
            # Collect search terms that matches cell value
            matched_terms_in_cell = []

            for term in search_terms:
                if match_function(cell_value, term, search_options):
                    matched_terms_in_cell.append(term)  # noqa: PERF401
            # Temporary solution for logging search results
            if len(matched_terms_in_cell):
                results.append(
                    build_result(
                        file_name=file_name,
                        location=f"{get_excel_column_letter(column)}{index + 1}",
                        search_terms=matched_terms_in_cell,
                        original_content=cell,
                        location_context=f"{sheet_name} ",
                    ),
                )
    return results

def document_search(file_name, line_list, search_terms, search_options, location_context):
    """Search a list of strings.

    Args:
    ----
        file_name (string): The name of the file the string list was created from
        line_list: A list of strings
        search_terms (list): Keywords used in search
        search_options (dictionary): Configurations for search
        location_context (string): Page number if available

    Returns:
    -------
        list: search results

    """
    results = []
    # Loop through each line in the document:
    for line_number, line in enumerate(line_list, start=1):
        matched_terms_in_line = []
        # check each search term:
        for term in search_terms:
            if match_function(line, term, search_options):
                matched_terms_in_line.append(term)  # noqa: PERF401
        # if one or more search term was found...
        if len(matched_terms_in_line):
            # ...add to the results
            results.append(
                build_result(
                    file_name=file_name,
                    location=f"Line {line_number} of {len(line_list)}",
                    search_terms=matched_terms_in_line,
                    original_content=line,
                    location_context=location_context,
                ),
            )
    return results


def build_result(file_name, location_context, location, search_terms, original_content):
    """Build search results.

    Args:
    ----
        file_name (string): The name of the file that was searched
        location_context (string): Page number or worksheet name if available
        location (string): The line number or column, row of the searched data
        search_terms (list): Keywords used in search that had a successful match
        original_content (string): The content of the cell or line that was searched.

    Returns:
    -------
        dictionary: the search result

    """
    return {
        "file": file_name,
        "location": f"{location_context} {location}",
        "search_terms": ", ".join(search_terms),
        "original_content": original_content,
        }

def strip_list(a_list) -> list:
    """Strip List.

    Args:
    ----
        a_list (list): a generic list of values.

    Returns:
    -------
        list: a list of strings.

    """
    return [str(s).strip() for s in a_list]

def search_term_file_to_list(search_term_file) -> list:
    """Search Term File to List.

    Args:
    ----
        search_term_file (file): an excel file with search terms in the first column.

    Returns:
    -------
        list: search terms as strings.

    """
    search_term_df = pd.read_excel(search_term_file, header=None)
    search_term_df = search_term_df.dropna()
    search_terms = search_term_df.iloc[:, 0].tolist()
    return strip_list(search_terms)

def get_excel_column_letter(col_num):
    """Get Excel Column Letter.

    Convert a column number (0-indexed) to an Excel-style column letter.
    (A, B, ..., Z, AA, AB, ...).
    """
    alphabet_length = 26
    if col_num < alphabet_length:
        return chr(col_num + ord("A"))
    div = col_num // alphabet_length
    mod = col_num % alphabet_length
    return get_excel_column_letter(div-1) + get_excel_column_letter(mod)

def match_function(content, term, mode):
    """Match Function.

    Summary:
    -------
    Part of the core functionality of multi-file search tool.
    This function is intended to be ran on every cell in an excel,
    or every line in a document.

    Args:
    ----
        content (string): a cell from a table or line from a document.
        term (string): a search term or regex pattern.
        mode (dictionary): configurations for match.

    Returns:
    -------
    Boolean: if the search term matched with the provided content.

    """
    modified_content = content
    modified_term = term
    if mode["mode"] == "regex":
        return bool(re.search(fr"{term}", content))
    if not mode["case-sensitive"]:
        modified_content = modified_content.lower()
        modified_term = modified_term.lower()
    if mode["whole-word"]:
        word_list = list(re.split(r"\W", modified_content))
        return modified_term in word_list
    return modified_term in modified_content
