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
            --- set uiElems to entire contents
            --- log uiElems
        end try
    end repeat
end tell