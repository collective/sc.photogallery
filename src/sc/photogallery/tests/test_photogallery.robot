*** Settings ***

Library  Selenium2Library  timeout=10 seconds  implicit_wait=5 seconds
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description

*** Test cases ***

Test CRUD
    Log in as site owner
    Go to homepage

    Create  Título  Descrição
    Update  Título  Descrição
    Delete

*** Keywords ***

Click Add Photo Gallery
    Open Add New Menu
    Click Link  css=a#photo-gallery
    Page Should Contain  Add Photo Gallery

Create
    [arguments]  ${title}  ${description}

    Click Add Photo Gallery
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Save
    Page Should Contain  Item created

Update
    [arguments]  ${title}  ${description}

    Click Link  link=Edit
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
