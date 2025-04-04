"""Main API functions for the user to start and stop analytics tracking."""

from __future__ import annotations

import datetime
import errno
import functools
import json
import logging
import os
import time
import traceback
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Union

import streamlit as st

from config import styles_config

from . import display, firestore
from .utils import clear_error_log, collate_results, get_time, replace_empty

# Configure logging
LOGGER = logging.getLogger("Toolbox")

# Conditional import for main streamlit container.
try:
    from tool_dictionary import tool_list
except ModuleNotFoundError:
    LOGGER.info("We are in a container, tool_dictionary not needed.")

# Store original streamlit functions. They will be monkey-patched with some wrappers
# in `start_tracking` (see wrapper functions below).
_orig_button = st.button
_orig_checkbox = st.checkbox
_orig_radio = st.radio
_orig_selectbox = st.selectbox
_orig_multiselect = st.multiselect
_orig_slider = st.slider
_orig_select_slider = st.select_slider
_orig_text_input = st.text_input
_orig_number_input = st.number_input
_orig_text_area = st.text_area
_orig_date_input = st.date_input
_orig_time_input = st.time_input
_orig_file_uploader = st.file_uploader
_orig_color_picker = st.color_picker

_orig_sidebar_button = st.sidebar.button
_orig_sidebar_checkbox = st.sidebar.checkbox
_orig_sidebar_radio = st.sidebar.radio
_orig_sidebar_selectbox = st.sidebar.selectbox
_orig_sidebar_multiselect = st.sidebar.multiselect
_orig_sidebar_slider = st.sidebar.slider
_orig_sidebar_select_slider = st.sidebar.select_slider
_orig_sidebar_text_input = st.sidebar.text_input
_orig_sidebar_number_input = st.sidebar.number_input
_orig_sidebar_text_area = st.sidebar.text_area
_orig_sidebar_date_input = st.sidebar.date_input
_orig_sidebar_time_input = st.sidebar.time_input
_orig_sidebar_file_uploader = st.sidebar.file_uploader
_orig_sidebar_color_picker = st.sidebar.color_picker

lock = Lock()

CORE_KEYS = {
    "total_pageviews",
    "total_script_runs",
    "total_time_seconds",
}

# Dict that holds all analytics results. Note that this is persistent across users,
# as modules are only imported once by a streamlit app.
counts = {"loaded_from_firestore": False, "loaded_from_file": False}

# For Reset Count purposes, Home Page is the best to initialize on.
current_page = "Home Page"

# Dict that holds this specific container's analytics results.
container_counts = {"loaded_from_firestore": False, "loaded_from_file": False}

# Utility that loops through main container's tools to init a new day
def start_day():
    """Initialize new day for all tools in container."""
    today = str(get_time().date())
    # We need to track the new day across all tools
    all_tools = tool_list()
    for tool in all_tools:
        _new_day(tool.get_tool_name(), today)
    # Init core pages that don't have meta-data.
    _new_day("Home Page", today)
    _new_day("Tool Wizard", today)
    _new_day("Feedback", today)
    _new_day("Tool Select", today)
    _new_day("Featured Tools", today)
    _new_day("Analytics", today)
    _new_day("None", today)
    container_counts["per_day"]["days"].append(today)
    container_counts["per_day"]["pageviews"].append(0)
    container_counts["per_day"]["script_runs"].append(0)
    container_counts["per_day"]["errors"].append(0)

def _new_day(tool_name: str, today: str):
    # Update tools date tracking with today's date.
    if tool_name not in container_counts:
        container_counts[tool_name] = {"Tool Name": tool_name }
        _init_tool_tracking(tool_name)
    container_counts[tool_name]["per_day"]["days"].append(today)
    container_counts[tool_name]["per_day"]["pageviews"].append(0)
    container_counts[tool_name]["per_day"]["script_runs"].append(0)
    container_counts[tool_name]["per_day"]["errors"].append(0)

def _init_tool_tracking(tool_name: str):
    LOGGER.info("Initializing Tracking for: %s", tool_name)
    yesterday = str(get_time().date() - datetime.timedelta(days=1))
    container_counts[tool_name]["total_pageviews"] = 0
    container_counts[tool_name]["total_script_runs"] = 0
    container_counts[tool_name]["total_time_seconds"] = 0
    container_counts[tool_name]["per_day"] = {"days": [str(yesterday)],
                                               "pageviews": [0],
                                               "script_runs": [0],
                                               "errors": [0]}
    container_counts[tool_name]["widgets"] = {
        "checkbox": {},
        "button": {},
        "file_uploader": {},
        "select": {},
        "multiselect": {},
        "value": {},
    }
    container_counts[tool_name]["error_log"] = {}
    container_counts[tool_name]["start_time"] = get_time().strftime("%d %b %Y, %H:%M:%S")  # noqa: E501

def reset_counts():
    """Reset counts."""
    # Use yesterday as first entry to make chart look better.
    yesterday = str(get_time().date() - datetime.timedelta(days=1))
    container_counts["total_pageviews"] = 0
    container_counts["total_script_runs"] = 0
    container_counts["total_time_seconds"] = 0
    container_counts["per_day"] = {"days": [str(yesterday)],
                                    "pageviews": [0], "script_runs": [0],
                                    "errors": [0]}
    container_counts["start_time"] = get_time().strftime("%d %b %Y, %H:%M:%S")  # noqa: E501
    counts["total_pageviews"] = 0
    counts["total_script_runs"] = 0
    counts["total_time_seconds"] = 0
    counts["per_day"] = {"days": [str(yesterday)], "pageviews": [0],
                          "script_runs": [0], "errors": [0]}
    counts["start_time"] = get_time().strftime("%d %b %Y, %H:%M:%S")  # noqa: E501

def _track_user():
    """Track individual pageviews by storing user id to session state."""
    global current_page # noqa: PLW0603
    if current_page is None:
        current_page = "None"
    # If we don't have a current_page, we likely just started the app. Init to Home.
    try:
        current_page = st.session_state["current_page"]
    except KeyError:
        LOGGER.exception("Page not tracking! Here is the session state: %s", st.session_state)
    if current_page is None:
        current_page = "None"
    container_counts[current_page]["total_script_runs"] += 1
    container_counts["total_script_runs"] += 1
    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
    container_counts["per_day"]["script_runs"][-1] += 1
    now = get_time()
    container_counts[current_page]["total_time_seconds"] += (
        (now - st.session_state.last_time).total_seconds()
    )
    st.session_state.last_time = now
    if not st.session_state.user_tracked:
        st.session_state.user_tracked = True
        container_counts["total_pageviews"] += 1
        container_counts[current_page]["total_pageviews"] += 1
        container_counts["per_day"]["pageviews"][-1] += 1
        container_counts[current_page]["per_day"]["pageviews"][-1] += 1
def _wrap_error_handler(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # noqa: BLE001
            # Not all widgets have a key, catch the error if it doesn't exist.
            container_counts[current_page]["per_day"]["errors"][-1] += 1

    return inner

def _wrap_checkbox(func):
    """Wrap st.checkbox."""
    def new_func(label, *args, **kwargs):
        checked = func(label, *args, **kwargs)
        label = replace_empty(label)
        key = kwargs.get("key")
        # Initialize the container if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"checkbox": {}},
                                              "per_day": {"script_runs": []}}
        if label not in container_counts[current_page]["widgets"]["checkbox"]:
            container_counts[current_page]["widgets"]["checkbox"][label] = 0
        if checked != st.session_state.state_dict.get(label, None):
            container_counts[current_page]["widgets"]["checkbox"][label] += 1
            try:
                if "script_runner" in key:
                    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                    container_counts["per_day"]["script_runs"][-1] += 1
            except Exception:  # noqa: BLE001, S110
                # Not all widgets have a key, catch the error if it doesn't exist.
                pass
        st.session_state.state_dict[label] = checked
        return checked

    return new_func
def _wrap_button(func):
    """Wrap st.button."""

    def new_func(label, *args, **kwargs):
        clicked = func(label, *args, **kwargs)
        label = replace_empty(label)
        key = kwargs.get("key")

        # Initialize container_counts for the current page if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"button": {}}}

        # Initialize the 'button' section if it doesn't exist
        if "button" not in container_counts[current_page]["widgets"]:
            container_counts[current_page]["widgets"]["button"] = {}

        # Initialize the specific button label if it doesn't exist
        if label not in container_counts[current_page]["widgets"]["button"]:
            container_counts[current_page]["widgets"]["button"][label] = 0

        if clicked:
            container_counts[current_page]["widgets"]["button"][label] += 1
            try:
                if "script_runner" in key:
                    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                    container_counts["per_day"]["script_runs"][-1] += 1
            except Exception:  # noqa: BLE001, S110
                # Not all widgets have a key, catch the error if it doesn't exist.
                pass
        st.session_state.state_dict[label] = clicked
        return clicked

    return new_func

def _wrap_file_uploader(func):
    """Wrap st.file_uploader."""

    def new_func(label, *args, **kwargs):
        uploaded_file = func(label, *args, **kwargs)
        label = replace_empty(label)
        key = kwargs.get("key")

        # Initialize the container if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"file_uploader": {}},
                                              "per_day": {"script_runs": []}}

        # Initialize the file_uploader label if it doesn't exist
        if "file_uploader" not in container_counts[current_page]["widgets"]:
            container_counts[current_page]["widgets"]["file_uploader"] = {}

        if label not in container_counts[current_page]["widgets"]["file_uploader"]:
            container_counts[current_page]["widgets"]["file_uploader"][label] = 0

        if uploaded_file and not st.session_state.state_dict.get(label, None):
            container_counts[current_page]["widgets"]["file_uploader"][label] += 1
            try:
                if "script_runner" in key:
                    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                    container_counts["per_day"]["script_runs"][-1] += 1
            except Exception:  # noqa: BLE001, S110
                # Not all widgets have a key, catch the error if it doesn't exist.
                pass

        if "state_dict" not in st.session_state:
            st.session_state.state_dict = {}
        st.session_state.state_dict[label] = bool(uploaded_file)
        return uploaded_file

    return new_func

def _wrap_select(func):
    """Wrap Select.

    Wrap a streamlit function that returns one selected element out of multiple options,
    e.g. st.radio, st.selectbox, st.select_slider.
    """

    def new_func(label, options, *args, **kwargs):
        orig_selected = func(label, options, *args, **kwargs)
        label = replace_empty(label)
        selected = replace_empty(orig_selected)
        key = kwargs.get("key")
        # Initialize the container if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"select": {}},
                                              "per_day": {"script_runs": []}}
        if label not in container_counts[current_page]["widgets"]["select"]:
            container_counts[current_page]["widgets"]["select"][label] = {}
        for option in options:
            option = replace_empty(option)  # noqa: PLW2901
            if option not in container_counts[current_page]["widgets"]["select"][label]:
                container_counts[current_page]["widgets"]["select"][label][option] = 0
            if option not in container_counts[current_page]["widgets"]["select"][label]:
                container_counts[current_page]["widgets"]["select"][label][option] = 0
        if selected != st.session_state.state_dict.get(label, replace_empty(None)):
            container_counts[current_page]["widgets"]["select"][label][selected] += 1
            try:
                if "script_runner" in key:
                    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                    container_counts["per_day"]["script_runs"][-1] += 1
            except Exception:  # noqa: BLE001, S110
                # Not all widgets have a key, catch the error if it doesn't exist.
                pass
        st.session_state.state_dict[label] = selected
        return orig_selected

    return new_func


def _wrap_multiselect(func):
    """Wrap multiselect.

    Wrap a streamlit function that returns multiple selected elements out of multiple
    options, e.g. st.multiselect.
    """

    def new_func(label, options, *args, **kwargs):
        selected = func(label, options, *args, **kwargs)
        label = replace_empty(label)
        key = kwargs.get("key")
        # Initialize the container if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"multiselect": {}},
                                              "per_day": {"script_runs": []}}
        if label not in container_counts[current_page]["widgets"]["multiselect"]:
            container_counts[current_page]["widgets"]["multiselect"][label] = {}
        for option in options:
            option = str(replace_empty(option))  # noqa: PLW2901
            if option not in container_counts[current_page][
                "widgets"]["multiselect"][label]:
                container_counts[current_page]["widgets"][
                    "multiselect"][label][option] = 0
            if option not in container_counts[current_page][
                "widgets"]["multiselect"][label]:
                container_counts[current_page]["widgets"][
                    "multiselect"][label][option] = 0
        for sel in selected:
            sel = str(replace_empty(sel))  # noqa: PLW2901
            if sel not in st.session_state.state_dict.get(label, []):
                container_counts[current_page]["widgets"]["multiselect"][label][sel] += 1  # noqa: E501
                try:
                    if "script_runner" in key:
                        container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                        container_counts["per_day"]["script_runs"][-1] += 1
                except Exception:  # noqa: BLE001, S110
                    # Not all widgets have a key, catch the error if it doesn't exist.
                    pass
        st.session_state.state_dict[label] = selected
        return selected

    return new_func


def _wrap_value(func):
    """Wrap Value.

    Wrap a streamlit function that returns a single value (str/int/float/datetime/...),
    e.g. st.slider, st.text_input, st.number_input, st.text_area, st.date_input,
    st.time_input, st.color_picker.
    """

    def new_func(label, *args, **kwargs):
        value = func(label, *args, **kwargs)
        # Initialize the container if it doesn't exist
        if current_page not in container_counts:
            container_counts[current_page] = {"widgets": {"value": {}},
                                              "per_day": {"script_runs": []}}
        if label not in container_counts[current_page]["widgets"]["value"]:
            container_counts[current_page]["widgets"]["value"][label] = {}
        key = kwargs.get("key")
        formatted_value = replace_empty(value)
        if isinstance(value, tuple) and len(value) == 2:  # noqa: PLR2004
            # Double-ended slider or date input with start/end, convert to str.
            formatted_value = f"{value[0]} - {value[1]}"

        # st.date_input and st.time return datetime object, convert to str
        if (isinstance(value, (datetime.datetime, datetime.date, datetime.time))):
            formatted_value = str(value)

        if formatted_value not in container_counts[current_page][
            "widgets"]["value"][label]:
            container_counts[current_page]["widgets"][
                "value"][label][formatted_value] = 0
        if formatted_value not in container_counts[current_page][
            "widgets"]["value"][label]:
            container_counts[current_page]["widgets"][
                "value"][label][formatted_value] = 0
        if formatted_value != st.session_state.state_dict.get(label, None):
            container_counts[current_page]["widgets"][
                "value"][label][formatted_value] += 1
            try:
                if "script_runner" in key:
                    container_counts[current_page]["per_day"]["script_runs"][-1] += 1
                    container_counts["per_day"]["script_runs"][-1] += 1
            except Exception:  # noqa: BLE001, S110
                # Not all widgets have a key, catch the error if it doesn't exist.
                pass
        st.session_state.state_dict[label] = formatted_value
        return value

    return new_func

def load_counts(load_from_json, verbose):
    """Load counts from a json file or directory of json files.

    Args:
    ----
        load_from_json (Union[str, Path]): str or Path to json file or directory files.
        verbose (bool): Print whether loading counts was successful or not.

    Raises:
    ------
        FileNotFoundError: If json file or directory of json files is not found.
        OSError: If file is locked and cannot be opened.

    """
    global lock  # noqa: PLW0602
    try:
        if Path.is_dir(Path(load_from_json)):
            for file in os.listdir(load_from_json):
                # If given directory this is our main app.
                if file == ("datatoolbox_analytics.json" and (
                    load_from_json is not None) and file is not None and not Path.is_dir(Path(file)) and file.endswith(".json")):  # noqa: E501
                    LOGGER.info(("Loading counts from json:", load_from_json+file))
                    with lock:  # noqa: SIM117
                        with Path(load_from_json+file).open("r") as f:
                            json_counts = json.load(f)
                            for key in json_counts:
                                container_counts[key] = json_counts[key]
        else:
            if verbose:
                LOGGER.info("No Directory given, falling back to local.")
            with lock:  # noqa: SIM117
                with Path(load_from_json).open("r") as f:
                    json_counts = json.load(f)
                    if load_from_json is not None:
                        if verbose:
                            LOGGER.info(("Loading counts from json:", load_from_json))
                        for key in json_counts:
                            container_counts[key] = json_counts[key]
        if verbose:
            LOGGER.info("Success! Loaded counts:")
            LOGGER.info(container_counts)
    except FileNotFoundError:
        if verbose:
            LOGGER.exception("File not found, proceeding with empty counts.")
    except OSError as e:
        # File is locked, wait and try again
        LOGGER.exception("OS Error")
        if e.errno == errno.EBUSY:
            time.sleep(1)
            load_counts(load_from_json, verbose)

def start_tracking(  # noqa: C901, PLR0915
    verbose: bool = True,  # noqa: FBT001, FBT002
    firestore_key_file: str = None,
    firestore_collection_name: str = "container_counts",
    load_from_json: Union[str, Path] = None,  # noqa: FA100, UP007
):
    """Start tracking user inputs to a streamlit app.

    If you call this function directly, you NEED to call
    `streamlit_analytics.stop_tracking()` at the end of your streamlit script.
    For a more convenient interface, wrap your streamlit calls in
    `with streamlit_analytics.track():`.
    """
    if firestore_key_file and not container_counts["loaded_from_firestore"]:
        firestore.load(container_counts, firestore_key_file, firestore_collection_name)
        container_counts["loaded_from_firestore"] = True
    if firestore_key_file and not container_counts["loaded_from_firestore"]:
        firestore.load(container_counts, firestore_key_file, firestore_collection_name)
        container_counts["loaded_from_firestore"] = True
        if verbose:
            LOGGER.info("Loaded count data from firestore:")
            LOGGER.info(container_counts)

    if load_from_json is not None and not container_counts["loaded_from_file"]:
        try:
            if Path.is_dir(Path(load_from_json)):
                if len(os.listdir(load_from_json)) == 0:
                    if verbose:
                        LOGGER.info("No existing analytics files found, proceeding with empty counts.")
                    reset_counts()
                for file in os.listdir(load_from_json):
                    # If given directory this is our main app.
                    if file == "datatoolbox_analytics.json" and (
                        load_from_json is not None) and file is not None:
                        if verbose:
                            LOGGER.info(("Loading counts from json:", load_from_json+file))
                        with Path(load_from_json+file).open("r") as f:
                            json_counts = json.load(f)
                            for key in json_counts:
                                container_counts[key] = json_counts[key]
            else:
                if verbose:
                    LOGGER.info("No Directory given, falling back to local.")
                with Path(load_from_json).open("r") as f:
                    json_counts = json.load(f)
                    if load_from_json is not None:
                        if verbose:
                            LOGGER.info(("Loading counts from json:", load_from_json))
                        for key in json_counts:
                            container_counts[key] = json_counts[key]
            container_counts["loaded_from_file"] = True
            if verbose:
                LOGGER.info("Success! Loaded counts:")
                LOGGER.info(container_counts)
        except FileNotFoundError:
            if verbose:
                LOGGER.exception("File not found, proceeding with empty counts.")
            reset_counts()
    # Reset session state.
    if "user_tracked" not in st.session_state:
        st.session_state.user_tracked = False
    if "state_dic" not in st.session_state:
        st.session_state.state_dict = {}
    if "last_time" not in st.session_state:
        st.session_state.last_time = get_time()

    # We should update tracking each day for all tools.
    today = str(get_time().date())
    # If we are looking at a directory we are the main Toolbox container
    if Path.is_dir(Path(load_from_json)):
        # If the container isn't tracking today, none of its tools are.
        if container_counts["per_day"]["days"][-1] != today:
            start_day()
    # Otherwise our app is containerized and we need to reverse engineer the tool_name
    else:
        global current_page # noqa: PLW0603
        try:
            current_page = st.session_state["current_page"]
        except KeyError:
            LOGGER.exception(("Page not tracking! Here is the session state: ", st.session_state))
        # If the container isn't tracking today, none of its tools are.
        if container_counts["per_day"]["days"][-1] != today:
            # Append to container days.
            container_counts["per_day"]["days"].append(today)
            container_counts["per_day"]["pageviews"].append(0)
            container_counts["per_day"]["script_runs"].append(0)
            container_counts["per_day"]["errors"].append(0)
            # Append to tool days.
            _new_day(current_page, today)
    try:
        _track_user()
    except KeyError:
        if verbose:
            LOGGER.exception("%(page)s not tracked due to error: ", {"page": current_page})
    # Monkey-patch streamlit to call the wrappers above.
    st.button = _wrap_button(_orig_button)
    st.checkbox = _wrap_checkbox(_orig_checkbox)
    st.radio = _wrap_select(_orig_radio)
    st.selectbox = _wrap_select(_orig_selectbox)
    st.multiselect = _wrap_multiselect(_orig_multiselect)
    st.slider = _wrap_value(_orig_slider)
    st.select_slider = _wrap_select(_orig_select_slider)
    st.text_input = _wrap_value(_orig_text_input)
    st.number_input = _wrap_value(_orig_number_input)
    st.text_area = _wrap_value(_orig_text_area)
    st.date_input = _wrap_value(_orig_date_input)
    st.time_input = _wrap_value(_orig_time_input)
    st.file_uploader = _wrap_file_uploader(_orig_file_uploader)
    st.color_picker = _wrap_value(_orig_color_picker)

    st.sidebar.button = _wrap_button(_orig_sidebar_button)
    st.sidebar.checkbox = _wrap_checkbox(_orig_sidebar_checkbox)
    st.sidebar.radio = _wrap_select(_orig_sidebar_radio)
    st.sidebar.selectbox = _wrap_select(_orig_sidebar_selectbox)
    st.sidebar.multiselect = _wrap_multiselect(_orig_sidebar_multiselect)
    st.sidebar.slider = _wrap_value(_orig_sidebar_slider)
    st.sidebar.select_slider = _wrap_select(_orig_sidebar_select_slider)
    st.sidebar.text_input = _wrap_value(_orig_sidebar_text_input)
    st.sidebar.number_input = _wrap_value(_orig_sidebar_number_input)
    st.sidebar.text_area = _wrap_value(_orig_sidebar_text_area)
    st.sidebar.date_input = _wrap_value(_orig_sidebar_date_input)
    st.sidebar.time_input = _wrap_value(_orig_sidebar_time_input)
    st.sidebar.file_uploader = _wrap_file_uploader(_orig_sidebar_file_uploader)
    st.sidebar.color_picker = _wrap_value(_orig_sidebar_color_picker)

    if verbose:
        LOGGER.info("Tracking script execution with streamlit-analytics...")

def write_analytics(save_to_json, verbose):
    """Write analytics results to a json file.

    If `save_to_json` is a directory, it will compile all json files in the
    directory into a single json file named `combined_analytics.json`.

    If `save_to_json` is not a directory, it will simply write the counts to
    the file specified by `save_to_json`.

    Args:
    ----
        save_to_json (Union[str, Path]): The directory or file to write to.
        verbose (bool): If True, print debugging information.

    Returns:
    -------
        None

    """
    global lock  # noqa: PLW0603 PLW0602
    global counts  # noqa: PLW0603 PLW0602
    # Compile count from all files if reading directory.
    try:
        if Path.is_dir(Path(save_to_json)):
            counts = collate_results(counts, save_to_json, lock)
            # Write to Master File
            with lock:  # noqa: SIM117
                with Path(save_to_json+"combined_analytics.json").open("w") as f:
                    json.dump(counts, f)
                    if verbose:
                        LOGGER.info(("Results being saved: ", counts))
                        LOGGER.info(("Storing results to file:",
                                save_to_json+"combined_analytics.json"))
            # Write to Personal File
            with lock:  # noqa: SIM117
                with Path(save_to_json+"datatoolbox_analytics.json").open("w") as f:
                    json.dump(container_counts, f)
                    if verbose:
                        LOGGER.info(("Storing personal results to file:",
                                save_to_json, "datatoolbox_analytics.json"))
        else:
            # We only care about counts if compiling a directory.
            with lock:
                with Path(save_to_json).open("w") as f:
                    json.dump(container_counts, f)
                if verbose:
                    LOGGER.info(("Storing results to file:", save_to_json))
    except FileNotFoundError:
        if verbose:
            LOGGER.exception("File not found, proceeding with empty counts.")
    except OSError as e:
        # File is locked, wait and try again
        LOGGER.info("OS Error: file locked, retrying...")
        if e.errno == errno.EBUSY:
            time.sleep(1)
            write_analytics(save_to_json, verbose)

def stop_tracking(
    unsafe_password: str = None,
    save_to_json: Union[str, Path] = None,  # noqa: FA100, UP007
    firestore_key_file: str = None,
    firestore_collection_name: str = "counts",
    verbose: bool = False,  # noqa: FBT001, FBT002
):
    """Stop tracking user inputs to a streamlit app.

    Should be called after `streamlit-analytics.start_tracking()`.
    This method also shows the analytics results below your app if you attach
    `?tool=User+Analytics` to the URL.
    """
    # Initialize tracking with container_counts
    counts = deepcopy(container_counts)


    if verbose:
        LOGGER.info("Finished script execution. New counts:")
        LOGGER.info(counts)
        LOGGER.info("-" * 80)

    # Reset streamlit functions.
    st.button = _orig_button
    st.checkbox = _orig_checkbox
    st.radio = _orig_radio
    st.selectbox = _orig_selectbox
    st.multiselect = _orig_multiselect
    st.slider = _orig_slider
    st.select_slider = _orig_select_slider
    st.text_input = _orig_text_input
    st.number_input = _orig_number_input
    st.text_area = _orig_text_area
    st.date_input = _orig_date_input
    st.time_input = _orig_time_input
    st.file_uploader = _orig_file_uploader
    st.color_picker = _orig_color_picker

    st.sidebar.button = _orig_sidebar_button
    st.sidebar.checkbox = _orig_sidebar_checkbox
    st.sidebar.radio = _orig_sidebar_radio
    st.sidebar.selectbox = _orig_sidebar_selectbox
    st.sidebar.multiselect = _orig_sidebar_multiselect
    st.sidebar.slider = _orig_sidebar_slider
    st.sidebar.select_slider = _orig_sidebar_select_slider
    st.sidebar.text_input = _orig_sidebar_text_input
    st.sidebar.number_input = _orig_sidebar_number_input
    st.sidebar.text_area = _orig_sidebar_text_area
    st.sidebar.date_input = _orig_sidebar_date_input
    st.sidebar.time_input = _orig_sidebar_time_input
    st.sidebar.file_uploader = _orig_sidebar_file_uploader
    st.sidebar.color_picker = _orig_sidebar_color_picker

    # Save count data to firestore.
    if firestore_key_file:
        if verbose:
            LOGGER.info("Saving count data to firestore:")
            LOGGER.info(counts)
        firestore.save(counts, firestore_key_file, firestore_collection_name)

    if save_to_json is not None:
        write_analytics(save_to_json, verbose)

    # Show analytics results in the streamlit app:
    query_params = st.query_params
    if "tool" in query_params and "User Analytics" in query_params["tool"]:
        display.show_results(counts, reset_counts, clear_error_log, unsafe_password, save_to_json, lock)

@contextmanager
def track(  # noqa: PLR0913
    unsafe_password: str = None,
    save_to_json: Union[str, Path] = None,  # noqa: UP007
    firestore_key_file: str = None,
    firestore_collection_name: str = "counts",
    verbose=False,  # noqa: FBT002
    load_from_json: Union[str, Path] = None,  # noqa: UP007
):
    """Context manager to start and stop tracking user inputs to a streamlit app.

    To use this, wrap all calls to streamlit in `with streamlit_analytics.track():`.
    This also shows the analytics results below your app if you attach
    `tool=User Analytics` to the URL.
    """
    start_tracking(
        verbose=verbose,
        firestore_key_file=firestore_key_file,
        firestore_collection_name=firestore_collection_name,
        load_from_json=load_from_json,
    )

    # Yield here to execute the code in the with statement. This will call the wrappers
    # above, which track all inputs.
    try:
        yield

    except Exception as e:  # noqa: BLE001
        try:
            global current_page # noqa: PLW0603
            if current_page is None:
                current_page = "None"
        except Exception:  # noqa: BLE001
            current_page = "None"
        if verbose:
            LOGGER.exception((f"Encountered an exception at {current_page}: ", e.__traceback__.tb_lineno))  # noqa: E501
            LOGGER.exception((f"Encountered an exception at {current_page}: ", traceback.format_exc()))
        if current_page is None:
            current_page = "None"
        container_counts[current_page]["per_day"]["errors"][-1] += 1
        container_counts["per_day"]["errors"][-1] += 1
        now = str(get_time())
        container_counts[current_page]["error_log"].__setitem__(now, e.__str__())

        styles = styles_config.load_styles_config()
        if styles["Panda Mode"]:
            st.error(f"Error: {e} - {traceback.format_exc()}", icon="🐼")
        else:
            st.error(f"Error: {e} - {traceback.format_exc()}")

    finally:
        stop_tracking(
            unsafe_password=unsafe_password,
            save_to_json=save_to_json,
            firestore_key_file=firestore_key_file,
            firestore_collection_name=firestore_collection_name,
            verbose=verbose,
        )
