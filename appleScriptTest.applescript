#!/usr/bin/osascript

#if running of application "System Preferences" then
#    quit application "System Preferences"
#    delay 1
#end if
#tell application "System Preferences"
#    reveal pane id "com.apple.preference.expose"
#    delay 1
#    tell application "System Events"
#        tell group 2 of window 1 of application process "System Preferences"
#            tell checkbox "Automatically rearrange Spaces based on most recent use"
#                if value is equal to 0 then click it
#            end tell
#        end tell
#    end tell
#    quit
#end tell



tell application "System Preferences"
    activate
    --- Goto Full Disk Access
    reveal the anchor named "Privacy_AllFiles" in pane id "com.apple.preference.security"

    --- Wait for the window to appear
    repeat 15 times
        if window "Security & Privacy" exists then exit repeat
        delay 1
    end repeat

    tell the anchor named "Privacy_AllFiles" in current pane
        #get properties


        #set theCheckBox to checkbox "ESET Cyber Security Pro"
        #set theState to value of theCheckBox
        #if theState is 0 then click theCheckBox
    end tell


    (*reveal pane id "com.apple.preference.security"#set current pane to pane "com.apple.preference.security"
    delay 2
    tell application "System Events"
        click radio button "Privacy" of tab group 1 of window "Security & Privacy" of application process "System Preferences"
        delay 2
        #tell application "System Preferences" to get name of anchors of current pane #[OK] list all anchors
        tell application "System Preferences"
            reveal the anchor named "Privacy_AllFiles" in current pane
        end tell

        #get properties
    end tell
    *)
end tell














# [Work ok] - check and close System Preferences
#if running of application "System Preferences" then
#    quit application "System Preferences"
#    delay 1
#end

# [Work ok] - show taskview
#try
#    tell application id "com.apple.exposelauncher" to launch
#end try

