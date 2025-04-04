import streamlit as st

from data_toolbox.tag_manager.singletons import coordinator, manager

from .association_edit_view import AssociationEditView
from .tag_creation_view import TagCreationView
from .tag_edit_view import TagEditView

COLOR_BOX = """
<div style="padding:5px; vertical-align:middle">
  <div style="
        display:inline-block;
        text-align:center;
        vertical-align:middle;">
    $text
  </div>
  <div style="
        background-color:$color;
        height:20px;
        width:40px;
        display:inline-block;
        border-radius: 10px;
        vertical-align:middle;" />
</div>
"""

class TagManagerView:
    """Handle interaction with streamlit for the main tag manager screen.

    Methods:
    -------
    show()

    """

    def show(self) -> None:
        """Initiate the UI."""
        st.title("Tag Manager")

        TagCreationView(manager).show()

        st.subheader("Existing Tags")
        for tag in manager.tags:
            tag_edit_view = TagEditView(tag)
            tag_edit_view.show()

        st.subheader("Project-Tag Associations")
        for key in coordinator.associations:
            association_edit_view = AssociationEditView(coordinator.associations[key])
            association_edit_view.show()

        # Finalize
        manager.export_tags()
        coordinator.export_associations()
