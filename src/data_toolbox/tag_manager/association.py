from uuid import UUID


class Association:
    """A class representing an association.

    Properties:
    ----------
        project_name: str
            The name of the project
        tags: List[UUID]
            The list of tags guids for tags associated with the project

    Methods:
    -------
        add_tag(tag)
        set_tags(new_ta

    """

    @property
    def project_name(self) -> str:
        """Returns the project name."""
        return self.__project_name

    @property
    def tags(self) -> list:
        """Returns the list of tags."""
        return self.__tags

    def __init__(self, project_name: str, tags: list[UUID]):  # noqa: FA102
        """Initialize a new Association object.

        Args:
        ----
        project_name (str): The name of the project.
        tags (List[UUID]): The list of tags guids for tags associated with the project.

        Returns:
        -------
        None

        Raises:
        ------
        ValueError: If the 'tags' parameter is not a list.

        Initializes an Association object with the provided project name, tags.
        It sets the project name and tags attributes of the object.
        If the 'tags' parameter is not a list, a ValueError will be raised.

        """
        if not isinstance(tags, list):
            error = "The 'tags' parameter must be a list."
            raise TypeError(error)
        self.__project_name = project_name
        self.__tags = tags

    def __str__(self) -> str:
        """Return a string representation of the Association object.

        Returns:
        -------
        str: A string containing the project name and the list of tags.

        """
        return f"project_name: {self.project_name}, tags: {self.tags}"

    def add_tag(self, tag_id: UUID) -> None:
        """Add a tag to the list of tags."""
        self.__tags.append(tag_id)

    def set_tags(self, new_tags: list):
        """Set the list of tags.

        :param new_tags: List[UUID]
            List of tag guids
        """
        self.__tags = new_tags

    def serialize(self) -> str:
        """Return the serialized string."""
        tag_str = [f'"{tag_id}"' for tag_id in self.__tags]
        return (f'{{"project_name": "{self.__project_name}", "tags": [{", ".join(tag_str)}]}}')  # noqa: E501
