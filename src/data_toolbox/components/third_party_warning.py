"""Warn users about tool utilizing third party."""
from streamlit import info


def third_party_warning():
    """Print the third party warning."""
    info("This tool sends and receives data externally from third party resource(s)",
         icon="ℹ️")

if __name__ == "__main__":
    third_party_warning()
