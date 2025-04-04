# noqa: INP001 Don't want __init__.py in the top level for pytest
"""Data storage class for information about tools."""
class ToolMetadata:
    """A class representing a tool's metadata.

    Attributes
    ----------
    __tool_name : str
        The name of the tool.
    __tool : function
        Function entry point into the tool.
    __accepted_file_types : list[str]
        The types of files the tool handles.
    __uses : list[str]
        Explanation of use cases for the tool.
    __category : str
        Category that the tool belongs to.
    __image_path : str
        Path to the tools icon.
    __nickname : str
        Alias for the tool.
    __featured : bool
        Whether or not the tool is featured. Affects tool placement within
        streamlit.
    __requires_network_access : bool
        True if the tool expects to be able to utilize publicly available
        resources.
    __port : int
        Optional port number tool is hosted on. Defaults to None.
    __visibility : bool
        True if the tool is meant to be visible to non-admin users

    Methods
    -------
    get_tool_name():
        Returns the name of the tool.
    get_tool():
        Returns the functional entry point for the tool.
    get_accepted_file_types():
        Returns the list of file types the tool is expected to handle.
    get_accepted_file_types_list():
        Returns the list of file types as list[str].
    get_uses():
        Returns the use cases for the tool.
    get_category()
        Returns the category the tool belongs to.
    get_image_path()
        Return the path to the tool icon.
    get_nickname()
        Return the aliases for the tool.
    get_featured()
        Return whether or not the tool is in the featured set.
    get_requires_network_access()
        Return whether or not the tool expects to be able to utilize publicly
        available resources.
    get_port()
        Returns the port associated with tool.
    get_visibility()
        Return whether or not the tool is meant to be visible to non-admin users
    set_visibility()
        Set whether or not the tool is meant to be visible to non-admin users
    get_tags()
        Returns the tags that the tool belongs to.

    """

    def __init__(self, tool_name, tool, accepted_file_types, uses, category,  # noqa: PLR0913
                 image_path=None, nickname=None, featured=False,
                 requires_network_access=False, requires_map_service=False,
                 requires_cached_model=False, port=None, visibility=True,
                 tags=None, local_tool=None):
        """Create a holder for tool metadata."""
        self.__tool_name = tool_name
        self.__tool = tool
        self.__accepted_file_types = accepted_file_types
        self.__uses = uses
        self.__category = category
        self.__image_path = image_path
        self.__nickname = nickname
        self.__featured = featured
        self.__requires_network_access = requires_network_access
        self.__requires_map_service = requires_map_service
        self.__requires_cached_model = requires_cached_model
        self.__port = port
        self.__visibility = visibility
        self.__tags = tags
        self.__local_tool = local_tool

    def get_tool_name(self):
        """Return the name of the tool."""
        return self.__tool_name

    def get_tool(self):
        """Return the tool."""
        return self.__tool

    def get_accepted_file_types(self):
        """Return the types of files the tool accepts."""
        return ", ".join(self.__accepted_file_types)

    def get_accepted_file_types_list(self):
        """Return the types of file the tool accepts as list[str]."""
        return self.__accepted_file_types

    def get_uses(self):
        """Return the various uses of the tool."""
        return ", ".join(self.__uses)

    def get_category(self):
        """Return the category of the tool."""
        return self.__category

    def get_image_path(self):
        """Return the path to the image of the tool if available."""
        return self.__image_path

    def set_image_path(self, image_path: str):
        """Set the image path of the tool."""
        self.__image_path = image_path

    def get_nickname(self):
        """Return the nickname of the tool if available."""
        return self.__nickname

    def get_featured(self):
        """Return bool representing if tool is featured."""
        return self.__featured

    def get_requires_network_access(self):
        """Return bool representing if network access is required."""
        return self.__requires_network_access

    def get_requires_map_service(self):
        """Return bool representing if map service is required."""
        return self.__requires_map_service

    def get_requires_cached_model(self):
        """Return bool representing if cached model is required."""
        return self.__requires_cached_model

    def get_port(self):
        """Return port associated with the tool."""
        return self.__port

    def get_visibility(self):
        """Return bool representing if the tool is visible to non-admin users."""
        return self.__visibility

    def set_visibility(self, updated_visibility):
        """Set bool representing if the tool is visible to non-admin users."""
        self.__visibility = updated_visibility

    def get_tags(self):
        """Return list of tags associated with the tool."""
        return self.__tags

    def get_local_tool(self):
        """Return local tool."""
        return self.__local_tool
