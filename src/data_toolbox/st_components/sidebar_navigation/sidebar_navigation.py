import streamlit as st


def sidebar_navigation():
     """Render the toolbox icon and available pages for navigation in the sidebar.

     Returns
     -------
     None

     """
     st.sidebar.image("./images/data_team_header_1_3_0.png")

     st.sidebar.divider()

     st.sidebar.page_link("main.py", label="Home", icon="🏠",
                              help="Open the landing page.")
     st.sidebar.page_link("pages/featured_tools.py", label="Featured Tools", icon="🎉",
                              help="Display the list of Featured Tools.")
     st.sidebar.page_link("pages/tool_wizard.py", label="Tool Wizard", icon="🧙🏽‍♂️",
                              help="Display the Tool Wizard, which helps you to find a tool "
                                   "that is compatible with your files.")
     st.sidebar.page_link("pages/tool_selection.py", label="Tool Search", icon="🔎",
                              help="Discover the different tools available to you, "
                                   "by filtering based on name, category, and other criteria.")
     st.sidebar.page_link("pages/feedback.py", label="Feedback", icon="💬")

     st.sidebar.divider()
