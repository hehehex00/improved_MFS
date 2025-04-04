import unittest
from os.path import join, dirname, realpath
from pathlib import Path

from data_toolbox.utils.config_encryption.aes_manager import AESManager
from data_toolbox.utils.config_encryption.protected_config_reader import ProtectedConfigReader
from data_toolbox.utils.config_encryption.protected_config_writer import ProtectedConfigWriter


class TestProtectedConfigCreation(unittest.TestCase):

    def test_get_value(self):
        try:
            # Arrange
            cwd = dirname(realpath(__file__))
            fake_key = join(cwd, "fakes/key.txt")
            fake_nonce = join(cwd, "fakes/nonce.txt")
            fake_config = join(cwd, "fakes/config.ini")
            aes_manager = AESManager(fake_key, fake_nonce)
            writer = ProtectedConfigWriter(aes_manager)
            reader = ProtectedConfigReader(aes_manager)
            section = "SECTION"
            option = "option"
            expected = "Hello Panda"

            # Act
            writer.edit_or_create(fake_config)
            writer.set(section, option, expected)
            writer.write(fake_config)

            reader.read(fake_config)
            actual = reader.get(section, option)

            # Assert
            self.assertEqual(expected, actual)
        finally:
            # Annihilate
            Path(fake_key).unlink(missing_ok=True)
            Path(fake_nonce).unlink(missing_ok=True)
            Path(fake_config).unlink(missing_ok=True)
            Path(fake_key).parent.rmdir()
