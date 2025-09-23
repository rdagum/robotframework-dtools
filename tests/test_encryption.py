"""
Tests for the encryption module.

This module contains comprehensive tests for the Encryption class,
including testing direct key usage, file-based key loading, and error handling.
"""

import json
import pytest
import tempfile
import os
from unittest.mock import patch, mock_open
from cryptography.fernet import Fernet

from dtools.encryption import Encryption, Bcolors


class TestEncryption:
    """Test suite for the Encryption class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Generate a valid Fernet key for testing
        self.test_key = Fernet.generate_key()
        self.test_key_str = self.test_key.decode()
        self.test_message = "Hello, World! This is a test message."

    def test_init_with_direct_key_bytes(self):
        """Test initialization with direct key as bytes."""
        encryption = Encryption(encryption_key=self.test_key_str)
        assert encryption._encrypter is not None
        assert isinstance(encryption._key, bytes)

    def test_init_with_direct_key_string(self):
        """Test initialization with direct key as string."""
        encryption = Encryption(encryption_key=self.test_key_str)
        assert encryption._encrypter is not None
        assert isinstance(encryption._key, bytes)
        assert encryption._key == self.test_key

    def test_encrypt_decrypt_roundtrip_with_direct_key(self):
        """Test that encryption and decryption work correctly with direct key."""
        encryption = Encryption(encryption_key=self.test_key_str)

        # Encrypt the message
        encrypted = encryption.encrypt(self.test_message)
        assert isinstance(encrypted, bytes)
        assert encrypted != self.test_message.encode()

        # Decrypt the message
        decrypted = encryption.decrypt(encrypted)
        assert isinstance(decrypted, str)
        assert decrypted == self.test_message

    def test_encrypt_different_messages(self):
        """Test encryption of different types of messages."""
        encryption = Encryption(encryption_key=self.test_key_str)

        test_cases = [
            "Simple message",
            "Message with special chars: !@#$%^&*()",
            "Unicode message: café, naïve, résumé",
            "Number string: 123456789",
            "",  # Empty string
            "Very long message: " + "a" * 1000,
        ]

        for message in test_cases:
            encrypted = encryption.encrypt(message)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == message

    def test_encrypt_returns_bytes(self):
        """Test that encrypt method returns bytes."""
        encryption = Encryption(encryption_key=self.test_key_str)
        result = encryption.encrypt(self.test_message)
        assert isinstance(result, bytes)

    def test_decrypt_returns_string(self):
        """Test that decrypt method returns string."""
        encryption = Encryption(encryption_key=self.test_key_str)
        encrypted = encryption.encrypt(self.test_message)
        result = encryption.decrypt(encrypted)
        assert isinstance(result, str)

    def test_invalid_encryption_key(self):
        """Test initialization with invalid encryption key."""
        with pytest.raises(
            Exception
        ):  # Fernet will raise an exception for invalid keys
            Encryption(encryption_key="invalid_key")

    def test_decrypt_invalid_data(self):
        """Test decryption with invalid data."""
        encryption = Encryption(encryption_key=self.test_key_str)

        with pytest.raises(Exception):  # Should raise InvalidToken or similar
            encryption.decrypt(b"invalid_encrypted_data")

    def test_init_with_file_path_success(self):
        """Test initialization with valid key file."""
        # Create a temporary file with valid key data
        key_data = {"encryption_key": repr(self.test_key)}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(key_data, f)
            temp_file_path = f.name

        try:
            encryption = Encryption(key_file_path=temp_file_path)
            assert encryption._encrypter is not None

            # Test that it works
            encrypted = encryption.encrypt(self.test_message)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == self.test_message
        finally:
            os.unlink(temp_file_path)

    def test_init_with_file_path_missing_file(self):
        """Test initialization with missing key file."""
        with pytest.raises(FileNotFoundError, match="Encryption key file not found"):
            Encryption(key_file_path="/nonexistent/path/key.json")

    def test_init_with_file_path_missing_key(self):
        """Test initialization with file missing encryption_key."""
        # Create a temporary file without encryption_key
        key_data = {"other_key": "some_value"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(key_data, f)
            temp_file_path = f.name

        try:
            with pytest.raises(
                ValueError, match="encryption_key not found in configuration"
            ):
                Encryption(key_file_path=temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_init_with_file_path_invalid_json(self):
        """Test initialization with invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_file_path = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                Encryption(key_file_path=temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_get_default_key_path(self):
        """Test the default key path generation."""
        encryption = Encryption(encryption_key=self.test_key_str)
        default_path = encryption._get_default_key_path()

        assert "configuration" in default_path
        assert "key.json" in default_path
        assert os.path.isabs(default_path)  # Should be absolute path

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_init_default_file_mocked(self, mock_json_load, mock_file):
        """Test initialization with default file using mocks."""
        # Mock the JSON loading
        mock_json_load.return_value = {"encryption_key": repr(self.test_key)}

        encryption = Encryption()
        assert encryption._encrypter is not None

    def test_encryption_consistency(self):
        """Test that the same instance produces consistent results."""
        encryption = Encryption(encryption_key=self.test_key_str)

        # Encrypt the same message multiple times
        encrypted1 = encryption.encrypt(self.test_message)
        encrypted2 = encryption.encrypt(self.test_message)

        # Encrypted values should be different (due to random IV)
        assert encrypted1 != encrypted2

        # But both should decrypt to the same message
        assert encryption.decrypt(encrypted1) == self.test_message
        assert encryption.decrypt(encrypted2) == self.test_message

    def test_different_instances_same_key(self):
        """Test that different instances with same key can decrypt each other's data."""
        encryption1 = Encryption(encryption_key=self.test_key_str)
        encryption2 = Encryption(encryption_key=self.test_key_str)

        # Encrypt with first instance
        encrypted = encryption1.encrypt(self.test_message)

        # Decrypt with second instance
        decrypted = encryption2.decrypt(encrypted)

        assert decrypted == self.test_message

    def test_different_keys_incompatible(self):
        """Test that different keys cannot decrypt each other's data."""
        key1 = Fernet.generate_key().decode()
        key2 = Fernet.generate_key().decode()

        encryption1 = Encryption(encryption_key=key1)
        encryption2 = Encryption(encryption_key=key2)

        # Encrypt with first instance
        encrypted = encryption1.encrypt(self.test_message)

        # Try to decrypt with second instance (should fail)
        with pytest.raises(Exception):
            encryption2.decrypt(encrypted)


class TestBcolors:
    """Test suite for the Bcolors class."""

    def test_bcolors_constants(self):
        """Test that Bcolors class has all expected color constants."""
        expected_colors = [
            "HEADER",
            "OKBLUE",
            "OKCYAN",
            "OKGREEN",
            "WARNING",
            "FAIL",
            "ENDC",
            "BOLD",
            "UNDERLINE",
        ]

        for color in expected_colors:
            assert hasattr(Bcolors, color)
            assert isinstance(getattr(Bcolors, color), str)

    def test_bcolors_ansi_codes(self):
        """Test that Bcolors constants contain ANSI escape codes."""
        # All color codes should start with '\033['
        for attr_name in dir(Bcolors):
            if not attr_name.startswith("_"):
                attr_value = getattr(Bcolors, attr_name)
                assert attr_value.startswith(
                    "\033["
                ), f"{attr_name} should be an ANSI code"


class TestEncryptionIntegration:
    """Integration tests for the encryption module."""

    def test_key_generation_compatibility(self):
        """Test that generated Fernet keys work with the Encryption class."""
        # Generate a new key
        new_key = Fernet.generate_key()

        # Use it with Encryption class
        encryption = Encryption(encryption_key=new_key.decode())

        # Test encryption/decryption
        message = "Test message for new key"
        encrypted = encryption.encrypt(message)
        decrypted = encryption.decrypt(encrypted)

        assert decrypted == message

    def test_file_and_direct_key_equivalence(self):
        """Test that file-based and direct key initialization produce equivalent results."""
        test_key = Fernet.generate_key()
        test_message = "Equivalence test message"

        # Create temporary file
        key_data = {"encryption_key": repr(test_key)}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(key_data, f)
            temp_file_path = f.name

        try:
            # Initialize with file
            encryption_file = Encryption(key_file_path=temp_file_path)

            # Initialize with direct key
            encryption_direct = Encryption(encryption_key=test_key.decode())

            # Both should be able to encrypt/decrypt the same data
            encrypted_file = encryption_file.encrypt(test_message)
            encrypted_direct = encryption_direct.encrypt(test_message)

            # Cross-decrypt
            assert encryption_direct.decrypt(encrypted_file) == test_message
            assert encryption_file.decrypt(encrypted_direct) == test_message

        finally:
            os.unlink(temp_file_path)


if __name__ == "__main__":
    pytest.main([__file__])
