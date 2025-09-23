*** Settings ***
Documentation    Test cases for encryption keywords in DTools library
Library          dtools.DTools

*** Variables ***
${TEST_MESSAGE}      Hello, Robot Framework! This is a test message.
${UNICODE_MESSAGE}   café, naïve, résumé - Unicode test
${EMPTY_MESSAGE}     ${EMPTY}

*** Test Cases ***
Test Generate Encryption Key
    [Documentation]    Test that we can generate a new encryption key
    ${key}=    Generate Encryption Key
    Should Not Be Empty    ${key}
    Length Should Be       ${key}    44    # Fernet keys are 44 characters when base64 encoded

Test Encrypt And Decrypt Text With Generated Key
    [Documentation]    Test encryption and decryption with a generated key
    ${key}=             Generate Encryption Key
    ${encrypted}=       Encrypt Text    ${TEST_MESSAGE}    ${key}
    ${decrypted}=       Decrypt Text    ${encrypted}       ${key}
    Should Be Equal     ${decrypted}    ${TEST_MESSAGE}

Test Encrypt And Decrypt Unicode Text
    [Documentation]    Test encryption and decryption with Unicode characters
    ${key}=             Generate Encryption Key
    ${encrypted}=       Encrypt Text    ${UNICODE_MESSAGE}    ${key}
    ${decrypted}=       Decrypt Text    ${encrypted}          ${key}
    Should Be Equal     ${decrypted}    ${UNICODE_MESSAGE}

Test Encrypt And Decrypt Empty String
    [Documentation]    Test encryption and decryption of empty string
    ${key}=             Generate Encryption Key
    ${encrypted}=       Encrypt Text    ${EMPTY_MESSAGE}    ${key}
    ${decrypted}=       Decrypt Text    ${encrypted}        ${key}
    Should Be Equal     ${decrypted}    ${EMPTY_MESSAGE}

Test Encrypt Text With Default Key
    [Documentation]    Test encryption using default key file
    ${encrypted}=       Encrypt Text    ${TEST_MESSAGE}
    Should Not Be Empty    ${encrypted}
    Should Not Be Equal    ${encrypted}    ${TEST_MESSAGE}

Test Decrypt Text With Default Key
    [Documentation]    Test decryption using default key file
    ${encrypted}=       Encrypt Text    ${TEST_MESSAGE}
    ${decrypted}=       Decrypt Text    ${encrypted}
    Should Be Equal     ${decrypted}    ${TEST_MESSAGE}

Test Encryption Produces Different Results
    [Documentation]    Test that encryption produces different results each time (due to IV)
    ${key}=             Generate Encryption Key
    ${encrypted1}=      Encrypt Text    ${TEST_MESSAGE}    ${key}
    ${encrypted2}=      Encrypt Text    ${TEST_MESSAGE}    ${key}
    Should Not Be Equal    ${encrypted1}    ${encrypted2}
    
    # But both should decrypt to the same message
    ${decrypted1}=      Decrypt Text    ${encrypted1}    ${key}
    ${decrypted2}=      Decrypt Text    ${encrypted2}    ${key}
    Should Be Equal     ${decrypted1}    ${TEST_MESSAGE}
    Should Be Equal     ${decrypted2}    ${TEST_MESSAGE}

Test Decryption With Wrong Key Fails
    [Documentation]    Test that decryption fails with wrong key
    ${key1}=            Generate Encryption Key
    ${key2}=            Generate Encryption Key
    ${encrypted}=       Encrypt Text    ${TEST_MESSAGE}    ${key1}
    
    Run Keyword And Expect Error    Decryption failed:*
    ...    Decrypt Text    ${encrypted}    ${key2}

Test Encryption With Invalid Key Fails
    [Documentation]    Test that encryption fails with invalid key
    Run Keyword And Expect Error    Encryption failed:*
    ...    Encrypt Text    ${TEST_MESSAGE}    invalid_key

Test Decryption With Invalid Data Fails
    [Documentation]    Test that decryption fails with invalid encrypted data
    ${key}=             Generate Encryption Key
    Run Keyword And Expect Error    Decryption failed:*
    ...    Decrypt Text    invalid_encrypted_data    ${key}