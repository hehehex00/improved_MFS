from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.pptx import search_pptx

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.pptx"

@patch(f"{base_path}.Presentation")
def test_search_pptx_exception_handling(mock_process_file):
    # Arrange
    file = MagicMock()
    file.name = "test_file.pptx"
    search_terms = []
    search_options = {}
    # Act
    mock_process_file.side_effect = Exception("Error reading file")
    result = search_pptx(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.pptx",
        "location": "Error reading file"
    }]
    assert result == expected_result
