"""Utils.

A collection of utilities for the Multi-File Search tool.
"""
import re
import os
from io import BytesIO
import concurrent.futures
import numpy as np

import chardet
import pandas as pd


# Global variables and helper functions for document search multiprocessing
_worker_doc_file_name = None
_worker_doc_location_context = None
_worker_doc_total_lines = None
_worker_doc_search_terms = None
_worker_doc_search_options = None

def init_document_worker(file_name, location_context, total_lines, search_terms, search_options):
    global _worker_doc_file_name, _worker_doc_location_context, _worker_doc_total_lines, _worker_doc_search_terms, _worker_doc_search_options
    _worker_doc_file_name = file_name
    _worker_doc_location_context = location_context
    _worker_doc_total_lines = total_lines
    _worker_doc_search_terms = search_terms
    _worker_doc_search_options = search_options

def process_document_chunk(chunk):
    chunk_results = []
    for line_number, line in chunk:
        matched_terms_in_line = []
        for term in _worker_doc_search_terms:
            if match_function(line, term, _worker_doc_search_options):
                matched_terms_in_line.append(term)
        if matched_terms_in_line:
            chunk_results.append({
                "file": _worker_doc_file_name,
                "location": f"{_worker_doc_location_context} Line {line_number} of {_worker_doc_total_lines}",
                "search_terms": ", ".join(matched_terms_in_line),
                "original_content": line,
            })
    return chunk_results


# Global variables and helper functions for tabular search multiprocessing
_worker_tabular_columns = None
_worker_tabular_file_name = None
_worker_tabular_sheet_name = None
_worker_tabular_search_terms = None
_worker_tabular_search_options = None

def init_tabular_worker(columns, file_name, sheet_name, search_terms, search_options):
    global _worker_tabular_columns, _worker_tabular_file_name, _worker_tabular_sheet_name, _worker_tabular_search_terms, _worker_tabular_search_options
    _worker_tabular_columns = columns
    _worker_tabular_file_name = file_name
    _worker_tabular_sheet_name = sheet_name
    _worker_tabular_search_terms = search_terms
    _worker_tabular_search_options = search_options

def process_tabular_chunk(chunk):
    chunk_results = []
    for index, row in chunk.iterrows():
        for column in _worker_tabular_columns:
            cell = row[column]
            cell_value = str(cell).strip()
            if cell_value == "":
                continue
            matched_terms_in_cell = []
            for term in _worker_tabular_search_terms:
                if match_function(cell_value, term, _worker_tabular_search_options):
                    matched_terms_in_cell.append(term)
            if matched_terms_in_cell:
                location = f"{get_excel_column_letter(column)}{index + 1}"
                chunk_results.append({
                    "file": _worker_tabular_file_name,
                    "location": f"{_worker_tabular_sheet_name} {location}",
                    "search_terms": ", ".join(matched_terms_in_cell),
                    "original_content": cell,
                })
    return chunk_results


def data_frame_to_excel(df):
    """Convert Data Frame to Excel."""
    output_xlsx_file = BytesIO()
    with pd.ExcelWriter(output_xlsx_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output_xlsx_file.seek(0)
    return output_xlsx_file

def detect_encoding(file):
    """Detect a files encoding."""
    content = file.read()
    encoding = chardet.detect(content)["encoding"]
    file.seek(0)
    return encoding

def tabular_search(file_name, df, search_terms, search_options, sheet_name=""):
    """Search a data frame using multiprocessing."""
    results = []
    columns = df.columns.tolist()
    num_processes = os.cpu_count() or 4
    
    if df.empty:
        return results
    
    chunks = np.array_split(df, num_processes)
    
    with concurrent.futures.ProcessPoolExecutor(
        initializer=init_tabular_worker,
        initargs=(columns, file_name, sheet_name, search_terms, search_options)
    ) as executor:
        chunk_futures = executor.map(process_tabular_chunk, chunks)
        for chunk_result in chunk_futures:
            results.extend(chunk_result)
    return results

def document_search(file_name, line_list, search_terms, search_options, location_context):
    """Search a list of strings using multiprocessing."""
    results = []
    total_lines = len(line_list)
    if not line_list:
        return results
    
    line_data = list(enumerate(line_list, start=1))
    num_processes = os.cpu_count() or 4
    chunk_size = (len(line_data) + num_processes - 1) // num_processes
    chunks = [line_data[i:i+chunk_size] for i in range(0, len(line_data), chunk_size)]
    
    with concurrent.futures.ProcessPoolExecutor(
        initializer=init_document_worker,
        initargs=(file_name, location_context, total_lines, search_terms, search_options)
    ) as executor:
        chunk_futures = executor.map(process_document_chunk, chunks)
        for chunk_result in chunk_futures:
            results.extend(chunk_result)
    return results

def build_result(file_name, location_context, location, search_terms, original_content):
    """Build search results."""
    return {
        "file": file_name,
        "location": f"{location_context} {location}",
        "search_terms": ", ".join(search_terms),
        "original_content": original_content,
    }

def strip_list(a_list) -> list:
    """Strip whitespace from list elements."""
    return [str(s).strip() for s in a_list]

def search_term_file_to_list(search_term_file) -> list:
    """Convert search term file to list."""
    search_term_df = pd.read_excel(search_term_file, header=None)
    search_term_df = search_term_df.dropna()
    search_terms = search_term_df.iloc[:, 0].tolist()
    return strip_list(search_terms)

def get_excel_column_letter(col_num):
    """Convert column number to Excel-style letter."""
    if col_num < 26:
        return chr(col_num + ord("A"))
    div = col_num // 26
    mod = col_num % 26
    return get_excel_column_letter(div-1) + get_excel_column_letter(mod)

def match_function(content, term, mode):
    """Core matching functionality."""
    modified_content = content
    modified_term = term
    if mode["mode"] == "regex":
        return bool(re.search(fr"{term}", content))
    if not mode["case-sensitive"]:
        modified_content = modified_content.lower()
        modified_term = modified_term.lower()
    if mode["whole-word"]:
        word_list = re.findall(r'\b\w+\b', modified_content)
        return modified_term in word_list
    return modified_term in modified_content