import logging
from configparser import ConfigParser
from pathlib import Path

from data_toolbox.utils.config_encryption.aes_manager import AESManager


class ProtectedConfigWriter:
    """Protected configuration writer that will AES encrypt and base64 encode the values.

    Note: Always call edit_or_create() before set()

    Methods:
    -------
    set()
    edit_or_create()

    """

    def __init__(self, aes_manager: AESManager, defaults=None, dict_type=dict, allow_no_value=False):  # noqa: E501
        """Create ProtectedConfigWriter instance."""
        self.__aes_manager = aes_manager
        self.__config_reader = ConfigParser(defaults, dict_type, allow_no_value)

    def set(self, section: str, option: str, value: str) -> None:
        """Set an item in the protected config.

        Args:
        ----
        section (str): The overall section in the config file
        option (str): The item in the config file
        value (str): The value to encrypt and store in the config file

        """
        if not self.__config_reader.has_section(section):
            self.__config_reader.add_section(section)

        encrypted = self.__aes_manager.encrypt(value)
        self.__config_reader.set(section, option, encrypted)

    def edit_or_create(self, protected_config_file_path: str) -> None:
        """Read the protected config file.

        Args:
        ----
        protected_config_file_path (str): The path to the configuration file

        """
        self.__aes_manager.ensure_key()
        self.__aes_manager.ensure_nonce()

        if Path(protected_config_file_path).exists() and protected_config_file_path.endswith(".ini"):  # noqa: E501
            return

        logging.info("Could not load configuration file, creating it at %s", protected_config_file_path)  # noqa: E501
        Path(protected_config_file_path).open("w", encoding="utf-8").close()

        self.__config_reader.read(protected_config_file_path)

    def write(self, protected_config_file_path: str) -> None:
        """Write the protected config file.

        Args:
        ----
        protected_config_file_path (str): The path to the configuration file

        """
        with Path(protected_config_file_path).open("w", encoding="utf-8") as fp:
            self.__config_reader.write(fp)
