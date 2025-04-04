"""Perform common string utility operations."""
from __future__ import annotations


def hex2rgb(hexcode_str: str) -> tuple[int, int, int]:
    """Convert hexcode to red, green, and blue values scaled 0 to 255.

    Args:
    ----
        hexcode_str (str): Hexcode of a color eg ("#000000)

    Returns:
    -------
        tuple[int,int,int]: int values of red, green, blue

    Example:
    -------
        >>>hexcode = "#FF0000"

        >>>r,g,b = hex2rgb(hexcode)

        >>>for value in (r,g,b): print(value)

        255

        0

        0

    """
    if len(hexcode_str) != 7 or hexcode_str[0] != "#":  # noqa: PLR2004
        error_msg = f"{hexcode_str} Invalid Hexcode"
        raise ValueError(error_msg)
    # Remove the "#"" Character
    hexcode = hexcode_str.strip("#")
    r = int(hexcode[0:2], 16)
    g = int(hexcode[2:4], 16)
    b = int(hexcode[4:6], 16)

    return r, g, b


def rgb2hex(red: int, green: int, blue: int) -> str:
    """Convert red, green, and blue values scaled 0 to 255 into hexcode.

    Args:
    ----
        red (int): Red Value
        green (int): Green Value
        blue (int): Blue Value

    Returns:
    -------
        str: Hexcode string of argument tuple

    """
    for value in (red, green, blue):
        if value > 255 or value < 0:  # noqa: PLR2004
            error_msg = "red, green, blue values must be int between 0 and 255"
            raise ValueError(error_msg)
    return f"#{int(red):02x}{int(green):02x}{int(blue):02x}"
