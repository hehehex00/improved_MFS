# ruff: noqa: D102

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import streamlit as st

from data_toolbox.utils import display_restored_uploaded_files, restore_uploaded_files
from data_toolbox.utils.uploaded_file_extensions import (
    restore_first_uploaded_file,
    were_files_restored,
)

if TYPE_CHECKING:
    from io import BytesIO

    from streamlit.runtime.uploaded_file_manager import UploadedFile  #extends io.BytesIO


class ToolInterface:
    """Abstract Class for creating a streamlit tool.

    Every tool must implement certain basics.

    Attributes:
    ----------
    tool_name: str
        name of the tool, also used in the tool dictionary
    uploaded_files: List[UploadedFile] | None
        files uploaded from streamlit in the specific Streamlit wrapper
    output_file_name:
        the file that parallel processing would output the results into
    accepted_file_types:
        suffixes that would be accepted by the tool, based on the naming of the file

    Methods
    -------
    ingest()
        Optional, used for any pre-processing necessary
    execute()
        Execute the streamlit tool
    process()
        The meat and potatoes that actually processes the input
    download_file
        A generically implemented streamlit file download method. Override as necessary
    streamlit_upload_files
        A generically implemented streamlit file upload method. Override as necessary

    """

    def __init__(
            self,
            tool_name: str,
            accepted_file_types: list[str],
            output_file_name:str="results",
            **kwargs,  # noqa: ARG002
        ):
        """Initialize a streamlit tool allowing future customization."""
        self.tool_name = tool_name
        self.uploaded_files = None
        self.output_file_name = output_file_name
        self.accepted_file_types = accepted_file_types


    @abstractmethod
    def ingest(self, files: list[UploadedFile], **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def process(self, **kwargs:Any):
        raise NotImplementedError

    @abstractmethod
    def execute(self, **kwargs:Any):
        """Execute Streamlit specific steps to run through the box."""
        raise NotImplementedError

    def download_file(
            self,
            output_file:BytesIO,
            output_file_name:str,
            label="Download Results",
        ) -> None:
        st.download_button(
            label= label,
            data=output_file,
            file_name=output_file_name,
        )

    def streamlit_upload_files(
            self,
            label:str="Upload",
            multi_file:bool=True,  # noqa: FBT001, COM812, FBT002
            script_runner:bool=False,
        ) -> list[UploadedFile] | None:
        """Streamlit File Uploader.

        Convenience method for managing streamlit file uploads.

        Parameters
        ----------
        label : str, optional
            The text to display for the upload button, by default "Upload"
        multi_file : bool, optional
            Whether to allow users to upload multiple files, by default True
        script_runner : bool, optional
            Whether to use a separate key for the file uploader, by default False

        Returns
        -------
        list[UploadedFile] | None
            A list of uploaded files or None if no files were uploaded.

        """
        if multi_file:
            uploaded_files = restore_uploaded_files()
        else:
            uploaded_files = restore_first_uploaded_file()
        key = "script_runner" if script_runner else None

        if were_files_restored(uploaded_files):
            display_restored_uploaded_files(uploaded_files)
            return uploaded_files
        return st.file_uploader(
            label=label,
            type=self.accepted_file_types,
            accept_multiple_files=multi_file,
            key=key,
        )
