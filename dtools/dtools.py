"""
DTools - A Robot Framework library providing general utilities.

This library provides various utility keywords for common tasks in test automation,
including string manipulation, date/time operations, file operations, and more.
"""

import os
import re
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library(scope='GLOBAL', version='1.0.0')
class DTools:
    """DTools is a Robot Framework library that provides general utilities for test automation.

    This library includes keywords for:
    - String manipulation and validation
    - Date and time operations
    - File and directory operations
    - Data generation and validation
    - JSON operations
    - Random data generation
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    def __init__(self) -> None:
        """Initialize the DTools library."""
        self.builtin = BuiltIn()

    # String Utilities
    @keyword("Generate Random String")
    def generate_random_string(self, length: int = 10, chars: str = "letters") -> str:
        """Generate a random string of specified length.

        Args:
            length: Length of the string to generate (default: 10)
            chars: Type of characters to use ('letters', 'digits', 'alphanumeric', 'all')

        Returns:
            A random string of the specified length

        Examples:
            | ${random_str} | Generate Random String | 8 | letters |
            | ${random_num} | Generate Random String | 5 | digits |
        """
        import string
        import random

        if chars == "letters":
            char_set = string.ascii_letters
        elif chars == "digits":
            char_set = string.digits
        elif chars == "alphanumeric":
            char_set = string.ascii_letters + string.digits
        elif chars == "all":
            char_set = string.ascii_letters + string.digits + string.punctuation
        else:
            char_set = chars

        return ''.join(random.choice(char_set) for _ in range(int(length)))

    @keyword("Clean String")
    def clean_string(self, text: str, remove_chars: str = " \t\n\r") -> str:
        """Clean a string by removing specified characters.

        Args:
            text: The string to clean
            remove_chars: Characters to remove (default: whitespace)

        Returns:
            The cleaned string

        Example:
            | ${clean} | Clean String | " hello world " |
        """
        for char in remove_chars:
            text = text.replace(char, "")
        return text

    @keyword("Extract Numbers From String")
    def extract_numbers_from_string(self, text: str) -> List[str]:
        """Extract all numbers from a string.

        Args:
            text: The string to extract numbers from

        Returns:
            List of numbers found in the string

        Example:
            | @{numbers} | Extract Numbers From String | Price: $123.45, Tax: $12.34 |
        """
        return re.findall(r'\d+\.?\d*', text)

    # Date and Time Utilities
    @keyword("Get Current Timestamp")
    def get_current_timestamp(self, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get the current timestamp in specified format.

        Args:
            format_string: Python datetime format string

        Returns:
            Current timestamp as formatted string

        Example:
            | ${timestamp} | Get Current Timestamp | %Y-%m-%d |
        """
        return datetime.now().strftime(format_string)

    @keyword("Add Time To Date")
    def add_time_to_date(
            self,
            date_string: str,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            input_format: str = "%Y-%m-%d",
            output_format: str = "%Y-%m-%d"
    ) -> str:
        """Add time to a given date.
        Args:
            date_string: The date as a string
            days: Number of days to add
            hours: Number of hours to add
            minutes: Number of minutes to add
            input_format: Format of the input date string
            output_format: Format for the output date string

        Returns:
            New date as formatted string

        Example:
            | ${new_date} | Add Time To Date | 2023-01-01 | days=7 |
        """
        date_obj = datetime.strptime(date_string, input_format)
        new_date = date_obj + timedelta(days=days, hours=hours, minutes=minutes)
        return new_date.strftime(output_format)

    # File Utilities
    @keyword("Create Directory If Not Exists")
    def create_directory_if_not_exists(self, path: str) -> None:
        """Create a directory if it doesn't exist.

        Args:
            path: Path to the directory to create

        Example:
            | Create Directory If Not Exists | /path/to/directory |
        """
        os.makedirs(path, exist_ok=True)

    @keyword("Get File Size")
    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            file_path: Path to the file

        Returns:
            File size in bytes

        Example:
            | ${size} | Get File Size | /path/to/file.txt |
        """
        return os.path.getsize(file_path)

    @keyword("Calculate File Hash")
    def calculate_file_hash(self, file_path: str, algorithm: str = "md5") -> str:
        """Calculate hash of a file.

        Args:
            file_path: Path to the file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')

        Returns:
            Hash of the file as hexadecimal string

        Example:
            | ${hash} | Calculate File Hash | /path/to/file.txt | sha256 |
        """
        hash_func = getattr(hashlib, algorithm.lower())()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    # Data Generation Utilities
    @keyword("Generate UUID")
    def generate_uuid(self, version: int = 4) -> str:
        """Generate a UUID.

        Args:
            version: UUID version (1 or 4)

        Returns:
            UUID as string

        Example:
            | ${uuid} | Generate UUID | 4 |
        """
        if version == 1:
            return str(uuid.uuid1())
        else:
            return str(uuid.uuid4())

    @keyword("Generate Random Email")
    def generate_random_email(self, domain: str = "example.com") -> str:
        """Generate a random email address.

        Args:
            domain: Email domain (default: example.com)

        Returns:
            Random email address

        Example:
            | ${email} | Generate Random Email | testdomain.com |
        """
        username = self.generate_random_string(8, "alphanumeric").lower()
        return f"{username}@{domain}"

    # JSON Utilities
    @keyword("Parse JSON String")
    def parse_json_string(self, json_string: str) -> Any:
        """Parse a JSON string into a dictionary.

        Args:
            json_string: JSON string to parse

        Returns:
            Dictionary representation of the JSON

        Example:
            | &{data} | Parse JSON String | {"key": "value"} |
        """
        return json.loads(json_string)

    @keyword("Convert To JSON String")
    def convert_to_json_string(self, data: Union[Dict, List], indent: Optional[int] = None) -> str:
        """Convert data to JSON string.

        Args:
            data: Data to convert (dictionary or list)
            indent: JSON indentation (None for compact)

        Returns:
            JSON string representation

        Example:
            | ${json} | Convert To JSON String | ${data} | 2 |
        """
        return json.dumps(data, indent=indent)

    @keyword("Get JSON Value")
    def get_json_value(self, json_data: Union[str, Dict], json_path: str) -> Any:
        """Get value from JSON using dot notation path.

        Args:
            json_data: JSON string or dictionary
            json_path: Path to the value (e.g., 'user.name')

        Returns:
            Value at the specified path

        Example:
            | ${name} | Get JSON Value | ${json_data} | user.profile.name |
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        keys = json_path.split('.')
        result = data
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                raise ValueError(f"Path '{json_path}' not found in JSON data")
        return result

    # Validation Utilities
    @keyword("Validate Email Format")
    def validate_email_format(self, email: str) -> bool:
        """Validate email format using regex.

        Args:
            email: Email address to validate

        Returns:
            True if email format is valid, False otherwise

        Example:
            | ${is_valid} | Validate Email Format | user@domain.com |
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @keyword("Validate URL Format")
    def validate_url_format(self, url: str) -> bool:
        """Validate URL format using regex.

        Args:
            url: URL to validate

        Returns:
            True if URL format is valid, False otherwise

        Example:
            | ${is_valid} | Validate URL Format | https://example.com |
        """
        pattern = r'^https?:\/\/(?:[-\w.])+(?:\:[0-9]+)?(?:\/(?:[\w\/_.])*(?:\?(?:[\w&=%.]*))?(?:\#(?:[\w.]*))?)?$'
        return bool(re.match(pattern, url))

    # List Utilities
    @keyword("Remove Duplicates From List")
    def remove_duplicates_from_list(self, input_list: List[Any]) -> List[Any]:
        """Remove duplicates from a list while preserving order.

        Args:
            input_list: List to remove duplicates from

        Returns:
            List with duplicates removed

        Example:
            | @{unique} | Remove Duplicates From List | ${list_with_duplicates} |
        """
        seen = set()
        result = []
        for item in input_list:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @keyword("Sort List By Key")
    def sort_list_by_key(self, input_list: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sort a list of dictionaries by a specific key.

        Args:
            input_list: List of dictionaries to sort
            key: Key to sort by
            reverse: Sort in descending order if True

        Returns:
            Sorted list

        Example:
            | @{sorted} | Sort List By Key | ${list_of_dicts} | name | reverse=True |
        """
        return sorted(input_list, key=lambda x: x.get(key, ''), reverse=reverse)
