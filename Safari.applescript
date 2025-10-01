#!/usr/bin/env osascript

on openPrivateBrowsingWindow(urlToOpen)
  tell application "Safari"
    activate

    tell application "System Events"
      click menu item "New Private Window" of Â
        menu "File" of menu bar 1 of Â
        application process "Safari"
    end tell

    -- The frontmost window is the private Browsing window that just got
    -- opened -- change the URL to the one we want to open.
    tell window 1 to set properties of current tab to {URL:urlToOpen}
  end tell
end openPrivateBrowsingWindow

on run argv
  openPrivateBrowsingWindow("https://stackoverflow.com/")
end run