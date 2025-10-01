def allowFulldiskAccess(throw=True):
    cmd = '''
    set myUserName to "test"
    set myPassword to "test"

    set nameOfRowToSelect to "Full Disk Access"

    if running of application "System Preferences" then
        try
            tell application "System Preferences" to quit
        on error
            do shell script "killall 'System Preferences'"
        end try
    end if

    repeat while running of application "System Preferences" is true
        delay 0.1
    end repeat

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
    #quit application "System Preferences"
    '''
    args = ['2', '2']
    from subprocess import Popen, PIPE

    res = False
    try:
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        # print(p.returncode, stdout, stderr)
        res = (0 == p.returncode)        
    except:
        pass
    
    if not res and throw:
        raise NameError('Grant access failed! Detail is ', (stderr)) 

    return res

def allowGeneralAccess(throw=True):
    cmd = '''
    set myUserName to "test"
    set myPassword to "test"

    set nameOfRowToSelect to "Full Disk Access"

    if running of application "System Preferences" then
        try
            tell application "System Preferences" to quit
        on error
            do shell script "killall 'System Preferences'"
        end try
    end if

    repeat while running of application "System Preferences" is true
        delay 0.1
    end repeat

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
                        else if button "Details…" exists then
                            log "=> Found button Details..."
                            click button "Details…"
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
                        --- Detail button - many components - End
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
    quit application "System Preferences"
    '''
    args = ['2', '2']
    from subprocess import Popen, PIPE

    res = False
    try:
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        # print(p.returncode, stdout, stderr)
        res = (0 == p.returncode)        
    except:
        pass
    
    if not res and throw:
        raise NameError('Grant access failed! Detail is ', (stderr)) 

    return res