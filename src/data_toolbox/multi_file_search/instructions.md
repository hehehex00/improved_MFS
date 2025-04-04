# How Multi-File Search works

This tool searches all uploaded files for input search terms using three different
search options. The tool then returns a table with the search results.

## Basic Search

This type of search takes input search terms and outputs what file, the location,
and original context where each search term was found.

**Steps:**

1. Select search option
2. Upload files to be searched. Acceptable file formats are DOCX, PDF, PPTX, TXT,
XLS, XLSX, and CSV
3. Type in a word, phrase, or selector and press `enter` to add each search term
4. Select "Case Sensitive" and/or "Whole Word" option to apply to search
5. Click "Download Results" to download the results as a XLSX file

## Regex Search

This type of search takes input regular expression(s) and outputs what file, the location,
and original context where each regex was found. This is useful when searching for patterns
of text and not exact strings.

**Steps:**

1. Select search option
2. Upload files to be searched. Acceptable file formats are DOCX, PDF, PPTX, TXT,
XLS, XLSX, and CSV
3. Type in a regular expression and press `enter` to add each search term. A regular
expression (often shortened to regex or occasionally referred to as rational
expression) is a sequence of characters that specifies a match pattern in text.
Regular expressions are powerful because they can match groups of characters.
For example  `\d+` will return all numbers `0` to `9`.
4. Click "Download Results" to download the results as a XLSX file

## Upload Search Term File

This type of search takes an input file of keywords or selectors outputs what file, the location,
and original context where each keyword or selector term was found.

**Steps:**

1. Select search option
2. Upload files to be searched. Acceptable file formats are DOCX, PDF, PPTX, TXT,
XLS, XLSX, and CSV
3. Upload file with list of keywords or selectors to search
4. Click "Download Results" to download the results as a XLSX file

**Tool Limitations:**

- This tool can not read text on images in PDFs
- Searches can handle non-latin characters,
but will only search for the exact characters entered in.
This can impact languages with flexible spelling rules and/or
large regional variations of spelling such as Arabic
