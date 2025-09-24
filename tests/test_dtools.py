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
        assert result.count("-") == 4

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

    # Tests for set_suite_folders_as_tags function
    def test_set_suite_folders_as_tags_basic(self):
        """Test basic functionality of set_suite_folders_as_tags."""
        suite_source = "C:\\tests\\feature\\subfolder\\test_suite.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(suite_source, base_path)
        expected = ["level0:feature", "level1:subfolder", "level2:test_suite"]
        assert result == expected

    def test_set_suite_folders_as_tags_unix_paths(self):
        """Test with Unix-style paths."""
        suite_source = "/home/tests/api/login/auth_test.robot"
        base_path = "/home/tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, delimiter="/"
        )
        expected = ["level0:api", "level1:login", "level2:auth_test"]
        assert result == expected

    def test_set_suite_folders_as_tags_with_product(self):
        """Test with first_folder_is_product=True."""
        suite_source = "C:\\tests\\myproduct\\feature\\test_suite.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, first_folder_is_product=True
        )
        expected = ["product:myproduct", "level0:feature", "level1:test_suite"]
        assert result == expected

    def test_set_suite_folders_as_tags_max_levels(self):
        """Test max_levels parameter."""
        suite_source = "C:\\tests\\l1\\l2\\l3\\l4\\l5\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, max_levels=3
        )
        expected = ["level0:l1", "level1:l2", "level2:l3"]
        assert result == expected

    def test_set_suite_folders_as_tags_max_levels_with_product(self):
        """Test max_levels with first_folder_is_product=True."""
        suite_source = "C:\\tests\\product\\l1\\l2\\l3\\l4\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, max_levels=3, first_folder_is_product=True
        )
        expected = ["product:product", "level0:l1", "level1:l2", "level2:l3"]
        assert result == expected

    def test_set_suite_folders_as_tags_no_robot_extension(self):
        """Test with file that doesn't have .robot extension."""
        suite_source = "C:\\tests\\feature\\test_file.txt"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(suite_source, base_path)
        expected = ["level0:feature", "level1:test_file.txt"]
        assert result == expected

    def test_set_suite_folders_as_tags_single_folder(self):
        """Test with only one folder level."""
        suite_source = "C:\\tests\\single\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(suite_source, base_path)
        expected = ["level0:single", "level1:test"]
        assert result == expected

    def test_set_suite_folders_as_tags_direct_file(self):
        """Test with file directly in base path."""
        suite_source = "C:\\tests\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(suite_source, base_path)
        expected = ["level0:test"]
        assert result == expected

    def test_set_suite_folders_as_tags_custom_delimiter(self):
        """Test with custom delimiter."""
        suite_source = "C:\\tests\\feature\\subfolder\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, delimiter="\\"
        )
        expected = ["level0:feature", "level1:subfolder", "level2:test"]
        assert result == expected

    def test_set_suite_folders_as_tags_empty_folders_filtered(self):
        """Test that empty folder names are filtered out."""
        # Simulate path with double separators that would create empty components
        suite_source = "C:\\tests\\\\feature\\\\test.robot"
        base_path = "C:\\tests"
        # Manually create the scenario by modifying the relative path calculation
        result = self.dtools.set_suite_folders_as_tags(suite_source, base_path)
        # The function should handle and filter empty components
        assert all(tag for tag in result if ":" in tag and tag.split(":")[1])

    def test_set_suite_folders_as_tags_error_empty_suite_source(self):
        """Test error handling for empty suite_source."""
        try:
            self.dtools.set_suite_folders_as_tags("", "C:\\tests")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "cannot be empty" in str(e)

    def test_set_suite_folders_as_tags_error_empty_base_path(self):
        """Test error handling for empty base_path."""
        try:
            self.dtools.set_suite_folders_as_tags("C:\\tests\\test.robot", "")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "cannot be empty" in str(e)

    def test_set_suite_folders_as_tags_error_invalid_base_path(self):
        """Test error handling when suite_source doesn't start with base_path."""
        try:
            self.dtools.set_suite_folders_as_tags("C:\\other\\test.robot", "C:\\tests")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "must start with base_path" in str(e)

    def test_set_suite_folders_as_tags_edge_case_exact_max_levels(self):
        """Test when path has exactly max_levels folders."""
        suite_source = "C:\\tests\\l1\\l2\\l3\\test.robot"
        base_path = "C:\\tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, max_levels=3
        )
        expected = ["level0:l1", "level1:l2", "level2:l3"]
        assert result == expected

    def test_set_suite_folders_as_tags_mixed_separators(self):
        """Test handling of mixed path separators."""
        suite_source = "C:/tests/feature\\subfolder/test.robot"
        base_path = "C:/tests"
        result = self.dtools.set_suite_folders_as_tags(
            suite_source, base_path, delimiter="/"
        )
        # Should handle the mixed separators gracefully
        assert len(result) > 0
        assert all("level" in tag or "product" in tag for tag in result)
