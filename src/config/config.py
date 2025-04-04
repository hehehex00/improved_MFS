"""Initial configuration for the streamlit app."""
from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv


def analytics_password() -> str:
    """Unsafe password management for basic access control.

    Parameters
    ----------
    None

    Returns
    -------
    str
        Password for analytics

    """
    # Load secrets file
    load_dotenv("./config/secrets.env")
    # Pull password from environment variables:
    password = os.environ.get("ANALYTICS_PASSWORD")
    if password:
        return password
    # If password has not been configured, fallback to default:
    return "Pl3@$e-set-the-password"

# Minimum number of domain parts required for a valid domain
MIN_DOMAIN_PARTS = 2

def strip_domains_from_host(host: str) -> str:
    """Extract the second-level and top-level domains from a hostname.

    Parameters
    ----------
    host : str
        The full hostname to process (e.g. 'sub.example.com')

    Returns
    -------
    str
        The second-level and top-level domains joined with a dot (e.g. 'example.com').
        Returns empty string if hostname has fewer than 2 parts.

    """
    parts = host.split(".")

    suffix_len = int(os.environ.get("TOP_DOMAIN_LEN"))
    if len(parts) >= MIN_DOMAIN_PARTS:
        return ".".join(parts[-suffix_len:])
    return ""

def get_second_and_top_domain() -> str:
    """Get the second and top level domain from the current session's host.

    Returns
    -------
    str
        The second and top level domain

    """
    # ....dont @ me it works #blamestreamlitandgreg
    sessions = st.runtime.get_instance()._session_mgr.list_active_sessions()  # noqa: SLF001
    host = sessions[0].client.request.host
    return strip_domains_from_host(host)

def get_protocol() -> str:
    """Get the protocol to use for URLs.

    Returns
    -------
    str
        The protocol (https)

    """
    return "https"

def is_dev_environment() -> bool:
    """Check if this is a development environment.

    Returns
    -------
    bool
        True if this is a dev environment, False otherwise

    """
    # Checks if "dev-" is in the host URL
    sessions = st.runtime.get_instance()._session_mgr.list_active_sessions()  # noqa: SLF001
    host = sessions[0].client.request.host
    return "dev-" in host

def get_tool_url(tool_name: str) -> str:
    """Get the URL for a tool.

    Parameters
    ----------
    tool_name : str
        The name of the tool

    Returns
    -------
    str
        The complete URL for the tool

    """
    prefix = "dev-" if is_dev_environment() else ""
    return f"{get_protocol()}://{prefix}{tool_name}.{get_second_and_top_domain()}"

def main_port() -> str:
    """Load Main Streamlit App's Network Port for redirection purposes.

    Defines the primary app's container port. If not given via env-var
    defaults to 8501.

    Returns
    -------
    str
        Network port for main streamlit app.

    """
    port = os.environ.get("NETWORK_PORT")
    if port:
        return port
    return "8501"
