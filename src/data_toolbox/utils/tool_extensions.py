from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tool_metadata import ToolMetadata


def supports_all_file_types(tool: ToolMetadata, file_extensions: set[str]) -> bool:
    """Check if the tool supports all file types based on the file_extensions.

    Parameters
    ----------
    tool : ToolMetadata
        The tool to check.
    file_extensions : set[str]
        The file extensions that the tool needs to support.

    Returns
    -------
    bool

    """
    supported_file_extensions: set[str] = \
        {file_type.lower() for file_type in tool.get_accepted_file_types_list()}

    if "any" in supported_file_extensions or "all" in supported_file_extensions:
        return True

    compatible_file_types = supported_file_extensions.intersection(file_extensions)
    return len(compatible_file_types) >= len(file_extensions)
