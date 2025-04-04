import base64
import logging
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESManager:
    """Manages AES encryption/decryption using key and nonce files.

    This class handles AES encryption operations by managing key and nonce files.
    It provides methods to ensure key/nonce existence, encrypt and decrypt values.
    """

    def __init__(self, key_path: str, nonce_path: str):
        """Create AESManager instance.

        Args:
            key_path: Path to the AES key file
            nonce_path: Path to the AES nonce file

        """
        self.__key_path = key_path
        self.__nonce_path = nonce_path

    def ensure_key(self):
        """Generate 16 byte AES key using random bytes.

        Returns:
        -------
        None

        """
        if Path(self.__key_path).exists():
            return

        Path(self.__key_path).parent.mkdir(parents=True, exist_ok=True)

        key = get_random_bytes(16)
        self.__write_key(key)

    def ensure_nonce(self):
        """Generate 16 byte AES nonce using random bytes.

        Returns:
        -------
        None

        """
        if Path(self.__nonce_path).exists():
            return

        Path(self.__nonce_path).parent.mkdir(parents=True, exist_ok=True)

        nonce = get_random_bytes(16)
        self.__write_nonce(nonce)

    def encrypt(self, value: str) -> str:
        """Encrypt a value for a protected config.

        Args:
        ----
        value (str): The value to encrypt via AES

        Returns:
        -------
        str: ciphertext base64 encoded and tag

        """
        cipher = AES.new(self.__read_key(), AES.MODE_EAX, self.__read_nonce())
        ciphertext, _ = cipher.encrypt_and_digest(value.encode())

        return self.__encode(ciphertext).decode()

    def decrypt(self, value: str) -> str:
        """Decrypt a value from a protected config.

        Args:
        ----
        value (str): Base64 encoded and AES encrypted value

        Returns:
        -------
        str: Plaintext value if decryption is successful. None if error.

        """
        unbase64d = self.__decode(value)
        cipher = AES.new(self.__read_key(), AES.MODE_EAX, nonce=self.__read_nonce())

        try:
            return cipher.decrypt(unbase64d).decode()
        except ValueError:
            logging.exception("Cannot decrypt, key is incorrect or value corrupted.")
            return None

    def __encode(self, value: bytes) -> bytes:
        return base64.b64encode(value)

    def __decode(self, value: str) -> bytes:
        return base64.b64decode(value)

    def __read_key(self) -> bytes:
        with Path(self.__key_path).open(mode="r") as fp:
            return self.__decode(fp.read())

    def __write_key(self, key : bytes):
        with Path(self.__key_path).open(mode="w") as fp:
            fp.write(self.__encode(key).decode())

    def __read_nonce(self) -> bytes:
        with Path(self.__nonce_path).open(mode="r") as fp:
            return self.__decode(fp.read())

    def __write_nonce(self, nonce : bytes):
        with Path(self.__nonce_path).open(mode="w") as fp:
            fp.write(self.__encode(nonce).decode())
