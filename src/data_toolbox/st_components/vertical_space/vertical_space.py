import streamlit as st


def vertical_space(height: int):
    """Render vertical space with given height.

    Parameters
    ----------
    height : int
        The height of the vertical spacer

    Returns
    -------
    None

    """
    for _ in range(height):
        st.markdown("")
