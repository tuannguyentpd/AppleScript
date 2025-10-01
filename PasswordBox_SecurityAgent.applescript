set myPassword to "test"
tell application "System Events" to tell application processes "SecurityAgent"
    activate
    delay 1
    ---set uiElems to entire contents
    ---log uiElems
    set value of text field 2 of window "Untitled" to myPassword
    delay 1
    click button "Install Software" of window "Untitled"
end tell