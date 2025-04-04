from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.docx import search_docx

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.docx"

@patch(f"{base_path}.docx2txt.process")
def test_search_docx_exception_handling(mock_process_file):
    # Arrange
    file = MagicMock()
    file.name = "test_file.docx"
    search_terms = []
    search_options = {}
    # Act
    mock_process_file.side_effect = Exception("Error reading file")
    result = search_docx(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.docx",
        "location": "Error reading file"
    }]
    assert result == expected_result

@patch(f"{base_path}.docx2txt.process")
@patch(f"{base_path}.document_search")
def test_search_docx_calls_document_search(mock_document_search, mock_process):
    # Arrange
    file = MagicMock()
    file.name = "test_file.docx"
    search_terms = ['term1', 'term2']
    search_options = {"aardvark":"llama"}
    mock_process.return_value  = "Mock document contents for test."
    # Act
    search_docx(file, search_terms, search_options)
    # Assert
    mock_document_search.assert_called_with(
        file_name="test_file.docx",
        line_list=["Mock document contents for test."],
        search_terms=search_terms,
        search_options=search_options,
        location_context="",
    )
