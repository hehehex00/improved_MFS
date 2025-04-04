from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Generator  # noqa: UP035

from config.config import analytics_password
from data_toolbox.utils import streamlit_analytics

log = logging.getLogger("Toolbox")

def get_analytics_context() -> Generator[any, any, None] | None:
    """Provide an analytics context object for use.

    In case analytics are disabled, None is returned.

    Returns
    -------
    Generator[any, any, None] or None

    """
    # Track user interactions using Streamlit Analytics
    # Inspiration for handling it like this taken from the following resources
    # 12factor.net/config 12factor.net/logs
    # Prefer an analytics storage location passed in the environment but fall
    # back to a locally saved file. The locally saved file will not preserve
    # the analytics between runs but is a failsafe so code runs given bad
    # configuration.
    try:
        enable_analytics = os.environ.get("LOG_ANALYTICS")
        if enable_analytics == "True":
            log.info("Enable Analytics = True")
            analytics_file = os.environ.get("SL_ANALYTICS_PATH")
            log.info("Analytics Path obtained")
            if not analytics_file:
                log.info("Analytics Path not set, setting up default path")
                analytics_file = str(Path("../../analytics.json"))

            # In order to log analytics, streamlit apps must be run
            # with streamlit_analytics.track
            return streamlit_analytics.track(verbose=False,
                                                        unsafe_password=analytics_password(),
                                                        save_to_json=analytics_file,
                                                        load_from_json=analytics_file)
    except Exception:
        log.exception("Analytics failed to start!")
        return None
    # If we aren't logging analytics, we can skip and execute toolbox normally.
    return None
