import streamlit as st


class TagCreationView:
    """Handle interaction with streamlit for tag creation.

    Methods:
    -------
        show()

    """

    def __init__(self, tag_manager):
        """Initialize the TagCreationView object.

        Parameters:
        ----------
        tag_manager : TagManager
            The TagManager object that will be used to manage tags.

        Attributes:
        ----------
        __default_name : str
            The default name for a new tag, initially an empty string.
        __default_color : str
            The default color for a new tag, initially set to white (#FFFFFF).
        __tag_manager : TagManager
            The TagManager object that will be used to manage tags.

        Returns:
        -------
        None

        """
        self.__default_name = ""
        self.__default_color = "#FFFFFF"
        self.__tag_manager = tag_manager

    def show(self):
        """Initiate the UI for creating a new tag.

        This method creates a Streamlit expander with a form for creating a new tag.
        It includes a text input for the tag name, a color picker for the tag color,
        and a submit button.

        If the submit button is clicked, it checks if the tag name already exists.
        If it does, it displays a toast message.
        If it doesn't, it creates a new tag with the provided name and color.

        Parameters:
        ----------
        None

        Returns:
        -------
        None

        """
        #Initiate the UI
        with st.expander("Create a new tag"):  # noqa: SIM117
            with st.form("Create New Tag", border=False):
                tag_name = st.text_input("Tag Name", self.__default_name, max_chars=25)
                tag_color = st.color_picker("Tag Color", self.__default_color)
                submit_bttn = st.form_submit_button(label="Create")
                if submit_bttn:
                    if tag_name == "":
                        st.warning("Tag name cannot be empty")
                    elif self.__tag_manager.tag_exists(tag_name):
                        st.toast("Tag already exists")
                    # Checks if tag color already exists
                    elif any(tag.color == tag_color for tag in self.__tag_manager.tags):
                        st.warning(f"A tag with the color '{tag_color}' already exists.")
                    else:
                        self.__tag_manager.create_new_tag(tag_name, tag_color)
