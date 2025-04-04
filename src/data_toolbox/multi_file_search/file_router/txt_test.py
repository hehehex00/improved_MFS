from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.txt import search_txt

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.txt"

@patch(f"{base_path}.detect_encoding", Exception("Error reading file"))
def test_search_txt_exception_handling():
    # Arrange
    file = MagicMock()
    file.name = "test_file.txt"
    search_terms = []
    search_options = {}
    # Act
    result = search_txt(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.txt",
        "location": "Error reading file"
    }]
    assert result == expected_result
