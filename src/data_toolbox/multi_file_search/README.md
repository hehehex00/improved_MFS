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
