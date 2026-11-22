
*** Settings ***
Library    iot.api.API


*** Variables ***
${UUID}         CASSIA_456
${CHANNEL}      OTA_CASSIA_456
${ARTIFACT}     moxa_34.swu


*** Test Cases ***
Bad Firmware OTA
    [Setup]    Create Cassia Node

    ${node}=    Api Get Node By Uuid    ${UUID}
    Should Be Equal As Strings    ${node}[version]    33

    ${result}=    Api Post Version To Ota Channel    ${CHANNEL}    ${ARTIFACT}
    Should Be Equal As Integers    ${result}    400

    ${node}=    Api Get Node By Uuid    ${UUID}
    Should Be Equal As Strings    ${node}[version]    33

    Should Not Be Empty    ${node}[last_error]
    Should Contain    ${node}[last_error]    mismatched artifact


*** Keywords ***
Create Cassia Node
    Init Node    ${UUID}    33
    Add Endpoint    EP1_C    EP1    ${UUID}    3000    1
    Add Endpoint    EP2_C    EP2    ${UUID}    3000    1
    Add Endpoint    CANARY_C    Canary_A    ${UUID}    4000    1
