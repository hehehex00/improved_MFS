import streamlit as st

from data_toolbox.tag_manager.singletons import manager
from data_toolbox.tag_manager.tag import Tag

COLOR_DIV = """
<div style="
    background-color:$color;
    height:20px;
    width:40px;
    display:inline-block;
    border-radius: 10px;"/>
"""

class TagEditView:
    """Handle interaction with streamlit for editing tags.

    Methods:
    -------
        show()

    """

    def __init__(self, tag: Tag):
        """Initialize the TagEditView object with a given Tag instance.

        Arguements:
        ----------
        - tag (Tag): The Tag instance to be associated with the TagEditView object.

        Attributes:
        ----------
        - __tag (Tag): The Tag instance associated with the TagEditView object.

        """
        self.__tag = tag

    def show(self) -> None:
        """Initiate UI for the editor."""
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            placeholder = st.empty()
            delete_bttn = placeholder.button("Delete", key=f"{self.__tag.id}_Delete_Bttn")
            if delete_bttn:
                manager.delete_tag(self.__tag)
                placeholder.empty()
                return
        with col3:   # noqa: SIM117
            with st.expander("Edit Tag :pencil2:"):
                name = st.text_input("Tag Name", self.__tag.name)
                color = st.color_picker("Tag Color",
                self.__tag.color,
                key=f"{self.__tag.id}_Color_Picker")
                self.__tag.update_values(name, color)
        with col1:
            st.text(self.__tag.name)
        with col2:
            div = COLOR_DIV.replace("$color", self.__tag.color)
            st.markdown(div, unsafe_allow_html=True)
