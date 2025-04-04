from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.pdf import search_pdf

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.pdf"

@patch(f"{base_path}.pypdf.PdfReader")
def test_search_pdf_exception_handling(mock_process_file):
    # Arrange
    file = MagicMock()
    file.name = "test_file.pdf"
    search_terms = []
    search_options = {}
    # Act
    mock_process_file.side_effect = Exception("Error reading file")
    result = search_pdf(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.pdf",
        "location": "Error reading file"
    }]
    assert result == expected_result
