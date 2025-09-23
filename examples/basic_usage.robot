*** Settings ***
Documentation    Basic usage examples for DTools library
Library          dtools.DTools

*** Test Cases ***
Generate Test Data
    [Documentation]    Generate various types of test data
    ${user_id}=        Generate UUID
    ${username}=       Generate Random String    10    alphanumeric
    ${email}=          Generate Random Email    company.com
    ${password}=       Generate Random String    12    all
    
    Log    Generated test user data:
    Log    User ID: ${user_id}
    Log    Username: ${username}
    Log    Email: ${email}
    Log    Password: ${password}

Work With JSON Data
    [Documentation]    Example of JSON data manipulation
    # Create user data as dictionary
    &{user_data}=      Create Dictionary    
    ...                id=12345
    ...                name=John Doe
    ...                email=john@example.com
    ...                active=True
    
    # Convert to JSON string
    ${json_string}=    Convert To JSON String    ${user_data}    2
    Log    User data as JSON:\n${json_string}
    
    # Parse JSON and extract values
    &{parsed_data}=    Parse JSON String    ${json_string}
    ${user_name}=      Get JSON Value    ${parsed_data}    name
    ${user_email}=     Get JSON Value    ${parsed_data}    email
    
    Log    Extracted name: ${user_name}
    Log    Extracted email: ${user_email}

Validate Input Data
    [Documentation]    Example of data validation
    @{emails}=         Create List    
    ...                valid@example.com
    ...                another.valid+email@domain.co.uk
    ...                invalid-email
    ...                @invalid.com
    
    FOR    ${email}    IN    @{emails}
        ${is_valid}=   Validate Email Format    ${email}
        Run Keyword If    ${is_valid}
        ...    Log    ✓ Valid email: ${email}
        ...    ELSE
        ...    Log    ✗ Invalid email: ${email}
    END

Work With Dates
    [Documentation]    Example of date manipulation
    ${today}=          Get Current Timestamp    %Y-%m-%d
    ${next_week}=      Add Time To Date    ${today}    days=7
    ${next_month}=     Add Time To Date    ${today}    days=30
    ${deadline}=       Add Time To Date    ${today}    days=14    hours=9
    ...                input_format=%Y-%m-%d    output_format=%Y-%m-%d %H:%M
    
    Log    Today: ${today}
    Log    Next week: ${next_week}
    Log    Next month: ${next_month}
    Log    Project deadline: ${deadline}

Process Lists
    [Documentation]    Example of list processing
    @{raw_data}=       Create List    
    ...                apple    banana    apple    cherry    banana    date    apple
    
    Log    Original list: ${raw_data}
    
    @{unique_items}=   Remove Duplicates From List    ${raw_data}
    Log    Unique items: ${unique_items}
    
    # Create list of products with prices
    @{products}=       Create List
    ...                ${{{"name": "Apple", "price": 1.50}}}
    ...                ${{{"name": "Banana", "price": 0.80}}}
    ...                ${{{"name": "Cherry", "price": 3.00}}}
    
    @{sorted_by_name}=     Sort List By Key    ${products}    name
    @{sorted_by_price}=    Sort List By Key    ${products}    price    reverse=True
    
    Log    Products sorted by name: ${sorted_by_name}
    Log    Products sorted by price (desc): ${sorted_by_price}