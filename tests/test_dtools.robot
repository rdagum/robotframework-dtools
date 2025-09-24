*** Settings ***
Documentation    Example Robot Framework test suite demonstrating DTools library usage
Library          dtools.DTools
Library          String
Library          Collections

*** Variables ***
${TEST_EMAIL}     test@example.com
${TEST_URL}       https://example.com

*** Test Cases ***
Test String Utilities
    [Documentation]    Test string manipulation keywords
    ${random_str}=     dtools.DTools.Generate Random String    8    letters
    Should Match Regexp    ${random_str}    ^[a-zA-Z]{8}$
    
    ${clean_str}=      Clean String    ${SPACE}${SPACE}hello world${SPACE}${SPACE}
    Should Be Equal    ${clean_str}    helloworld
    
    @{numbers}=        Extract Numbers From String    Price: $123.45, Tax: $12.34
    Should Contain     ${numbers}    123.45
    Should Contain     ${numbers}    12.34

Test Date and Time Utilities
    [Documentation]    Test date and time manipulation keywords
    ${timestamp}=      Get Current Timestamp    %Y-%m-%d
    Should Match Regexp    ${timestamp}    ^\\d{4}-\\d{2}-\\d{2}$
    
    ${new_date}=       Add Time To Date    2023-01-01    days=7
    Should Be Equal    ${new_date}    2023-01-08

Test Data Generation
    [Documentation]    Test data generation keywords
    ${uuid}=           Generate UUID    4
    Should Match Regexp    ${uuid}    ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
    
    ${email}=          Generate Random Email    test.com
    Should Contain     ${email}    @test.com
    @{username_parts}=  Split String    ${email}    @
    ${username}=       Get From List    ${username_parts}    0
    Length Should Be   ${username}    8

Test JSON Utilities
    [Documentation]    Test JSON manipulation keywords
    ${json_data}=      Convert To JSON String    {"name": "John", "age": 30}
    &{parsed}=         Parse JSON String    ${json_data}
    Should Be Equal    ${parsed.name}    John
    Should Be Equal As Numbers    ${parsed.age}    30
    
    ${nested_json}=    Convert To JSON String    {"user": {"profile": {"name": "Jane"}}}
    ${name}=           Get JSON Value    ${nested_json}    user.profile.name
    Should Be Equal    ${name}    Jane

Test Validation Utilities
    [Documentation]    Test validation keywords
    ${valid_email}=    Validate Email Format    user@domain.com
    Should Be True     ${valid_email}
    
    ${invalid_email}=  Validate Email Format    invalid-email
    Should Not Be True    ${invalid_email}
    
    ${valid_url}=      Validate URL Format    https://example.com
    Should Be True     ${valid_url}
    
    ${invalid_url}=    Validate URL Format    not-a-url
    Should Not Be True    ${invalid_url}

Test List Utilities
    [Documentation]    Test list manipulation keywords
    @{list_with_dupes}=    Create List    1    2    2    3    3    3    4
    @{unique_list}=        Remove Duplicates From List    ${list_with_dupes}
    @{expected_list}=      Create List    1    2    3    4
    Lists Should Be Equal  ${unique_list}    ${expected_list}
    
    @{dict_list}=          Create List    
    ...                    ${{{"name": "Bob", "age": 30}}}
    ...                    ${{{"name": "Alice", "age": 25}}}
    @{sorted_list}=        Sort List By Key    ${dict_list}    name
    ${first_name}=         Get From Dictionary    ${sorted_list[0]}    name
    ${second_name}=        Get From Dictionary    ${sorted_list[1]}    name
    Should Be Equal        ${first_name}    Alice
    Should Be Equal        ${second_name}    Bob

Test Suite Folder Tagging
    [Documentation]    Test suite folder tagging functionality
    # Test basic functionality
    @{tags}=           Set Suite Folders As Tags    C:\\tests\\feature\\subfolder\\test_suite.robot    C:\\tests
    @{expected}=       Create List    level0:feature    level1:subfolder    level2:test_suite
    Lists Should Be Equal    ${tags}    ${expected}
    
    # Test with Unix paths
    @{unix_tags}=      Set Suite Folders As Tags    /home/tests/api/login/auth_test.robot    /home/tests    delimiter=/
    @{expected_unix}=  Create List    level0:api    level1:login    level2:auth_test
    Lists Should Be Equal    ${unix_tags}    ${expected_unix}
    
    # Test with product folder
    @{product_tags}=   Set Suite Folders As Tags    C:\\tests\\myproduct\\feature\\test_suite.robot    C:\\tests    first_folder_is_product=True
    @{expected_product}=    Create List    product:myproduct    level0:feature    level1:test_suite
    Lists Should Be Equal    ${product_tags}    ${expected_product}
    
    # Test max levels
    @{limited_tags}=   Set Suite Folders As Tags    C:\\tests\\l1\\l2\\l3\\l4\\l5\\test.robot    C:\\tests    max_levels=3
    @{expected_limited}=    Create List    level0:l1    level1:l2    level2:l3
    Lists Should Be Equal    ${limited_tags}    ${expected_limited}
    
    # Test direct file in base path
    @{direct_tags}=    Set Suite Folders As Tags    C:\\tests\\test.robot    C:\\tests
    @{expected_direct}=    Create List    level0:test
    Lists Should Be Equal    ${direct_tags}    ${expected_direct}

Test Suite Folder Tagging Error Cases
    [Documentation]    Test error handling for suite folder tagging
    # Test empty suite source
    Run Keyword And Expect Error    ValueError: suite_source and base_path cannot be empty
    ...    Set Suite Folders As Tags    ${EMPTY}    C:\\tests
    
    # Test empty base path
    Run Keyword And Expect Error    ValueError: suite_source and base_path cannot be empty
    ...    Set Suite Folders As Tags    C:\\tests\\test.robot    ${EMPTY}
    
    # Test invalid base path
    Run Keyword And Expect Error    ValueError: suite_source must start with base_path
    ...    Set Suite Folders As Tags    C:\\other\\test.robot    C:\\tests
