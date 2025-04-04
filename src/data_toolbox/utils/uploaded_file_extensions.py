from __future__ import annotations

from typing import TYPE_CHECKING

from data_toolbox.utils.files import determine_file_extension, human_readable_size_of

if TYPE_CHECKING:
    from streamlit.runtime.uploaded_file_manager import UploadedFile

import streamlit as st


def determine_file_extensions(uploaded_files: list[UploadedFile]) -> set[str]:
    """Determine the set of file extensions across all uploaded_files.

    Parameters
    ----------
    uploaded_files : list[UploadedFile]
        The list of uploaded files.

    Returns
    -------
    set[str]

    """
    return {determine_file_extension(uploaded_file.name)
            for uploaded_file in uploaded_files}


def file_upload_result_to_file_list(
        file_upload_result: UploadedFile | list[UploadedFile] | None,
) -> list[UploadedFile]:
    """Convert the result of a Streamlit file_upload to a list of UploadedFile objects.

    Parameters
    ----------
    file_upload_result : UploadedFile | list[UploadedFile] | None
        The result of a Streamlit file_upload widget

    Returns
    -------
    list[UploadedFile]

    """
    if file_upload_result is None:
        return []
    if not isinstance(file_upload_result, list):
        return [file_upload_result]
    return file_upload_result


default_file_upload_storage_key = "file_upload"


def store_uploaded_files_for_page_switch(
        file_upload_result: UploadedFile | list[UploadedFile] | None,
        key: str = default_file_upload_storage_key,
):
    """Store the result of a Streamlit file_upload widget for later retrieval.

    Combine this with restore_uploaded_files to share file uploads between pages.

    Parameters
    ----------
    file_upload_result : UploadedFile | list[UploadedFile] | None
        The result of a Streamlit file_upload widget
    key : str
        The key to use for storage. Ensure to use the same value for retrieval.

    Returns
    -------
    None

    """
    st.session_state[key] = file_upload_result


def restore_uploaded_files(
        key: str = default_file_upload_storage_key,
) -> UploadedFile | list[UploadedFile] | None:
    """Restore the result of a Streamlit file_upload widget stored earlier.

    This is designed to work in conjunction with store_uploaded_files_for_page_switch.
    You may want to use display_restored_uploaded_files to display the restored file data.

    Parameters
    ----------
    key : str
        The key to used for storage.

    Returns
    -------
    UploadedFile | list[UploadedFile] | None

    """
    try:
        return st.session_state[key]
    except KeyError:
        return None

def were_files_restored(restore_result: UploadedFile | list[UploadedFile] | None) -> bool:
    """Return True when at least one file is restored.

    Parameters
    ----------
    restore_result : UploadedFile | list[UploadedFile] | None
        The result of calling restore_uploaded_files

    Returns
    -------
    bool

    """
    return (restore_result is not None and
            (not isinstance(restore_result, list) or len(restore_result) >= 1))

def restore_first_uploaded_file(
        key: str = default_file_upload_storage_key,
) -> UploadedFile | None:
    """Restore the result of a Streamlit file_upload widget stored earlier.

    This is designed to work in conjunction with store_uploaded_files_for_page_switch.
    You may want to use display_restored_uploaded_files to display the restored file data.
    Only the first file is returned, when multiple files were stored.

    Parameters
    ----------
    key : str
        The key to used for storage.

    Returns
    -------
    UploadedFile | None

    """
    restored_files = restore_uploaded_files(key)
    if restored_files is None:
        return None
    if isinstance(restored_files, list):
        if len(restored_files) >= 1:
            return restored_files[0]
        return None
    return restored_files


def display_restored_uploaded_files(
        uploaded_files: UploadedFile | list[UploadedFile],
        label: str = "Uploaded files",
):
    """Display a list of uploaded_files restored from an upload on a different page.

    Parameters
    ----------
    uploaded_files : UploadedFile | list[UploadedFile]
        The file or files restored from an upload on a different page.
    label : str
        The label to display before the files.

    Returns
    -------
    None

    """
    def render_file(file: UploadedFile):
        return f"- {file.name} :grey[-- {human_readable_size_of(file.size)}]"

    header_markdown = [f"##### {label}"]

    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]
    files_markdown = [render_file(uploaded_file) for uploaded_file in uploaded_files]

    st.markdown("\n".join(header_markdown + files_markdown))
