
*** Settings ***
Library    iot.api.API


*** Variables ***
${UUID}         MOXA_123
${CHANNEL}      OTA_MOXA_123
${ARTIFACT}     moxa_34.swu


*** Test Cases ***
OTA Happy Flow
    [Setup]    Create Node With Endpoints

    ${node}=    Api Get Node By Uuid    ${UUID}
    Should Be Equal As Strings    ${node}[version]    33

    ${result}=    Api Post Version To Ota Channel    ${CHANNEL}    ${ARTIFACT}
    Should Be Equal As Integers    ${result}    200

    ${node}=    Api Get Node By Uuid    ${UUID}
    Should Be Equal As Strings    ${node}[version]    33

    Wait Until Keyword Succeeds    3x    100ms    Poll And Check Version

    [Teardown]    Api Clear Ota Channel    ${CHANNEL}    ${ARTIFACT}


*** Keywords ***
Create Node With Endpoints
    Init Node    ${UUID}    33
    Add Endpoint    EP1_001    EP1    ${UUID}    3000    1
    Add Endpoint    EP2_001    EP2    ${UUID}    3000    1
    Add Endpoint    CANARY_001    Canary_A    ${UUID}    4000    1

Poll And Check Version
    Api Tick Ota    ${CHANNEL}
    ${node}=    Api Get Node By Uuid    ${UUID}
    Should Be Equal As Strings    ${node}[version]    34
