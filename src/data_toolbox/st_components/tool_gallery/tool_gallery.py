from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from data_toolbox.st_components.tool_preview import tool_preview

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

    from tool_metadata import ToolMetadata


def tool_gallery(tools: list[ToolMetadata], width: int = 3):
    """Display a gallery of tool previews.

    Each row displays up to width elements.

    Parameters
    ----------
    tools : list[ToolMetadata]
        The metadata of the tools to display.
    width : int, optional
        The maximum amount of elements per row.

    Returns
    -------
    None

    """
    columns: list[DeltaGenerator] = []

    for index, tool in enumerate(tools):
        if index % width == 0:
            columns = st.columns(width, gap="large")

        with columns[index % width]:
            tool_preview(tool)
