"""Utils for Streamlit Analytics."""

import datetime
import errno
import json
import logging
import os
import time
from pathlib import Path

LOGGER = logging.getLogger("Toolbox")

def format_seconds(s: int) -> str:
    """Format seconds to 00:00:00 format."""
    hours, remainder = divmod(s, 3600)
    mins, secs = divmod(remainder, 60)

    hours = int(hours)
    mins = int(mins)
    secs = int(secs)

    return f"{hours:02}:{mins:02}:{secs:02}"


def replace_empty(s):
    """Replace an empty string or None with a space."""
    if s == "" or s is None:
        return " "
    return s

def get_time():
    """Linter compliant date function util."""
    return datetime.datetime.now(tz=datetime.timezone.utc)

def clear_error_log(container_counts, tool_name: str):
    """Clear Error Log."""
    container_counts[tool_name]["error_log"] = {}
    return container_counts

def collate_results(counts, load_from_json, lock, verbose=False):
    """Load counts from a json file or directory of json files.

    Args:
    ----
        load_from_json (Union[str, Path]): str or Path to json file or directory files.
        verbose (bool): Print whether loading counts was successful or not.
        counts: Dictionary to store the loaded count data
        lock: Lock object for thread safety

    Raises:
    ------
        FileNotFoundError: If json file or directory of json files is not found.
        OSError: If file is locked and cannot be opened.

    """
    try:
        if Path.is_dir(Path(load_from_json)):
            # reinit using main file first.
            with Path(load_from_json+"datatoolbox_analytics.json").open("r") as f:
                json_counts = json.load(f)
                for key in json_counts:
                    counts[key]=json_counts[key]
            for file in os.listdir(load_from_json):
                # We skip the compiled log to avoid infinitely increasing values.
                skip_files = {"combined_analytics.json", "datatoolbox_analytics.json"}
                if file in skip_files:
                    if verbose:
                        LOGGER.info("Skipping Master File.")
                    continue
                if load_from_json is not None and file is not None and not Path.is_dir(Path(file)) and file.endswith(".json"):  # noqa: E501
                    if verbose:
                        LOGGER.info(("Loading counts from json:", load_from_json+file))
                    with lock:  # noqa: SIM117
                        with Path(load_from_json+file).open("r") as f:
                            json_counts = json.load(f)
                            for key in json_counts:
                                counts[key]=json_counts[key]
        if verbose:
            LOGGER.info("Success! Loaded counts:")
            LOGGER.info(counts)
    except FileNotFoundError:
        if verbose:
            LOGGER.exception("File not found, proceeding with empty counts.")
    except OSError as e:
        # File is locked, wait and try again
        LOGGER.exception("OS Error:") # Removed redundant exception object
        if e.errno == errno.EBUSY:
            time.sleep(1)
            collate_results(counts, load_from_json, verbose)
    return counts
