from uuid import UUID

FILTER_CSS = """
<p style="color: $colorff;
            background-color: $color20;
            border: 2px solid $colorff;
            border-radius: 5px;
            padding: 0 5px;
            font-size: 10pt;
            display: inline-block;">
    $text
</p>
"""

class Tag:
    """A class representing a tag.

    Properties:
    ----------
        id: UUID
            The guid of the tag
        color: str
            The color of the tag
        name: str
            The name of the tag

    Methods:
    -------
        to_html()
        serialize()
        to_dict()
        update_values(name, color)

    """

    @property
    def id(self) -> UUID:
        """Return the guid of the tag."""
        return self.__id

    @property
    def color(self) -> str:
        """Return the hex color code of the tag."""
        return self.__color

    @property
    def name(self) -> str:
        """Return the label of the tag."""
        return self.__name

    def __init__(self, id: UUID, color: str, name: str):  # noqa: A002
        """Initialize a new Tag object with the provided id, color, and name.

        Args:
        ----
        id (UUID): The unique identifier for the tag.
        color (str): The hex color code for the tag.
        name (str): The label or name of the tag.

        Returns:
        -------
        None

        Raises:
        ------
        ValueError: If the provided id is not a valid UUID.

        Notes:
        -----
        The __init__ method is a special method in Python classes that is automatically
        called when a new instance of the class is created. It is used to initialize the
        attributes of the new instance.

        """
        self.__id = id
        self.__color = color
        self.__name = name

    def to_html(self) -> str:
        """Return the html element to represent the tag."""
        return FILTER_CSS.replace("$text", self.name).replace("$color", self.__color)

    def serialize(self) -> str:
        """Return the json of the tag."""
        return f'{{"id": \"{self.__id}\", "name": \"{self.__name}\", "color": \"{self.__color}\"}}'  # noqa: Q004, E501

    def to_dict(self) -> dict:
        """Return the dictionary representation of the tag."""
        return {
            "id": self.__id,
            "name": self.__name,
            "color": self.__color,
        }

    def update_values(self, name: str, color: str) -> None:
        """Acts as the setter for properties."""
        self.__name = name
        self.__color = color
