from pathlib import Path
from uuid import UUID, uuid4

import pandas as pd

from .tag import Tag


class TagManager:
    """Manage tags associated with tools, responsible for creation and export of tags.

    Properties:
    ----------
        tags : List[Tag]
            List of tags to manage

    Methods:
    -------
        create_new_tag(tag_name, tag_color)
        import_tags(import_file)
        reload_tags()
        tag_exists(tag_name)
        export_tags()
        to_dataframe()
        get_tag(tag_name)
        get_tag(tag_id)
        delete_tag(tag)

    """

    @property
    def tags(self) -> list:
        """Return a list of all the tags."""
        return self.__tags

    def __init__(self):
        """Initialize a new instance of the TagManager class.

        :param None:
            No parameters are required for initialization
        """
        self.__tags = []
        self.__import_file = None

    def create_new_tag(self, tag_name: str, tag_color: str) -> None:
        """Create a new tag with the given name and color.

        :param tag_name: str
            The name of the tag
        :param tag_color: str
            The color of the tag
        """
        tag_id = uuid4()
        tag = Tag(tag_id, tag_color, tag_name)
        self.__tags.append(tag)

    def import_tags(self, import_file: str) -> None:
        """Import tags from a json lines file.

        :param import_file: str
            The path to the tags json file
        """
        self.__import_file = import_file
        import_df = pd.read_json(self.__import_file, lines=True)
        for row in range(len(import_df)):
            self.__import_tag(import_df.iloc[row])

    def reload_tags(self) -> None:
        """Reload tags from the specified import file.

        Example:
        -------
        >>> manager = TagManager()
        >>> manager.import_tags("tags.json")
        >>> manager.reload_tags()

        """
        reload_df = pd.read_json(self.__import_file, lines=True)
        for row in range(len(reload_df)):
            self.__import_tag(reload_df.iloc[row])

    def tag_exists(self, tag_name: str) -> bool:
        """Check if a tag exists.

        Parameters:
        ----------
        tag_name: str
            The key of the tag

        """
        if not tag_name:
            return False
        return any(tag.name == tag_name for tag in self.__tags)

    def export_tags(self) -> None:
        """Export tags to a json string."""
        serialized_tags = []
        self.__tags.sort(key=self.__get_tag_name)
        for tag in self.__tags:
            serialized_tags = [tag.serialize() for tag in self.__tags]
        with Path.open(self.__import_file, "w") as f:
            f.write("\n".join(serialized_tags))

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the tags to a pandas dataframe."""
        return pd.DataFrame(tag.to_dict() for tag in self.__tags)

    def get_tag(self, tag_name: str) -> Tag:
        """Return the tag with the given name.

        Parameters:
        ----------
        tag_name: str
            The name of the tag

        """
        for tag in self.__tags:  # noqa: RET503
            if tag.name == tag_name:
                return tag

    def get_tag_by_id(self, tag_id: UUID) -> Tag:
        """Return the tag with the given id.

        Parameters:
        ----------
        tag_id: UUID
            The id of the tag

        """
        for tag in self.__tags:  # noqa: RET503
            if tag.id == tag_id:
                return tag

    def delete_tag(self, tag: Tag) -> None:
        """Remove a tag from the list of managed tags.

        Args:
        ----
        tag (Tag): The tag to be removed.

        Returns:
        -------
        None: This method does not return any value.

        Raises:
        ------
        ValueError: If the tag is not found in the list of managed tags.

        Example:
        -------
        >>> manager = TagManager()
        >>> tag1 = Tag(UUID('12345678-1234-1234-1234-123456789012'), 'red', 'Important')
        >>> manager.create_new_tag('Important', 'red')
        >>> manager.delete_tag(tag1)

        """
        self.__tags.remove(tag)

    def __import_tag(self, tag_dict: dict) -> None:
        """Add a tag from a dictionary.

        Parameters:
        ----------
        tag_dict: dict[str, str]
            The dictionary of attributes for a tag

        """
        tag = Tag(UUID(tag_dict["id"]), tag_dict["color"], tag_dict["name"])
        if not self.tag_exists(tag_dict["name"]):
            self.__tags.append(tag)

    def __get_tag_name(self, tag: Tag):
        return tag.name
