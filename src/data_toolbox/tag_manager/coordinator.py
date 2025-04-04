from pathlib import Path
from uuid import UUID

import pandas as pd

from .association import Association


class Coordinator:
    """A class used to manage associations between projects and its list of tags.

    Properties:
    ----------
        associations: dict[str, Association]
            Dictionary of Association objects keyed on their project name

    Methods:
    -------
        add_association(key, tag_id)
        add_associations(project_name, tag_ids)
        get_association(key)
        association_exists(project_name, tag_id)
        import_associations(input_file)
        reload_associations()
        export_associations()

    """

    @property
    def associations(self) -> dict:
        """Returns dictionary of project-tag list associations.

        Returns dictionary of project-tag list associations where
        the key is the project and the value is a list of Association objects.
        """
        return self.__associations

    def __init__(self):
        """Initialize the Coordinator object.

        :return: None
        """
        self.__associations = {}
        self.__import_file = None

    def add_association(self, key: str, tag_id=None) -> None:
        """Add a tag association to the given project's list of tags.

        :param key: str
            The project name
        :param tag_id: UUID
            The tag guid
        """
        if key not in self.__associations:
            self.__associations[key] = Association(key, [])
        if tag_id and tag_id not in self.__associations[key].tags:
            self.__associations[key].add_tag(tag_id)

    def add_associations(self, project_name: str, tag_ids: list) -> None:
        """Add multiple associations given a project name and a list of tag ids.

        :param project_name: str
            The project name
        :param tag_ids: List[UUID]
            The list of tag guids
        """
        for tag_id in tag_ids:
            self.add_association(project_name, tag_id)

    def get_association(self, key: str) -> Association:
        """Return the association for the project."""
        if key not in self.__associations:
            self.__associations[key] = Association(key, [])
        return self.__associations[key]

    def association_exists(self, project_name: str, tag_id: UUID) -> bool:
        """Check if an association exists for the given project."""
        if project_name not in self.__associations:
            return False
        return tag_id in self.__associations[project_name]

    def import_associations(self, import_file: str) -> None:
        """Import associations from the given file.

        :param import_file: str
            The file to import associations from
        """
        self.__import_file = import_file
        associaton_df = pd.read_json(self.__import_file, lines=True)
        for row in range(len(associaton_df)):
            self.__import_association(associaton_df.iloc[row])

    def reload_associations(self) -> None:
        """Reload associations from the previously imported file.

        :param None:
        :return: None
        """
        reload_df = pd.read_json(self.__import_file, lines=True)
        for row in range(len(reload_df)):
            self.__import_association(reload_df.iloc[row])

    def export_associations(self) -> None:
        """Export associations to the given file."""
        serialized_associations = []
        self.__associations = dict(sorted(self.__associations.items()))  # noqa: E501
        serialized_associations = [association.serialize() for association in self.__associations.values()]  # noqa: E501
        with Path.open(self.__import_file, "w") as f:
            f.write("\n".join(serialized_associations))

    def __import_association(self, association: dict) -> None:
        """Import a single association.

        :param association: dict[str, str]
            Dictionary representation of the association
        """
        key = association["project_name"]
        tags = [UUID(tag_str) for tag_str in association["tags"]]
        self.__associations[key] = Association(key, tags)
