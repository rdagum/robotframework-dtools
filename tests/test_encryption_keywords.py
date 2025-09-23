"""
Tests for the encryption keywords in the DTools library.
"""

import pytest
from cryptography.fernet import Fernet
from dtools.dtools import DTools


class TestEncryptionKeywords:
    """Test suite for encryption keywords in DTools."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.dtools = DTools()
        self.test_message = "Hello, Robot Framework! This is a test message."
        self.test_key = Fernet.generate_key().decode("utf-8")

    def test_generate_encryption_key(self):
        """Test key generation keyword."""
        key = self.dtools.generate_encryption_key()

        # Should be a valid base64 string
        assert isinstance(key, str)
        assert len(key) > 0

        # Should be usable as a Fernet key
        Fernet(key.encode("utf-8"))  # This will raise if invalid

    def test_encrypt_text_with_provided_key(self):
        """Test text encryption with provided key."""
        encrypted = self.dtools.encrypt_text(self.test_message, self.test_key)

        assert isinstance(encrypted, str)
        assert encrypted != self.test_message
        assert len(encrypted) > 0

    def test_decrypt_text_with_provided_key(self):
        """Test text decryption with provided key."""
        # First encrypt
        encrypted = self.dtools.encrypt_text(self.test_message, self.test_key)

        # Then decrypt
        decrypted = self.dtools.decrypt_text(encrypted, self.test_key)

        assert decrypted == self.test_message

    def test_encrypt_decrypt_roundtrip_with_provided_key(self):
        """Test full encrypt/decrypt cycle with provided key."""
        test_messages = [
            "Simple message",
            "Message with special chars: !@#$%^&*()",
            "Unicode message: café, naïve, résumé",
            "",  # Empty string
            "Very long message: " + "a" * 1000,
        ]

        for message in test_messages:
            encrypted = self.dtools.encrypt_text(message, self.test_key)
            decrypted = self.dtools.decrypt_text(encrypted, self.test_key)
            assert decrypted == message

    def test_encrypt_text_with_default_key_file(self):
        """Test that encryption works with default key file if it exists."""
        # This test will pass if the default key file exists
        # If it doesn't exist, it should raise a RuntimeError
        try:
            encrypted = self.dtools.encrypt_text(self.test_message)
            assert isinstance(encrypted, str)
            assert encrypted != self.test_message

            # Should be able to decrypt it too
            decrypted = self.dtools.decrypt_text(encrypted)
            assert decrypted == self.test_message
        except RuntimeError:
            # This is also acceptable if no default key file exists
            pytest.skip("No default encryption key file found")

    def test_decrypt_text_without_key_fails_gracefully(self):
        """Test that decryption without key/file fails gracefully."""
        with pytest.raises(RuntimeError, match="Decryption failed"):
            self.dtools.decrypt_text("invalid_encrypted_text")

    def test_decrypt_invalid_data_fails_gracefully(self):
        """Test that decryption of invalid data fails gracefully."""
        with pytest.raises(RuntimeError, match="Decryption failed"):
            self.dtools.decrypt_text("invalid_base64_data", self.test_key)

    def test_encrypt_with_invalid_key_fails_gracefully(self):
        """Test that encryption with invalid key fails gracefully."""
        with pytest.raises(RuntimeError, match="Encryption failed"):
            self.dtools.encrypt_text(self.test_message, "invalid_key")

    def test_different_keys_incompatible(self):
        """Test that different keys cannot decrypt each other's data."""
        key1 = self.dtools.generate_encryption_key()
        key2 = self.dtools.generate_encryption_key()

        # Encrypt with first key
        encrypted = self.dtools.encrypt_text(self.test_message, key1)

        # Try to decrypt with second key (should fail)
        with pytest.raises(RuntimeError, match="Decryption failed"):
            self.dtools.decrypt_text(encrypted, key2)

    def test_encryption_consistency(self):
        """Test that encryption produces different results each time (due to IV)."""
        encrypted1 = self.dtools.encrypt_text(self.test_message, self.test_key)
        encrypted2 = self.dtools.encrypt_text(self.test_message, self.test_key)

        # Should be different (due to random IV)
        assert encrypted1 != encrypted2

        # But both should decrypt to same message
        decrypted1 = self.dtools.decrypt_text(encrypted1, self.test_key)
        decrypted2 = self.dtools.decrypt_text(encrypted2, self.test_key)

        assert decrypted1 == self.test_message
        assert decrypted2 == self.test_message


if __name__ == "__main__":
    pytest.main([__file__])
