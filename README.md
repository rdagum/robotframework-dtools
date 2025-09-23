# robotframework-dtools

A Robot Framework library providing general utilities for test automation.

## Overview

**dtools** is a comprehensive Robot Framework library that provides a collection of utility keywords for common tasks in test automation. It includes functionality for string manipulation, date/time operations, file operations, data generation, JSON handling, and validation utilities.

## Installation

### From PyPI (when published)
```bash
pip install robotframework-dtools
```

### From Source
```bash
git clone https://github.com/rdagum/rodotframework-dtools.git
cd rodotframework-dtools
pip install -e .
```

## Quick Start

Import the library in your Robot Framework test suite:

```robot
*** Settings ***
Library    dtools.DTools

*** Test Cases ***
Example Test
    ${random_string}=    Generate Random String    10    alphanumeric
    ${timestamp}=        Get Current Timestamp
    ${uuid}=            Generate UUID
    Log    Generated data: ${random_string}, ${timestamp}, ${uuid}
```

## Features

### String Utilities
- Generate random strings with customizable character sets
- Clean strings by removing unwanted characters
- Extract numbers from text using regex

### Date and Time Operations
- Get current timestamps in various formats
- Add time intervals to dates
- Date format conversion

### File Operations
- Create directories safely
- Get file sizes
- Calculate file hashes (MD5, SHA1, SHA256)

### Data Generation
- Generate UUIDs (version 1 and 4)
- Create random email addresses
- Generate test data with various patterns

### JSON Operations
- Parse JSON strings to dictionaries
- Convert data structures to JSON
- Extract values using dot notation paths

### Validation Utilities
- Validate email address formats
- Validate URL formats
- Custom validation patterns

### List Processing
- Remove duplicates while preserving order
- Sort lists by dictionary keys
- Advanced list manipulation

## Keywords Documentation

### String Keywords

#### Generate Random String
Generate a random string of specified length and character type.

**Arguments:**
- `length` (int): Length of string to generate (default: 10)
- `chars` (str): Character type - 'letters', 'digits', 'alphanumeric', 'all' (default: 'letters')

**Example:**
```robot
${random_str}=    Generate Random String    8    alphanumeric
```

#### Clean String
Remove specified characters from a string.

**Arguments:**
- `text` (str): String to clean
- `remove_chars` (str): Characters to remove (default: whitespace)

**Example:**
```robot
${clean}=    Clean String    "  hello world  "
# Result: "helloworld"
```

#### Extract Numbers From String
Extract all numeric values from a string.

**Arguments:**
- `text` (str): String to extract numbers from

**Example:**
```robot
@{numbers}=    Extract Numbers From String    Price: $123.45, Tax: $12.34
# Result: ['123.45', '12.34']
```

### Date and Time Keywords

#### Get Current Timestamp
Get the current date and time as a formatted string.

**Arguments:**
- `format_string` (str): Python datetime format string (default: "%Y-%m-%d %H:%M:%S")

**Example:**
```robot
${timestamp}=    Get Current Timestamp    %Y-%m-%d
```

#### Add Time To Date
Add a time interval to a given date.

**Arguments:**
- `date_string` (str): Input date as string
- `days` (int): Days to add (default: 0)
- `hours` (int): Hours to add (default: 0)
- `minutes` (int): Minutes to add (default: 0)
- `input_format` (str): Format of input date (default: "%Y-%m-%d")
- `output_format` (str): Format of output date (default: "%Y-%m-%d")

**Example:**
```robot
${new_date}=    Add Time To Date    2023-01-01    days=7
# Result: "2023-01-08"
```

### Data Generation Keywords

#### Generate UUID
Generate a UUID string.

**Arguments:**
- `version` (int): UUID version (1 or 4, default: 4)

**Example:**
```robot
${uuid}=    Generate UUID    4
```

#### Generate Random Email
Generate a random email address.

**Arguments:**
- `domain` (str): Email domain (default: "example.com")

**Example:**
```robot
${email}=    Generate Random Email    company.com
```

### JSON Keywords

#### Parse JSON String
Convert a JSON string to a Robot Framework dictionary.

**Arguments:**
- `json_string` (str): JSON string to parse

**Example:**
```robot
&{data}=    Parse JSON String    {"name": "John", "age": 30}
```

#### Convert To JSON String
Convert a data structure to JSON string.

**Arguments:**
- `data` (dict/list): Data to convert
- `indent` (int): JSON indentation (optional)

**Example:**
```robot
${json}=    Convert To JSON String    ${data}    2
```

#### Get JSON Value
Extract a value from JSON using dot notation.

**Arguments:**
- `json_data` (str/dict): JSON string or dictionary
- `json_path` (str): Path to value using dot notation

**Example:**
```robot
${name}=    Get JSON Value    ${json_data}    user.profile.name
```

### Validation Keywords

#### Validate Email Format
Check if an email address has valid format.

**Arguments:**
- `email` (str): Email address to validate

**Example:**
```robot
${is_valid}=    Validate Email Format    user@domain.com
```

#### Validate URL Format
Check if a URL has valid format.

**Arguments:**
- `url` (str): URL to validate

**Example:**
```robot
${is_valid}=    Validate URL Format    https://example.com
```

### List Keywords

#### Remove Duplicates From List
Remove duplicate items from a list while preserving order.

**Arguments:**
- `input_list` (list): List to process

**Example:**
```robot
@{unique}=    Remove Duplicates From List    ${list_with_duplicates}
```

#### Sort List By Key
Sort a list of dictionaries by a specific key.

**Arguments:**
- `input_list` (list): List of dictionaries to sort
- `key` (str): Dictionary key to sort by
- `reverse` (bool): Sort in descending order (default: False)

**Example:**
```robot
@{sorted}=    Sort List By Key    ${list_of_dicts}    name    reverse=True
```

## Examples

See the `examples/` directory for complete Robot Framework test suites demonstrating various use cases.

## Development

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/rdagum/rodotframework-dtools.git
cd rodotframework-dtools
```

2. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Running Tests

Run Python unit tests:
```bash
pytest tests/test_dtools.py -v
```

Run Robot Framework tests:
```bash
robot tests/test_dtools.robot
```

### Code Quality

Format code with Black:
```bash
black dtools/
```

Check code with Flake8:
```bash
flake8 dtools/
```

Type check with MyPy:
```bash
mypy dtools/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

- Create an issue for bug reports or feature requests
- Check the examples directory for usage patterns
- Refer to the Robot Framework documentation for general usage

## Version History

### 1.0.0
- Initial release
- String manipulation utilities
- Date and time operations
- File operations
- Data generation keywords
- JSON processing
- Validation utilities
- List processing functions