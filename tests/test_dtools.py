"""Tests for the DTools Robot Framework library."""

import json
from datetime import datetime
from dtools.dtools import DTools


class TestDTools:
    """Test suite for DTools library."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dtools = DTools()

    def test_generate_random_string_default(self):
        """Test random string generation with default parameters."""
        result = self.dtools.generate_random_string()
        assert len(result) == 10
        assert result.isalpha()

    def test_generate_random_string_custom(self):
        """Test random string generation with custom parameters."""
        result = self.dtools.generate_random_string(5, "digits")
        assert len(result) == 5
        assert result.isdigit()

    def test_clean_string(self):
        """Test string cleaning functionality."""
        dirty_string = "  hello world  "
        result = self.dtools.clean_string(dirty_string)
        assert result == "helloworld"

    def test_extract_numbers_from_string(self):
        """Test number extraction from string."""
        text = "Price: $123.45, Tax: $12.34"
        result = self.dtools.extract_numbers_from_string(text)
        assert "123.45" in result
        assert "12.34" in result

    def test_get_current_timestamp(self):
        """Test current timestamp generation."""
        result = self.dtools.get_current_timestamp("%Y-%m-%d")
        # Should match today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")
        assert result == today

    def test_add_time_to_date(self):
        """Test adding time to a date."""
        result = self.dtools.add_time_to_date("2023-01-01", days=7)
        assert result == "2023-01-08"

    def test_generate_uuid(self):
        """Test UUID generation."""
        result = self.dtools.generate_uuid()
        assert len(result) == 36  # Standard UUID length with hyphens
        assert result.count('-') == 4

    def test_generate_random_email(self):
        """Test random email generation."""
        result = self.dtools.generate_random_email("test.com")
        assert "@test.com" in result
        assert len(result.split("@")[0]) == 8  # Username length

    def test_parse_json_string(self):
        """Test JSON string parsing."""
        json_string = '{"key": "value", "number": 42}'
        result = self.dtools.parse_json_string(json_string)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_convert_to_json_string(self):
        """Test converting data to JSON string."""
        data = {"key": "value", "number": 42}
        result = self.dtools.convert_to_json_string(data)
        parsed = json.loads(result)
        assert parsed == data

    def test_get_json_value(self):
        """Test getting value from JSON using dot notation."""
        data = {"user": {"profile": {"name": "John"}}}
        result = self.dtools.get_json_value(data, "user.profile.name")
        assert result == "John"

    def test_validate_email_format_valid(self):
        """Test email validation with valid email."""
        result = self.dtools.validate_email_format("user@example.com")
        assert result is True

    def test_validate_email_format_invalid(self):
        """Test email validation with invalid email."""
        result = self.dtools.validate_email_format("invalid-email")
        assert result is False

    def test_validate_url_format_valid(self):
        """Test URL validation with valid URL."""
        result = self.dtools.validate_url_format("https://example.com")
        assert result is True

    def test_validate_url_format_invalid(self):
        """Test URL validation with invalid URL."""
        result = self.dtools.validate_url_format("not-a-url")
        assert result is False

    def test_remove_duplicates_from_list(self):
        """Test removing duplicates from list."""
        input_list = [1, 2, 2, 3, 3, 3, 4]
        result = self.dtools.remove_duplicates_from_list(input_list)
        assert result == [1, 2, 3, 4]

    def test_sort_list_by_key(self):
        """Test sorting list by key."""
        input_list = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
        result = self.dtools.sort_list_by_key(input_list, "name")
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"
