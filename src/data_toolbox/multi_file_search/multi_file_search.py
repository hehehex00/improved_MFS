"""..."""
import time
import concurrent.futures
import pandas as pd
import streamlit as st

from data_toolbox import components

from .file_router.router import router
from .user_interface.basic_search import basic_search
from .user_interface.components import step_component
from .user_interface.regex_search import regex_search
from .user_interface.search_term_file import search_term_file_search
from .utils.utils import data_frame_to_excel


def search(files, search_terms, search_mode):
    start_time = time.time()
    """Search Interface with Threading Support.

    Core Functionality for the application.
    Calls logic that processes and searches the uploaded files using threading.

    Args:
    ----
        files (list): User uploaded files
        search_terms (list): User entered or uploaded search terms (or regex patterns)
        search_mode (dictionary): Configurations for search

    """
    results = []
    progress_bar = st.progress(0, text=None)
    
    # Using ThreadPoolExecutor to handle threading with max 50 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Submit all files for processing
        futures = [executor.submit(router, file, search_terms, search_mode) for file in files]
        
        # Process results as they complete
        count = 0
        for future in concurrent.futures.as_completed(futures):
            search_results = future.result()
            if search_results:
                results.extend(search_results)
            count += 1
            progress_bar.progress(count / len(files))
    
    # Display Search Results
    results_df = pd.DataFrame(results)
    st.write(results_df)
    step_component("5. Download Search Results")
    
    # Create an excel file using the data frame
    output_xlsx_file = data_frame_to_excel(results_df)
    
    # Display Download Button
    st.download_button(
        label=":floppy_disk: Download Results",
        data=output_xlsx_file,
        type="primary",
        file_name="Multi_File_Search_Results.xlsx")
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    time.sleep(1)  # give the user the satisfaction of seeing a completed progress bar
    progress_bar.empty()  # clear the progress bar


# def search(files, search_terms, search_mode):
#     """Search Interface.

#     Core Functionality for the application.
#     Calls logic that processes and searches the uploaded files.

#     Args:
#     ----
#         files (list): User uploaded files
#         search_terms (list): User entered or uploaded search terms (or regex patterns)
#         search_mode (dictionary): Configurations for search

#     """
#     results = []
#     # Create a progress
#     progress_bar =st.progress(0, text=None)
#     # loop through each uploaded file
#     for count, file in enumerate(files, start=1):
#         print(file)
#         # Route correct search function:
#         search_results = router(file, search_terms, search_mode)
#         # Do stuff with the search results
#         if search_results:
#                 results.extend(search_results)
#         # Update the progress bar
#         progress_bar.progress(count / len(files))
#     # Display Search Results
#     results_df = pd.DataFrame(results)
#     st.write(results_df)
#     step_component("5. Download Search Results")
#     # Create an excel file using the data frame
#     output_xlsx_file = data_frame_to_excel(results_df)
#     # Display Download Button
#     st.download_button(
#         label= ":floppy_disk: Download Results",
#         data=output_xlsx_file,
#         type="primary",
#         file_name="Multi_File_Search_Results.xlsx")
#     time.sleep(1) # give the user the satisfaction of seeing a completed progress bar
#     progress_bar.empty() # clear the progress bar


def multi_file_search():
    """Multi-file Search.

    The main entrypoint for the multi-file search tool.
    """
    # H E A D E R:
    components.tool_header(
        title="Multi-File Search Version 2",
        uses="Ctrl+F through multiple files",
        nickname="Formally OreoScout and FileQuest",
        logo_path="./images/multi_file_search_logo.png",
        )
    # A B O U T :
    about_markdown_path="data_toolbox/multi_file_search/about.md"
    instructions_markdown_path="data_toolbox/multi_file_search/instructions.md"
    components.tool_about_section(
        about_markdown_path=about_markdown_path,
        instructions_markdown_path=instructions_markdown_path,
        )
    # T O O L:
    step_component("1. Select Search Options")
    search_mode = st.radio(
        label="Select search mode:",
        label_visibility="collapsed",
        options=["Basic", "Regex", "Upload Search Term File"],
        captions=[
            "Type in Search Terms",
            "Regular Expression search",
            "Use a prebuilt file with search terms",
            ],
        horizontal=True,
    )
    # Load UI Components for Search Modes:
    match search_mode:
        case "Basic":
            (uploaded_files, search_terms, search_options) = basic_search()
        case "Regex":
            (uploaded_files, search_terms, search_options) = regex_search()
        case "Upload Search Term File":
            (uploaded_files, search_terms, search_options) = search_term_file_search()
    # Run search:
    step_component("4. Select 'Search'")
    if st.button("**Search**", type="primary", key="script_runner"):
        search(uploaded_files, search_terms, search_options)

