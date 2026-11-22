
*** Settings ***
Library    iot.api.API


*** Variables ***
${UUID}       MOXA_123
${SERIAL}     EP1_001


*** Test Cases ***
Endpoint DFU With Backlog
    [Setup]    Create Node With Endpoints

    ${result}=    Api Start Dfu    ${SERIAL}    2
    Should Be Equal    ${result}    ${False}

    ${ep}=    Api Get Endpoint By Serial    ${SERIAL}
    Should Be Equal As Strings    ${ep}[version]    1

    Api Drain Backlog    ${SERIAL}

    ${result}=    Api Start Dfu    ${SERIAL}    2
    Should Be Equal    ${result}    ${True}

    ${ep}=    Api Get Endpoint By Serial    ${SERIAL}
    Should Be Equal As Strings    ${ep}[version]    2

    Api Set Battery    ${SERIAL}    2400

    ${result}=    Api Start Dfu    ${SERIAL}    3
    Should Be Equal    ${result}    ${False}

    ${ep}=    Api Get Endpoint By Serial    ${SERIAL}
    Should Be Equal As Strings    ${ep}[version]    2


*** Keywords ***
Create Node With Endpoints
    Init Node    ${UUID}    33
    Add Endpoint    EP1_001    EP1    ${UUID}    3000    1    5
    Add Endpoint    EP2_001    EP2    ${UUID}    3000    1
    Add Endpoint    CANARY_001    Canary_A    ${UUID}    4000    1
