"""Text Converter Class.

Contains methods for converting text
"""

import re

import pandas as pd


class TextConverter:
    """Class for converting text.

    Methods:
    -------
    - text_to_df: Static method that takes a text input and converts it into a pandas
    DataFrame with all words in a column called "Word"

    """

    def __init__(self):
        """Class constructor (no parameters)."""

    @staticmethod
    def text_to_df(text: str)->pd.DataFrame:
        """Convert text to a pandas dataframe with all words in a column called "Word".

        Args:
        ----
        text (str): String object.

        Returns:
        -------
        pd.DataFrame: dataframe with all words in text in a column called "Word".

        """
        # Split on word boundaries, removing empty spaces
        word_list = [word.strip() for word in re.split(r"\b", text) if word.strip()]
        # Remove 'words' that do not have a valid letter in them e.g. ":"
        word_list = [word for word in word_list if re.search(r"[^\W]+", word)]

        out = pd.DataFrame({"Word": word_list})
        out.attrs["original_text"] = text

        return out
