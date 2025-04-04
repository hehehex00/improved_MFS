def determine_file_extension(file_name: str) -> str:
    """Determine the type of file based on its extension.

    Parameters
    ----------
    file_name : str
        The name of a file, without its path.

    Returns
    -------
    str

    """
    if file_name.endswith(".tar.gz"):
        return "tar.gz"
    return file_name.split(".")[-1].lower()

BYTES_PER_KIBIBYTE = 1024.0

def human_readable_size_of(file_size: int, suffix: str = "B") -> str:
    """Create a human-readable string representation of a file size.

    See https://stackoverflow.com/a/1094933.

    Parameters
    ----------
    file_size : int
        The size of the files in bytes
    suffix : str
        The suffix to use in the returned string

    Returns
    -------
    str

    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(file_size) < BYTES_PER_KIBIBYTE :
            return f"{file_size:3.1f}{unit}{suffix}"
        file_size /= BYTES_PER_KIBIBYTE
    return f"{file_size:.1f}Yi{suffix}"
