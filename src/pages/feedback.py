import csv
from pathlib import Path

import streamlit as st

from data_toolbox.application_layout.application_layout import embed_in_application_layout
from data_toolbox.tag_manager.singletons import coordinator, manager


def display_feedback_section():
    """Display "Feedback" component.

    Returns
    -------
    None

    """
    # Create a directory for feedback data if it doesn't exist
    feedback_dir = "./feedback_data"  # Define the directory path within the container
    Path(feedback_dir).mkdir(parents=True, exist_ok=True)
    # Create an empty list to store feedback
    feedback_list = []
    def save_feedback_to_csv(feedback_list):
        # Define the path to the feedback data file within the container
        feedback_file_path = Path(feedback_dir) / "feedback.csv"
        with Path.open(feedback_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for feedback in feedback_list:
                writer.writerow([feedback["Type"], feedback["Feedback"]])
    # Feedback collection form
    st.title("💬 Feedback")
    st.markdown("""
    Please provide your feedback using the form below to help improve the Data Toolbox.
    """)
    # Create a text area for users to enter feedback
    user_feedback = st.text_area("Enter your feedback here:")
    # Create a selectbox to choose feedback type
    feedback_type = st.selectbox(
        "Select feedback type:",
        ["Bug Report", "Feature Request", "General Feedback"],
        )
    # Create a button to submit feedback
    if st.button("Submit Feedback"):
        feedback_entry = {
            "Type": feedback_type,
            "Feedback": user_feedback,
        }
        feedback_list.append(feedback_entry)
        save_feedback_to_csv([feedback_entry])  # Save the new feedback entry to CSV
        st.success("Feedback submitted successfully!")

if __name__ == "__main__":
    # Track Current Page
    st.session_state["current_page"] = "Feedback"
    tag_file = (Path(__file__).parent.parent /
            "data_toolbox" /
            "tag_manager" /
            "tags.jsonl")
    manager.import_tags(tag_file)

    association_file = (Path(__file__).parent.parent /
                    "data_toolbox" /
                    "tag_manager" /
                    "associations.jsonl")
    coordinator.import_associations(association_file)
    embed_in_application_layout(
        display_feedback_section,
        page_title="Data Toolbox - 💬 Feedback",
    )
