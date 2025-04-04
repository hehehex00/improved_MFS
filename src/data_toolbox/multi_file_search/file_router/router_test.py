from unittest.mock import patch
from data_toolbox.multi_file_search.file_router.router import router

# Base path for mocking functions called in router
base_path = "data_toolbox.multi_file_search.file_router.router"

class mock_file:
    def __init__(self, name):
        self.name = name

@patch(f'{base_path}.search_csv')
def test_router_csv_called(mock_search_csv):
    file = mock_file("test.csv")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_csv.assert_called_once()

@patch(f'{base_path}.search_xls')
def test_router_xls_called(mock_search_xls):
    file = mock_file("test.xls")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_xls.assert_called_once()

@patch(f'{base_path}.search_xlsx')
def test_router_xlsx_called(mock_search_xlsx):
    file = mock_file("test.xlsx")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_xlsx.assert_called_once()

@patch(f'{base_path}.search_docx')
def test_router_docx_called(mock_search_docx):
    file = mock_file("test.docx")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_docx.assert_called_once()

@patch(f'{base_path}.search_pdf')
def test_router_pdf_called(mock_search_pdf):
    file = mock_file("test.pdf")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_pdf.assert_called_once()

@patch(f'{base_path}.search_pptx')
def test_router_pptx_called(mock_search_pptx):
    file = mock_file("test.pptx")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_pptx.assert_called_once()

@patch(f'{base_path}.search_txt')
def test_router_txt_called(mock_search_txt):
    file = mock_file("test.txt")
    search_terms = ['term1', 'term2']
    search_options = {'case_sensitive': True}
    router(file, search_terms, search_options)
    mock_search_txt.assert_called_once()
