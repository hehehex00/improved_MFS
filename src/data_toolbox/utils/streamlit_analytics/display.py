"""Displays the analytics results within streamlit."""

import logging
from threading import Lock

import altair as alt
import pandas as pd
import streamlit as st

from . import utils

tool_breakdowns = {}
LOGGER = logging.getLogger("Toolbox")

def authenticated(password) -> bool:
    """If a password is set then it asks the user for that password.

    Very quick, dirty, and unsafe way of doing this.
    """
    # If the admin panel does not have a password set just return true
    if password is None:
        return True

    password_input = st.text_input("Enter password to show results", type="password")

    # For the streamlit loop, if the user hasn't typed anything in yet return false
    if not password_input:
        return False

    if password_input == password:
        return True

    # We'll find you
    st.write("Password not correct you are being reported, dont run ☝️")
    return False

def refresh_analytics(current_counts, load_from_json, lock):
    """Refresh analytics display."""
    # Loop through all files again and recompile our counts.
    counts = utils.collate_results(current_counts, load_from_json, lock=lock)
    return counts

def find_longest_history(counts):
    """Normalize analytics array lengths for display."""
    cur_max_history = 0
    cur_max_history_array = []
    for tool in counts:
        try:
            if "per_day" in counts[tool]:
                cur_tool_history = len(counts[tool]["per_day"]["days"])
                if cur_tool_history > cur_max_history:
                    cur_max_history = cur_tool_history
                    cur_max_history_array = counts[tool]["per_day"]["days"]
        except KeyError:  # noqa: PERF203
            LOGGER.exception("Invalid analytics data at %s", tool)
            continue
        except TypeError:
            LOGGER.exception("Skipping non-relevant analytics data at %s", tool)
            continue
    return cur_max_history_array, cur_max_history

def extend_array(max_history_len, max_history_arr, tool_counts):
    """Normalize array sizes for graph display, filling 0s in for missing dates."""
    diff = max_history_len - len(tool_counts["per_day"]["script_runs"])
    block = [0]*diff
    tool_counts["per_day"]["errors"].extend(block)
    tool_counts["per_day"]["script_runs"].extend(block)
    tool_counts["per_day"]["days"] = max_history_arr
    tool_counts["per_day"]["errors"] = tool_counts["per_day"]["errors"]
    tool_counts["per_day"]["script_runs"] = tool_counts["per_day"]["script_runs"]
    return tool_counts

def extract_and_format_counts(counts):
    """Format raw analytics data to prep it for display."""
    # init indexes
    indexes = ["Global"]
    # init selectbox options
    selectbox_options = []
    # init dataframes

    cur_max_history_array, cur_max_history = find_longest_history(counts)

    if cur_max_history > len(counts["per_day"]["script_runs"]):
        counts = extend_array(cur_max_history, cur_max_history_array, counts)

    execution_data = {
        "Date": set(counts["per_day"]["days"]),
        "Global": counts["per_day"]["script_runs"],
    }
    error_data = {
        "Date": set(counts["per_day"]["days"]),
        "Global": counts["per_day"]["errors"],
    }

    # loop through data and extract relevant pieces.
    for tool in counts:
        try:
            if "per_day" in counts[tool]:
                cur_tool_history = len(counts[tool]["per_day"]["days"])
                # If this tool hasn't been tracked for full up-time fill with 0s so we can still display it.
                if cur_tool_history < cur_max_history:
                    counts[tool] = extend_array(cur_max_history, cur_max_history_array, counts[tool])
                # Data for Tool Usage Graph
                execution_data[tool] = counts[tool]["per_day"]["script_runs"]
                # Data for Errors Graph
                error_data[tool] = counts[tool]["per_day"]["errors"]
                # Attach Execution Data to Dates
                execution_data["Date"].update(counts[tool]["per_day"]["days"])
                # Attach Error Data to Dates
                error_data["Date"].update(counts[tool]["per_day"]["days"])
                # Update Legend with Tool Name for Graph Labelling
                indexes.append(tool)
                # Update Selectbox with Tool Name for Graph Filtering
                selectbox_options.append(tool)

        except KeyError:  # noqa: PERF203
            LOGGER.exception("Invalid analytics data at %s", tool)
            continue
        except TypeError:
            LOGGER.exception("Skipping non-relevant analytics data at %s", tool)
            continue
    return execution_data, error_data, indexes, selectbox_options

def show_results(current_counts, reset_callback, error_log_callback, unsafe_password=None, load_from_json=None):
    """Show analytics results in streamlit, asking for password if given."""
    # Track Current Page
    st.session_state["current_page"] = "Analytics"
    # Show header.
    st.title("Analytics Dashboard")

    # Create lock instance inside function rather than as default arg
    lock = Lock()

    # If the passwords dont match then dont show the dashboard
    if not authenticated(unsafe_password):
        return

    # Refresh Analytics immediately upon loading.
    counts = refresh_analytics(current_counts, load_from_json, lock=lock)

    # Show traffic.
    st.header("Traffic")
    st.write(f"since {counts['start_time']}")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Pageviews",
        counts["total_pageviews"],
        counts["total_pageviews"],
        help="Every time a user (re-)loads the site.",
    )
    col2.metric(
        "Script runs",
        counts["total_script_runs"],
        help="Every time Streamlit reruns upon changes or interactions.",
    )
    col3.metric(
        "Time spent",
        utils.format_seconds(counts["total_time_seconds"]),
        help="Time from initial page load to last widget interaction, summed over all users.",  # noqa: E501
    )
    st.write("")

    # Format raw analytics
    execution_data, error_data, indexes, selectbox_options = extract_and_format_counts(counts)

    # Order set into list so we can use it in our chart.
    execution_data["Date"] = sorted(execution_data["Date"])
    error_data["Date"] = sorted(error_data["Date"])

    # Input Dropdown to select individual tools to view
    input_dropdown = alt.binding_select(options=indexes+[None],
                                            labels=indexes+["All"], name="Tools")

    # Create a filter to allow us to select individual tools to view.
    selection = alt.selection_point(fields=["Tool Name"], bind=input_dropdown)

    # Convert our execution data into a dataframe for graphical display
    try:
        analytics_df = pd.DataFrame(execution_data)
        error_df = pd.DataFrame(error_data)

        # Convert dataframe into a Altair Chart compatible dataframe.
        execution_long_form = analytics_df.melt("Date", var_name="Tool Name",
                                        value_name="Script Runs")
        error_long_form = error_df.melt("Date", var_name="Tool Name",
                                        value_name="Errors")
        # Surface the Altair Chart for Tool Usage
        st.header("Tool Usage Metrics")
        st.altair_chart((alt.Chart(execution_long_form).mark_line().encode(
                            x="Date:T",
                            y="Script Runs:Q",
                            # Set the Colors and scale based on selected indexes
                            color=alt.Color("Tool Name:N").scale(domain=indexes))
                            .add_params(selection)
                            .transform_filter(selection)
                        ),
                        use_container_width=True)
        # Surface the Altair Chart for Tool Errors
        st.header("Error Tracking")
        st.altair_chart((alt.Chart(error_long_form).mark_line().encode(
                            x="Date:T",
                            y="Errors:Q",
                            # Set the Colors and scale based on selected indexes
                            color=alt.Color("Tool Name:N").scale(domain=indexes))
                            .add_params(selection)
                            .transform_filter(selection)
                        ),
                        use_container_width=True)
    except ValueError:
        LOGGER.exception("Dataframes not uniform, unable to display data. Please contact Data Team.")
        print(execution_data)
    st.divider()

    # Show widget interactions.
    st.header("Tool Specific Metrics")

    option = st.selectbox("Tool Selection", selectbox_options)

    st.subheader(f"Raw Analytics for {option}")
    with st.expander(f"Full {option} Analytics"):
        st.write(counts[option])

    st.subheader(f"Raw Error Log for {option}")
    with st.expander("Error Log"):
        st.write(counts[option]["error_log"])
        reset_clicked = st.button(f":red[**Click here to clear Error Log for {option}**]")  # noqa: E501
        if reset_clicked:
            counts = error_log_callback(counts, option)
            st.write("Done! Please refresh the page.")

    # Show button to reset analytics.
    st.header(":red[Danger zone]")
    with st.expander(":red[Here be dragons] 🐲🔥"):
        st.write(
            """
            Here you can reset all analytics results.

            **This will erase everything tracked so far.**  \n
            You will **not** be able to retrieve it.  \n
            This will also overwrite any results synced to Firestore.
            """,
        )
        reset_prompt = st.selectbox(
            "Continue?",
            [
                "No idea what I'm doing here",
                "I'm absolutely sure that I want to reset the results",
            ],
        )
        if reset_prompt == "I'm absolutely sure that I want to reset the results":
            reset_clicked = st.button(":red[**Click here to reset**]")
            if reset_clicked:
                reset_callback()
                st.write("Done! Please refresh the page.")
