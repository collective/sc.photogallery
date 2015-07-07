*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description
@{images} =  640px-Mandel_zoom_00_mandelbrot_set.jpg  640px-Mandel_zoom_04_seehorse_tail.jpg  640px-Mandel_zoom_06_double_hook.jpg  640px-Mandel_zoom_07_satellite.jpg  640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Goto Homepage

    Create  Título  Descrição
    Update
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

    # Adding some images
    : FOR  ${image}  IN  @{images}
    \  Open Add New Menu
    \  Click Link  css=a#image
    \  Page Should Contain  Add Image
    \  Choose File  css=#image_file  /tmp/${image}
    \  Click Button  Save
    \  Page Should Contain  Changes saved
    \  Click Link  link=${title}

Update
    Click Link  link=Edit
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
