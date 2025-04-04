from unittest.mock import MagicMock, patch
from data_toolbox.multi_file_search.file_router.csv import search_csv

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.csv"

@patch(f"{base_path}.detect_encoding")
def test_search_csv_exception_handling(mock_detect_encoding):
    # Arrange
    file = MagicMock()
    file.name = "test_file.csv"
    search_terms = []
    search_options = {}
    # Act
    mock_detect_encoding.side_effect = Exception("Error reading file")
    result = search_csv(file, search_terms, search_options)
    # Assert
    expected_result = [{
        "file": "test_file.csv",
        "location": "Error reading file"
    }]
    assert result == expected_result

@patch(f"{base_path}.pd.read_csv")
@patch(f"{base_path}.detect_encoding")
@patch(f"{base_path}.tabular_search")
def test_search_csv_calls_tabular_search(mock_tabular_search, mock_detect_encoding, mock_read_csv):
    # Arrange
    file = MagicMock()
    file.name = "test_file.csv"
    search_terms = ['term1', 'term2']
    search_options = {"aardvark":"llama"}
    mock_detect_encoding.return_value  = "mock_encoding"
    mock_read_csv.return_value  = "mock_csv_data_frame"
    # Act
    search_csv(file, search_terms, search_options)
    # Assert
    mock_tabular_search.assert_called_with(
        file_name="test_file.csv",
        df="mock_csv_data_frame",
        search_terms=search_terms,
        search_options=search_options,
        sheet_name="",
    )
