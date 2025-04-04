"""Test suite for Multi File Search utils."""
from io import BytesIO

import pandas as pd

from data_toolbox.multi_file_search.utils.utils import (
    build_result,
    data_frame_to_excel,
    detect_encoding,
    document_search,
    get_excel_column_letter,
    match_function,
    search_term_file_to_list,
    strip_list,
    tabular_search,
)


def test_data_frame_to_excel():
    """Test data frame to excel conversion.

    This test is basically a util for an excel to DataFrame conversion. 🤷‍♂️
    """
    # Create a sample DataFrame
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["a", "b", "c"],
    })
    # Call the function and get the output Excel file
    output_xlsx_file = data_frame_to_excel(df)
    # Read the Excel file back into a DataFrame
    df_from_excel = pd.read_excel(output_xlsx_file)
    # Check if the original DataFrame and the DataFrame read from Excel are equal
    assert df.equals(df_from_excel)


def test_utf8_encoding():
    # "欢迎" in utf-8 encoding
    file_content = b"\xe6\xad\xa1\xe8\xbf\x8e"
    file = BytesIO(file_content)
    result = detect_encoding(file)
    assert result == "utf-8"


def test_big5_encoding():
    # "中國信託產險" in big5 encoding
    file_content = b"\xa4\xe5\xa4\xa4\xa4\xf3\xa4\xb8\xa4\xf1\xa5L\xad\x9b\xc4\xcf"
    file = BytesIO(file_content)
    result = detect_encoding(file)
    assert result == "Big5"

def test_tabular_search():
    # Setup
    file_name = "test.xlsx"
    sheet_name = "sheet1" # location context
    # Excel files and CSVs are read in without column headers:
    df = pd.DataFrame([
        ["Pineapple", "Mango", "Cranberry"],
        ["What's up Dog?", "Cat", "Elephant"],
    ])
    search_terms = ["Cranberry", "Dog", "Up"]
    search_options={
        "mode": "regular",
        "case-sensitive": False,
        "whole-word": False,
    }
    # Expected results
    expected_results = [
        {
            "file": file_name,
            "location": "sheet1  C1",
            "search_terms": "Cranberry",
            "original_content": "Cranberry",
        },
        {
            "file": file_name,
            "location": "sheet1  A2",
            "search_terms": "Dog, Up",
            "original_content": "What's up Dog?",
        },
    ]
    # Execution
    search_results = tabular_search(file_name, df, search_terms, search_options, sheet_name)
    # Assertion
    assert len(search_results) == 2
    assert search_results == expected_results

def test_document_search():
    file_name = "test_doc.txt"
    line_list = [
        "This is a test document.",
        "Containing some search terms and context.",
        "For unit testing purposes."
        ]
    search_terms = ["test", "search"]
    search_options={
        "mode": "regular",
        "case-sensitive": False,
        "whole-word": False,
    }
    expected_results = [
        {
            "file": file_name,
            "location": " Line 1 of 3",
            "search_terms": "test",
            "original_content": "This is a test document.",
        },
        {
            "file": file_name,
            "location": " Line 2 of 3",
            "search_terms": "search",
            "original_content": "Containing some search terms and context.",
        },
        {
            "file": file_name,
            "location": " Line 3 of 3",
            "search_terms": "test",
            "original_content": "For unit testing purposes.",
        }
    ]
    search_results = document_search(
        file_name,
        line_list,
        search_terms,
        search_options,
        location_context=""
        )
    assert len(search_results) == 3
    assert search_results == expected_results

def test_build_result():
    # Arrange
    file_name = "test.pptx"
    location_context = "Page 3"
    location = "Line 10"
    search_terms = ["apple", "orange"]
    original_content = "This is a test file for unit testing"
    # Act
    result = build_result(file_name, location_context, location, search_terms, original_content)
    # Assert
    assert result["file"] == "test.pptx"
    assert result["location"] == "Page 3 Line 10"
    assert result["search_terms"] == "apple, orange"
    assert result["original_content"] == "This is a test file for unit testing"


def test_strip_list_empty():
    result = strip_list([])
    assert result == []

def test_strip_list_with_strings():
    input_list = ["  hello ", "   world   ", " 123 "]
    result = strip_list(input_list)
    expected = ["hello", "world", "123"]
    assert result == expected

def test_strip_list_with_integers():
    input_list = [1, 2, 3]
    result = strip_list(input_list)
    expected = ["1", "2", "3"]
    assert result == expected

def test_strip_list_with_mixed_values():
    input_list = [1, "  hello ", 3.5, "   world   "]
    result = strip_list(input_list)
    expected = ["1", "hello", "3.5", "world"]
    assert result == expected

def test_search_term_file_to_list():
    # Create a one column
    rows = ["snake", 700, " checkmate "]
    df = pd.DataFrame({
        "column_header": rows, # only the first column is extracted.
        "another_colum": ["1", "Fox", "Undergrowth"] # these will be ignored
    })
    temp_excel_file = data_frame_to_excel(df) # this test assumes this works
    # call the function with the temporary file
    result = search_term_file_to_list(temp_excel_file)
    # assert that the result contains the correct search terms
    assert result == ["column_header", "snake", "700", "checkmate"]

def test_get_excel_column_letter():
    assert get_excel_column_letter(0) == "A"
    assert get_excel_column_letter(1) == "B"
    assert get_excel_column_letter(25) == "Z"
    assert get_excel_column_letter(26) == "AA"
    assert get_excel_column_letter(27) == "AB"
    assert get_excel_column_letter(701) == "ZZ"
    assert get_excel_column_letter(702) == "AAA"
    assert get_excel_column_letter(703) == "AAB"
    assert get_excel_column_letter(18277) == "ZZZ"

def test_match_function_simple_search():
    content = "Hello, World! This is a test string."
    mode = {"mode": "simple", "case-sensitive": True, "whole-word": False}
    assert match_function(content=content, term="World", mode=mode) == True
    assert match_function(content=content, term="WORLD", mode=mode) == False
    assert match_function(content=content, term="d! T", mode=mode) == True

def test_match_function_case_insensitive_search():
    content = "Hello, World! This is a test string."
    mode = {"mode": "simple", "case-sensitive": False, "whole-word": False}
    assert match_function(content=content, term="World", mode=mode) == True
    assert match_function(content=content, term="WORLD", mode=mode) == True
    assert match_function(content=content, term="world", mode=mode) == True
    assert match_function(content=content, term=" world! t", mode=mode) == True

def test_match_function_whole_word_search():
    content = "Hello, World! This is a test string."
    mode = {"mode": "simple", "case-sensitive": False, "whole-word": True}
    assert match_function(content=content, term="hello", mode=mode) == True
    assert match_function(content=content, term="hell", mode=mode) == False
    # will fail if search term is multi-word
    assert match_function(content=content, term="World! This", mode=mode) == False

def test_match_function_whole_word_case_sensitive_search():
    content = "Hello, World! This is a test string."
    mode = {"mode": "simple", "case-sensitive": True, "whole-word": True}
    assert match_function(content=content, term="Hello", mode=mode) == True
    assert match_function(content=content, term="HELLO", mode=mode) == False
    assert match_function(content=content, term="Hell", mode=mode) == False
    # will fail if search term is multi-word
    assert match_function(content=content, term="World! This", mode=mode) == False

def test_match_function_regex_search():
    content = "Hello, World! This is a test string."
    term = r"^[a-zA-Z]+,"
    mode = {"mode": "regex", "case-sensitive": False, "whole-word": False}
    assert match_function(content=content, term=term, mode=mode) == True
    content = "10,9,8,7,6,5,4,3,2,1..."
    assert match_function(content=content, term=term, mode=mode) == False
