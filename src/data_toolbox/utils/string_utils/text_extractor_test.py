"""Tests for the TextExtractor Class."""
from pathlib import Path

from .text_extractor import TextExtractor


def test_methods_exist():
    """Test to check if all necessary methods exist in the TextExtractor class."""
    assert hasattr(TextExtractor(), "extract_html")
    assert hasattr(TextExtractor(), "extract_pdf")
    assert hasattr(TextExtractor(), "extract_txt")
    assert hasattr(TextExtractor(), "text_cleanup")
    assert hasattr(TextExtractor(), "text_extractor_ui")


def test_extract_docx():
    """Test for successful `docx` text extraction."""
    # Create an instance of text_extractor
    text_extractor = TextExtractor()
    # the test file
    file_path = Path("data_toolbox/utils/string_utils/test_data/test.docx")
    # Use the extract_docx method to extract text from the test.docx file
    with Path.open(file_path, "rb") as file:
        extracted_text = text_extractor.extract_docx(file)
    # Check if the extracted text is not empty
    assert extracted_text is not None
    assert "Waldo Was Here." in extracted_text


def test_extract_html():
    """Test for successful `html` text extraction."""
    # Create an instance of text_extractor
    text_extractor = TextExtractor()
    # the test file
    file_path = Path("data_toolbox/utils/string_utils/test_data/test.html")
    # Use the extract_html method to extract text from the test.html file
    with Path.open(file_path, "rb") as file:
        extracted_text = text_extractor.extract_html(file)
    # Check if the extracted text is not empty
    assert extracted_text is not None
    assert "Waldo Was Here." in extracted_text
    # It automatically formats text
    assert "Waldo Was Here. See It Cleans Up Text!" in extracted_text


def test_extract_html_disables_cleanup():
    """Tests for default text cleanup behavior"""
    # Create an instance of text_extractor
    text_extractor = TextExtractor()
    # the test file
    file_path = Path("data_toolbox/utils/string_utils/test_data/test.html")
    # Use the extract_html method to extract text from the test.html file
    with Path.open(file_path, "rb") as file:
        extracted_text_not_cleaned = text_extractor.extract_html(file, cleanup=False)
    # Check if the extracted text is not empty
    assert extracted_text_not_cleaned is not None
    assert "Waldo Was Here.SeeItCleansUpText!" in extracted_text_not_cleaned


def test_extract_pdf():
    """Test for successful `pdf` text extraction."""
    # Create an instance of text_extractor
    text_extractor = TextExtractor()
    # the test file
    file_path = Path("data_toolbox/utils/string_utils/test_data/test.pdf")
    # Use the extract_pdf method to extract text from the test.pdf file
    with Path.open(file_path, "rb") as file:
        extracted_text = text_extractor.extract_pdf(file)
    # Check if the extracted text is not empty
    assert extracted_text is not None
    assert "Waldo Was Here." in extracted_text


def test_text_cleanup():
    """Test Text Cleanup adds spaces after capitalized words."""
    text_extractor = TextExtractor()
    input_text = "HelloWorld.ThisIsATest"
    expected_output = "Hello World. This Is A Test"
    cleaned_text = text_extractor.text_cleanup(input_text)
    assert cleaned_text == expected_output


def test_text_cleanup_multiple_spaces():
    """Test Text Cleanup handles multiple spaces."""
    text_extractor = TextExtractor()
    input_text = "Hello     World"
    expected_output = "Hello World"
    cleaned_text = text_extractor.text_cleanup(input_text)
    assert cleaned_text == expected_output


def test_text_cleanup_special_characters():
    """Test Text Cleanup handles special characters."""
    text_extractor = TextExtractor()
    input_text = "PythonIsAwesome!Don'tYouThink?"
    expected_output = "Python Is Awesome! Don't You Think?"
    cleaned_text = text_extractor.text_cleanup(input_text)
    assert cleaned_text == expected_output
