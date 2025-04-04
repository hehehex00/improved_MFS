from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path

from data_toolbox.utils.config_encryption.aes_manager import AESManager


class ProtectedConfigReader:
    """Protected configuration reader that will read AES encrypted and base64 encoded values.

    Note: Always call read() before set()

    Methods:
    -------
    get()
    read()

    """

    def __init__(self, aes_manager: AESManager, defaults=None, dict_type=dict, allow_no_value=False):  # noqa: E501
        """Create ProtectedConfigReader instance."""
        self.__aes_manager = aes_manager
        self.__config_reader = ConfigParser(defaults, dict_type, allow_no_value)

    def get(self, section: str, option: str) -> str:
        """Get an item from the protected config.

        Args:
        ----
        section (str): The overall section in the config file
        option (str): The item in the config file

        Returns:
        -------
        str: The plaintext value from the config

        """
        value = self.__config_reader.get(section, option)

        return self.__aes_manager.decrypt(value)

    def read(self, file_path: str):
        """Read the protected config file.

        Args:
        ----
        file_path (str): The path to the config file

        """
        if not Path(file_path).exists() and not file_path.endswith(".ini"):
            logging.error("Could not load configuration file at %s", file_path)
            return

        self.__config_reader.read(file_path)
