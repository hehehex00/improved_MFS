import unittest
from os.path import join, dirname, realpath
from pathlib import Path
from data_toolbox.utils.config_encryption.aes_manager import AESManager

class TestAESManager(unittest.TestCase):

    def test_encryption_decryption(self):
        try:
            # Arrange
            cwd = dirname(realpath(__file__))
            fake_key = join(cwd, "fakes/key.txt")
            fake_nonce = join(cwd, "fakes/nonce.txt")
            aes_manager = AESManager(fake_key, fake_nonce)
            expected = "Hello Panda"

            # Act
            aes_manager.ensure_key()
            aes_manager.ensure_nonce()
            encrypted = aes_manager.encrypt(expected)
            actual = aes_manager.decrypt(encrypted)

            # Assert
            self.assertEqual(expected, actual)

        finally:
            #Annihilate
            Path(fake_key).unlink(missing_ok=True)
            Path(fake_nonce).unlink(missing_ok=True)
            Path(fake_key).parent.rmdir()
