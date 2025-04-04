"""A Streamlit download button that doesn't reset the page when you click it.

Modified from https://gist.github.com/chad-m/6be98ed6cf1c4f17d09b7f6e5ca2978f
"""
import base64
import csv
import json
import pickle
import re
import uuid

import pandas as pd
import streamlit as st


def download_button(object_to_download, download_filename,
                     button_text, pickle_it=False, button_css=None):  # noqa: FBT002
    """Generate a link to download the given object_to_download.

    Args:
    ----
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download link.
    button_text (str): Text to display on download button (e.g. 'click here')
    button_or_markdown (Literal[&quot;button&quot;, &quot;text&quot;], optional):
         Function either makes the streamlit
    pickle_it (bool): If True, pickle file.
    button_css (None, str): CSS for the button. If None, defaults to pregenerated css

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return
    # bytes
    elif isinstance(object_to_download, bytes):
        pass
    # pd.DataFrame Object
    elif isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False,
                                                       encoding="utf-8-sig",
                                                       quoting=csv.QUOTE_NONNUMERIC)
    # String Object
    elif isinstance(object_to_download.getvalue().decode(), str):
        object_to_download = object_to_download.getvalue().decode()
    # Try JSON encode for everything else
    else:
        object_to_download = json.dumps(object_to_download)
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as _e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub(r"\d+", "", button_uuid)

    if button_css is None:
        button_css = f"""
        <style>
            #{button_id} {{
                background-color: #0E1117;
                color: #FAFAFA;
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: #262730;
                border-image: initial;
            }}
            #{button_id}:hover {{
                border-color: #7D373E;
                color: #7D373E;
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: #262730;
                color: #262730;
                }}
        </style> """

    dl_link = button_css + \
        f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'  # noqa: E501
    st.markdown(dl_link, unsafe_allow_html=True)
