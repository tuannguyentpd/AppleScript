#!/usr/bin/osascript

---set uiElems to entire contents
---log uiElems

# Click button on window of process on screen - Begin - OK
tell application "System Events" to tell application processes "Installer"
    if window "Install ESET Cyber Security Pro" exists then
        log "Found ESET Install UI"
        set installWindow to window "Install ESET Cyber Security Pro"
        tell installWindow
            activate
            click button "Allow" of sheet 1
            delay 1
            set uiElems to entire contents
            log uiElems
        end tell
    end if
end tell
# Click button on window of process on screen - End - OK

# Allow install - Begin
tell application "System Events"
    repeat 30 times
        try
            tell application processes "UserNotificationCenter"
                click button "OK" of window 1
                log "Clicked OK button"
                exit repeat
            end tell
        on error line number num
            log "Error number " & num
        end try
        delay  1
    end repeat
end tell
# Allow install - end

delay 3
tell application "System Events" to tell application processes "Installer"
    if window "Install ESET Cyber Security Pro" exists then
        log "Found ESET Install UI"
        set installWindow to window "Install ESET Cyber Security Pro"
        tell installWindow
            activate
            click button "Continue"
            delay 2
            click button "Continue"
            delay 2
            click button "Continue"
            delay 2
            click button "Agree" of sheet 1
            delay 5
            click button "Continue"
            delay 2
            click button "Continue"
            delay 2
            click button "Continue"

            delay 2
            click pop up button 1 of group 1
            delay 0.5
            click menu item "Enable ESET LiveGrid¨ feedback system (recommended)" of menu 1 of pop up button 1 of group 1
            delay 1
            click button "Continue"

            click pop up button 1 of group 1
            delay 0.5
            click menu item "Enable detection of potentially unwanted applications" of menu 1 of pop up button 1 of group 1
            delay 1
            click button "Continue"

            click button "Install"
            delay 3
            
            
            #set uiElems to entire contents of busy indicator 1 of group 1 of group 1
            #log uiElems
        end tell
    else
        log "No found main GUI"
    end if
end tell

delay 4
tell application "System Events" to tell application processes "SecurityAgent"
    activate
    delay 1
    (*set uiElems to entire contents
    log uiElems*)
    set value of text field 2 of window "Untitled" to "test"
    delay 1
    click button "Install Software" of window "Untitled"
end tell


tell application "System Events"
    activate
    repeat 360 times
        log "[Finding]: UserNotificationCenter"
        if application processes "UserNotificationCenter" exists then
            delay 1
            try
                if button "Open Security Preferences" of window 1 of application process "UserNotificationCenter" exists then
                    click button "Open Security Preferences" of window 1 of application process "UserNotificationCenter"
                    log "Found Open Security Preferences"
                    delay 10
                    exit repeat
                end if
            end try
        else
            delay 1
        end if
    end repeat
    delay 1
end tell


set myUserName to "test"
set myPassword to "test"

# General Access - Begin
(*if running of application "System Preferences" then
    try
        tell application "System Preferences" to quit
    on error
        do shell script "killall 'System Preferences'"
    end try
end if

repeat while running of application "System Preferences" is true
    delay 0.1
end repeat*)

tell application "System Preferences"
    activate
    reveal anchor "General" of pane "com.apple.preference.security"
end tell

tell application "System Events" to tell application process "System Preferences"
    repeat 10 times
        if exists window "Security & Privacy" then 
            exit repeat
        end if
        delay 1
    end repeat
    set security_window to window "Security & Privacy"
    tell security_window
        --- Unblock Setting - Begin
        delay 0.25
        repeat 10 times
            if exists button "Click the lock to make changes." then
                exit repeat
            end if
            delay 1
        end repeat
        if button "Click the lock to make changes." exists then
            click button "Click the lock to make changes."
            repeat until exists sheet 1
                delay 0.1
            end repeat
            delay 0.25
            tell sheet 1
                set value of text field 2 to myUserName
                set value of text field 1 to myPassword
                delay 0.25
                click button "Unlock"
                delay 2
            end tell
        end if
        --- Unblock Setting - End

        --- Allow access - Begin
        repeat 5 times
            log "[Finding]: tab group 1"
            if exists tab group 1 then
                log "=> Found tab group 1"

                tell tab group 1
                    log "[Finding]: button Details..."
                    #set uiElems to entire contents
                    #log uiElems

                    delay 1.5
                    --- Allow button - Begin
                    if button "Allow" exists then
                        log "=> Found button Allow"
                        click button "Allow"
                        log "=> Clicked button Allow"
                    --- Allow button - End
                    --- Detail button - many components - Begin
                    else if button "DetailsÉ" exists then
                        log "=> Found button Details..."
                        click button "DetailsÉ"
                        log "=> Clicked button Details..."

                        repeat 5 times
                            log "[Finding]: Sheet 1 of security window"
                            if exists sheet 1 of security_window then
                                log "=> Found sheet 1 of security_window"
                                tell sheet 1 of security_window
                                    set theTable to table 1 of scroll area 1
                                    tell theTable
                                        set myStr to "Clicked checkboxs:\n"
                                        set tableRowCount to row count
                                        repeat with i from 0 to tableRowCount
                                            set theCheckBox to checkbox 1 of UI element 1 of row i
                                            tell theCheckBox
                                                if not (its value as boolean) then 
                                                    click theCheckBox
                                                    set temp to value of static text of item 1 of UI element 1 of row i of theTable
                                                    set myStr to myStr & "\tChecked: " & temp & "\n"
                                                end if
                                            end tell
                                            delay 1
                                        end repeat
                                        log myStr
                                    end tell
                                    if button "OK" exists then
                                        click button "OK"
                                        log "clicked OK button"
                                    end if
                                end tell

                                exit repeat
                            end if
                            delay 0.5
                        end repeat
                    end if
                    --- Detail button - many componentsÊ- End
                end tell
                exit repeat
            end if
            delay 0.5
        end repeat

        #delay 1
        #set uiElems to entire contents
        #log uiElems
        --- Allow access - End
    end tell
end tell
# Close System Preferences
(*quit application "System Preferences"*)
log "General Access - Done"
# General Access - End
delay 7

# Allow Filter Network - Begin
tell application "System Events"
    repeat 15 times
        try
            tell application processes "UserNotificationCenter"
                click button "Allow" of window 1
                log "Clicked Allow button"
                exit repeat
            end tell
        on error line number num
            log "Error number " & num
        end try
        delay  1
    end repeat
end tell
# Allow Filter Network - end

# Full Disk Access - Begin
set nameOfRowToSelect to "Full Disk Access"

(*if running of application "System Preferences" then
    try
        tell application "System Preferences" to quit
    on error
        do shell script "killall 'System Preferences'"
    end try
end if

repeat while running of application "System Preferences" is true
    delay 0.1
end repeat*)

tell application "System Preferences"
    activate
    reveal anchor "Privacy" of pane "com.apple.preference.security"
end tell

tell application "System Events" to tell application process "System Preferences"
    repeat 10 times
        if exists window "Security & Privacy" then 
            exit repeat
        end if
        delay 1
    end repeat
    set security_window to window "Security & Privacy"
    tell security_window
        --- Switch to SecurityTab and goto FullDiskAccess - Begin
        keystroke "f" using command down
        keystroke tab
        delay 0.25

        select (first row of table 1 of scroll area 1 of tab group 1 whose value of static text of UI element 1 contains nameOfRowToSelect)
        --- Switch to SecurityTab and goto FullDiskAccess - End

        --- Unblock Setting - Begin
        delay 0.25
        repeat 10 times
            if exists button "Click the lock to make changes." then
                exit repeat
            end if
            delay 1
        end repeat
        if button "Click the lock to make changes." exists then
            click button "Click the lock to make changes."
            repeat until exists sheet 1
                delay 0.1
            end repeat
            delay 0.25
            tell sheet 1
                set value of text field 2 to myUserName
                set value of text field 1 to myPassword
                delay 0.25
                click button "Unlock"
                delay 2
            end tell
        end if
        --- Unblock Setting - End

        --- Allow access - Begin
        set theTable to table 1 of scroll area 1 of group 1 of tab group 1
        tell theTable
            set myStr to "Clicked checkboxs:\n"
            set tableRowCount to row count
            repeat with i from 0 to tableRowCount
                set theCheckBox to checkbox 1 of UI element 1 of row i
                tell theCheckBox
                    if not (its value as boolean) then 
                        click theCheckBox
                        set temp to value of static text of item 1 of UI element 1 of row i of theTable
                        set myStr to myStr & "\tChecked: " & temp & "\n"

                        repeat 7 times
                            ---log "loop to sheet"
                            if exists sheet 1 of security_window then
                                ---log "Existed sheet 1 -> need to click quit and reopen"
                                delay 0.25
                                click button "Quit & Reopen" of sheet 1 of security_window
                                delay 0.25
                                exit repeat
                            end if
                            delay 0.3
                        end repeat
                    end if
                end tell
            end repeat
            get myStr
        end tell
        --- Allow access - End
    end tell
end tell
# Close System Preferences
quit application "System Preferences"
log "FullDiskAccess - Done"
# Full Disk Access - End

# Init - Begin
tell application "System Events"
    repeat 10 times
        if application processes "ESET Cyber Security Pro" exists then
            tell application processes "ESET Cyber Security Pro"
                --- Click button "Start again"
                click button "Start Again" of window 1

                --- License
                repeat 100 times
                    if text field 1 of window 1 exists then
                        set value of text field 1 of window 1 to "NRSP-X9NA-KF2M-VJUC-BP7B"
                        delay 2
                        click button "Activate" of window 1
                        exit repeat
                    else
                        log "[Finding]: License text field"
                        delay 1
                    end if
                end repeat

                --- Click button "Done"
                repeat 60 times
                    try
                        if button "Done" of window 1 exists then
                            click button "Done" of window 1
                            exit repeat
                        end if
                    end try
                    log "[Finding]: button Done"
                    delay 2
                end repeat

                --- First update
                repeat 60 times
                    try
                        if button "Update" of scroll area 1 of window 1 exists then
                            click button "Update" of scroll area 1 of window 1
                            exit repeat
                        end if
                    end try
                    log "[Finding]: button Update"
                    delay 2
                end repeat

                repeat 600 times
                    if button "Abort" of window 1 exists then
                        log "[Updating]: button Abort exists"
                        delay 1
                    else
                        if static text "Update modules" of window 1 exists then
                            log "Update successful"
                        end if
                        exit repeat
                    end if
                end repeat

                set uiElems to entire contents
                log uiElems

                exit repeat
            end tell
        else
            log "[Finding]: ESET Cyber Security Pro"
        end if
        delay 2
    end repeat
end tell
# Init - End