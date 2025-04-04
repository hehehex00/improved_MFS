# How Multi-File Search works

This tool searches all uploaded files for input search terms using three different
search options. The tool then returns a table with the search results.

## Frequently Asked Questions

### Does this tool connect to the internet

**No.** This tool does _not_ connect to the internet.

### Can this read text on images in PDFs

**No.** Multi File search tool does not have OCR capability.

### Can this search for keywords with non-latin characters

***Yes, mostly.** It can handle non-latin characters,
but will only search for the exact characters entered in.
This can impact languages with flexible spelling rules and/or
large regional variations of spelling such as Arabic.

### What is the use case for Upload Search Term File option

If the user has a list of keywords for which they constantly search,
the user can put the words into an excel document with each keyword in its own cell.
This will save the user from constantly searching.

### What is a 'regular expression'

A regular expression (often shortened to regex or occasionally referred to as rational
expression) is a sequence of characters that specifies a match pattern in text.
Regular expressions are powerful because they can match groups of characters.
For example  `\d+` will return all numbers `0` to `9`.
This is useful if you are searching for patterns of text and not exact strings.

### Additional Notes
1. Document Search Utilities
Purpose: Search through text documents line-by-line using multiprocessing.
Key Components
    •	Global Variables: Store search parameters (_worker_doc_*) for multiprocessing workers
    •	init_document_worker(): Initializes worker processes with search parameters
    •	process_document_chunk():
        o	Processes chunks of lines (with line numbers)
        o	Checks each line against all search terms using match_function()
        o	Collects matches with file metadata and location info

2. Tabular Search Utilities
Purpose: Search through spreadsheet data (Excel/CSV) using multiprocessing.
Key Components:
    •	Global Variables: Store spreadsheet parameters (_worker_tabular_*)
    •	init_tabular_worker(): Initializes spreadsheet search workers
    •	process_tabular_chunk():
        o	Processes DataFrame chunks
        o	Checks specified columns in each row
        o	Converts cell locations to Excel-style coordinates (A1 notation)
        o	Uses match_function() for cell content checks

3. Core Matching Function
match_function():
    •	Supports multiple search modes:
        o	Regex matching (mode["mode"] == "regex")
        o	Case-insensitive search
        o	Whole-word matching
    •	Handles content/term normalization for case sensitivity

4. Multiprocessing Management
Common Patterns:
    1.	Data chunking:
        o	Documents: Split lines into equal chunks
        o	Spreadsheets: Split DataFrames with np.array_split()
    2.	Process pool setup:
            Python:
            with concurrent.futures.ProcessPoolExecutor(...) as executor:
                executor.map(...)
    3.	Result aggregation from parallel workers

5. Support Functions
    •	data_frame_to_excel(): Converts DataFrame to Excel file in memory
    •	detect_encoding(): Auto-detects file encoding using chardet
    •	get_excel_column_letter(): Converts numeric column index to Excel letters (e.g., 0 → A)
    •	search_term_file_to_list(): Loads search terms from Excel file
    •	strip_list(): Cleans whitespace from list elements

6. Main Search Entry Points
    1.	document_search():
        o	Takes list of lines + search parameters
        o	Distributes work across processes
        o	Returns list of match dictionaries
    2.	tabular_search():
        o	Takes DataFrame + search parameters
        o	Handles spreadsheet-specific metadata
        o	Returns cell-level matches

