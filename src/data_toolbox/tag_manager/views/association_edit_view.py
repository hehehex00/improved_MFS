import streamlit as st

from data_toolbox.tag_manager.association import Association
from data_toolbox.tag_manager.singletons import manager


class AssociationEditView:
    """Handle interaction with streamlit for editing of associations.

    Methods:
    -------
        show()

    """

    def __init__(self, association: Association):
        """Initialize the AssociationEditView object with the provided Association object.

        :param association: Association
            The Association object that this view will be editing.
        """
        self.__association = association

    def show(self) -> None:
        """Initiate UI for the editor."""
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:  # noqa: SIM117
            with st.expander("Edit :pencil2:"):
                updated_tags = st.multiselect("Tags",
                    [tag.name for tag in manager.tags],
                    default=self.__get_default_tags(),
                    key=self.__association.project_name)
                self.__set_updated_tags(updated_tags)
        with col1:
            st.text(self.__association.project_name)
        with col2:
            markdown = ""
            for tag_id in self.__association.tags:
                tag = manager.get_tag_by_id(tag_id)
                if tag:
                    markdown = markdown + tag.to_html()
            st.markdown(markdown, unsafe_allow_html=True)

    def __get_default_tags(self) -> list:
        """Get the current list of tags."""
        default_tags = [manager.get_tag_by_id(tag_id) for tag_id \
                        in self.__association.tags if manager.get_tag_by_id(tag_id)]
        return [tag.name for tag in default_tags]

    def __set_updated_tags(self, updated_tags: list) -> None:
        """Set the new tag list.

        :param updated_tags: List[str]
            List of tag names that should now be associated with the tool
        """
        updated_tag_ids = [manager.get_tag(tag_name).id for tag_name in updated_tags]
        self.__association.set_tags(updated_tag_ids)
