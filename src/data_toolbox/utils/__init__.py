"""Utils Module.

A collection of reusable, non-UI related, utilities.

"""

from .files import determine_file_extension
from .greetings import Greeting, greetings
from .string_utils import TextConverter, TextExtractor, string_operations
from .uploaded_file_extensions import (
    determine_file_extensions,
    display_restored_uploaded_files,
    file_upload_result_to_file_list,
    restore_uploaded_files,
    store_uploaded_files_for_page_switch,
    were_files_restored,
)
