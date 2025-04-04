# noqa: INP001 Don't want __init__.py in the top level for pytest
"""Metadata about all the tools in Data Toolbox."""

from __future__ import annotations

import json
import os

from config import styles_config
from data_toolbox.multi_file_search import multi_file_search
from data_toolbox.tag_manager.singletons import coordinator, manager

from tool_metadata import ToolMetadata

tool_categories = {
    "admin": "admin",  # admin tools are hidden by default
    "data_manipulation": "Data Manipulation",
    "translation_and_Media": "Translation & Media",
    "maps_and_geo_processing": "Maps & GEO Processing",
    "social_media_and_cryptocurrency": "Social Media & Cryptocurrency",
    "machine_learning_and_data_science": "Machine Learning & Data Science",
    "other": "Other",
}

VISIBILITY_CONFIG_PATH = "./config/visibility.config.json"
with open(VISIBILITY_CONFIG_PATH) as f:
    visibility_config = json.loads(f.read())
visibility_config = dict(sorted(visibility_config.items()))

styles = styles_config.load_styles_config()

tools = {
    "Multi File Search": ToolMetadata(
        "Multi File Search",
        multi_file_search,
        accepted_file_types=["xls", "xlsx", "csv", "docx", "pdf", "pptx", "txt"],
        uses=["Ctrl+F through multiple files"],
        category=tool_categories["data_manipulation"],
        image_path="./images/multi_file_search_logo.png",
        featured=True,
        visibility=visibility_config["Multi File Search"],
        tags=[
            manager.get_tag_by_id(tag_id).name
            for tag_id in coordinator.get_association("Multi File Search").tags
        ],
    )
}
# Filter out tools based on environment variables:
has_network_access = os.environ.get("HAS_INTERNET_ACCESS")
if has_network_access == "False":
    tools = {
        tool: metadata
        for tool, metadata in tools.items()
        if not metadata.get_requires_network_access()
    }

has_map_service = os.environ.get("HAS_MAP_SERVICE")
if has_map_service == "False":
    tools = {
        tool: metadata
        for tool, metadata in tools.items()
        if not metadata.get_requires_map_service()
    }

has_cached_model = os.environ.get("HAS_CACHED_MODEL")
if has_cached_model == "False":
    tools = {
        tool: metadata
        for tool, metadata in tools.items()
        if not metadata.get_requires_cached_model()
    }


def update_visibility_config(tool_metadata):
    """Persist changes to tool visibility in the config file."""
    visibility_config[tool_metadata.get_tool_name()] = tool_metadata.get_visibility()
    with open(VISIBILITY_CONFIG_PATH, "w") as f:  # noqa: PTH123
        json.dump(visibility_config, f, indent=2)


def get_tool(name):
    """Return the tools metadata class.

    Parameters
    ----------
    name : str
        The name of the tool you'd like the metadata for.

    Returns
    -------
    src.ToolMetadata
        The class containing the information about the tool.

    Examples
    --------
    >>> get_tool("Image_Triage")
    ToolMetadata(
        "Image Triage",
        image_triage,
        accepted_file_types=["ZIP"],
        uses=["Images, Triage"],
        category=tool_categories["machine_learning_and_data_science"],
        image_path="./images/data-team.png",
        nickname="Nickname",
        featured=False,
        visibility=visibility_config["Image Triage"],
        tags=[manager.get_tag_by_id(tag_id).name for tag_id in coordinator.get_association("Image Triage").tags],
    )

    """  # noqa: E501
    return tools[name]


def tool_list() -> list[ToolMetadata]:
    """Return a list of all the ToolMetadata that currently exist.

    Parameters
    ----------
    None

    Returns
    -------
    list[ToolMetadata]

    Examples
    --------
    >>> tool_list()
    [ToolMetadata(), ToolMetadata(), ...]

    """
    return list(tools.values())


def tool_dictionary():
    """Return the whole ToolMetadata dictionary.

    Parameters
    ----------
    None

    Returns
    -------
    dict{str : ToolMetadata}

    Examples
    --------
    >>> tool_dictionary()
    {
        "FirstTool" : ToolMetadata(),
        ...
    }

    """
    return tools


def tool_dictionary_categorized():
    """Return a nested dictionary with added categorization keys.

    Parameters
    ----------
    None

    Returns
    -------
    dict{
        str : dict{
            str : ToolMetadata,
            ...
        },
        ...
    }

    Examples
    --------
    >>> tool_dictionary_categorized()
    {
        "Category1" : {
            "Tool1" : ToolMetadata,
            ...
        }
    }

    """
    tools_categorized = {}
    for category in tool_categories.values():
        tools_categorized[category] = []
        for tool in tool_list():
            if tool.category == category:
                tools_categorized[category].append(tool)
    return tools_categorized
