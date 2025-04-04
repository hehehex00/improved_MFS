"""Text Extractor Class.

Contains methods for extracting text from various file types.
"""
import re
from pathlib import Path

import docx2txt
import pypdf
import streamlit as st
from bs4 import BeautifulSoup
from odfdo import Document


class TextExtractor:
    """A class that handles extracting text from various types of files.

    Attributes:
    ----------
    - valid_exts (list): List of valid extensions currently handled by text_extractor,
    which includes "html", "htm", "pdf", "docx", "txt"

    Methods:
    -------
    - extract_docx(file, cleanup=True): Extract text from a .docx file
    - extract_html(file, cleanup=True): Extract text from a HTML file
    - extract_pdf(file, cleanup=True): Extract text from a PDF file
    - extract_txt(file, cleanup=True): Extract text from a txt file
    - text_cleanup(text): Cleans up input string through a series of regex substitutions
    - text_extractor_ui(): User interface for uploading files and extracting text

    """

    # List of valid extensions currently handled by text_extractor
    valid_exts = ["html", "htm", "pdf", "docx", "txt"]

    def __init__(self):
        """Return streamlit ui."""
        self.text_extractor_ui()

    ### PLEASE KEEP METHODS IN ALPHABETICAL ORDER FOR BETTER ORGANIZATION ###

    @staticmethod
    def extract_docx(file, *, cleanup: bool = True) -> str:
        """Extract text from a .docx file.

        Args:
        ----
            file (_type_):  uploaded file from streamlit file uploaded
            cleanup (bool, optional): run text_extractor.text_cleanup on extracted text.
            Defaults to True.

        Returns:
        -------
            str: string object

        """
        text = docx2txt.process(file)
        if cleanup:
            text = TextExtractor.text_cleanup(text)
        return text

    @staticmethod
    def extract_html(file, *, cleanup: bool = True) -> str:
        """Extract text from a HTML file.

        Args:
        ----
            file (_type_): uploaded file from streamlit file uploaded
            cleanup (bool, optional): run text_extractor.text_cleanup on extracted text.
            Defaults to True.

        Returns:
        -------
            str: string object

        """
        text = ""
        content = file.read().decode("utf-8")
        soup = BeautifulSoup(content, "lxml")
        # strips html tags away from parsed text
        tag = soup.select_one("li:nth-of-type(2)")
        if tag:
            tag.decompose()
        text += soup.body.get_text(strip=True)
        if cleanup:
            text = TextExtractor.text_cleanup(text)
        return text

    @staticmethod
    def extract_odt(file, *, cleanup: bool = True) -> str:
        """Extract text from ODT file.

        Args:
        ----
            file (_type_): uploaded file from streamlit file uploaded
            cleanup (bool, optional): run text_extractor.text_cleanup on extracted text.
            Defaults to True.

        Returns:
        -------
            str: string object

        """
        odt_doc = Document(file) # load ODT file
        odt_text = odt_doc.get_formatted_text()
        if cleanup:
            odt_text = TextExtractor.text_cleanup(odt_text)
        return odt_text

    @staticmethod
    def extract_pdf(file, *, cleanup: bool = True) -> str:
        """Extract text from a PDF file.

        Args:
        ----
            file (_type_): uploaded file from streamlit file uploaded
            cleanup (bool, optional): run text_extractor.text_cleanup on extracted text.
            Defaults to True.

        Returns:
        -------
            str: string object

        """
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        if cleanup:
            text = TextExtractor.text_cleanup(text)
        return text

    @staticmethod
    def extract_txt(file, *, cleanup: bool = True) -> str:
        """Extract text from a txt file.

        Args:
        ----
            file (_type_): uploaded file from streamlit file uploaded
            cleanup (bool, optional): run text_extractor.text_cleanup on extracted text.
            Defaults to True.

        Returns:
        -------
            str: string object

        """
        text = Path(file).read_text()
        if cleanup:
            text = TextExtractor.text_cleanup(text)
        return text

    @staticmethod
    def text_cleanup(text: str) -> str:
        """Clean up input string through a series of regex substitutions.

        Args:
        ----
            text (str): input string object from one of the extract_XXX methods

        Returns:
        -------
            str: string object

        """
        # Add spaces between lower and Upper case letters
        text = re.sub(r" +", " ", text)
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
        text = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", text)
        text = re.sub(r"(\.)([^\W])", r"\1 \2", text)
        # Add spaces after punctuation
        text = re.sub(r"([.,!?:;])([^'\",@#\$%^])", r"\1 \2", text)
        return re.sub(r" +", " ", text)

    def text_extractor_ui(self):
        """UI to interact, test and experiment with the text extractor utils."""
        uploaded_files = st.file_uploader("Uploaded Files for Testing",
                                          type=sorted(
                                              TextExtractor.valid_exts),
                                          accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                st.write(file.name)
                ext = file.name.split(".")[-1].lower()
                match ext:
                    case "pdf":
                        text = TextExtractor.extract_pdf(file)
                        with st.status(file.name, state="complete"):
                            st.download_button(f"Download {file.name} as string",
                                               text, f"{file.name}.txt")
                            st.write(text)

                    case "html":
                        text = TextExtractor.extract_html(file)
                        with st.status(file.name, state="complete"):
                            st.download_button(f"Download {file.name} as string",
                                               text, f"{file.name}.txt")
                            st.write(text)

                    case "htm":
                        text = TextExtractor.extract_html(file)
                        with st.status(file.name, state="complete"):
                            st.download_button(f"Download {file.name} as string",
                                               text, f"{file.name}.txt")
                            st.write(text)

                    case "docx":
                        text = TextExtractor.extract_docx(file)
                        with st.status(file.name, state="complete"):
                            st.download_button(f"Download {file.name} as string",
                                               text, f"{file.name}.txt")
                            st.write(text)

                    case "odt":
                        text = TextExtractor.extract_odt(file)
                        with st.status(file.name, state="complete"):
                            st.download_button(f"Download {file.name} as string",
                                               text, f"{file.name}.txt")
                            st.write(text)

                st.write("---")
