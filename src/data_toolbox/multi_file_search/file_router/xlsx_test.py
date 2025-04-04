from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.xlsx import search_xlsx

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.xlsx"

@patch(f"{base_path}.pd.read_excel")
def test_search_xlsx_exception_handling(mock_process_file):
    # Arrange
    file = MagicMock()
    file.name = "test_file.xlsx"
    search_terms = []
    search_options = {}
    # Act
    mock_process_file.side_effect = Exception("Error reading file")
    result = search_xlsx(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.xlsx",
        "location": "Error reading file"
    }]
    assert result == expected_result
