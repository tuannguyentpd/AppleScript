log "get every anchor of current pane"
tell application "System Preferences"
   -- set current pane to pane "com.apple.preference.displays"
   get every anchor of current pane
   -- or get everything
   entire contents
end tell
 
log "System Preferences: Generalreveal Main"
tell application "System Preferences"
   reveal anchor "Main" of pane id "com.apple.preference.general"
   -- reveal anchor "Handoff" of pane id "com.apple.preference.general"
   activate
end tell
 
delay 2
 
log "System Preferences: Desktop & Screen Saverreveal Desktop"
tell application "System Preferences"
   reveal anchor "DesktopPref" of pane id "com.apple.preference.desktopscreeneffect"
   activate
end tell
 
delay 2
 
log "System Preferences: Desktop & Screen Saverreveal Screen Saver"
tell application "System Preferences"
   reveal anchor "ScreenSaverPref" of pane id "com.apple.preference.desktopscreeneffect"
   activate
end tell
 
delay 2
 
log "System Preferences: Dock"
tell application "System Preferences"
   reveal anchor "Main" of pane id "com.apple.preference.dock"
   activate
end tell
 
delay 2
 
log "System Preferences: Mission Control"
tell application "System Preferences"
   reveal anchor "Spaces" of pane id "com.apple.preference.expose"
   activate
end tell
 
delay 2
 
tell application "System Preferences"
   reveal anchor "Region" of pane id "com.apple.Localization"
   activate
end tell
 
delay 2
 
log "System Preferences: Language & Region"
tell application "System Preferences"
   reveal anchor "Language" of pane id "com.apple.Localization"
   activate
end tell
 
delay 2
 
log "System Preferences: Security & Privacyreveal General"
tell application "System Preferences"
   reveal anchor "General" of pane id "com.apple.preference.security"
   activate
end tell
 
delay 2
 
log "System Preferences: Security & Privacyreveal FileVault"
tell application "System Preferences"
   reveal anchor "FDE" of pane id "com.apple.preference.security"
   activate
end tell
 
delay 2
 
log "System Preferences: Security & Privacyreveal Firewall"
tell application "System Preferences"
   reveal anchor "Firewall" of pane id "com.apple.preference.security"
   activate
end tell
 
delay 2
 
log "System Preferences: Security & Privacyreveal Privacy"
tell application "System Preferences"
   -- reveal anchor "Privacy_LinkedIn" of pane id "com.apple.preference.security"
   log "Location Services"
   reveal anchor "Privacy_LocationServices" of pane id "com.apple.preference.security"
   delay 3
   log "Location Services: System Servicesreveal Details"
   reveal anchor "Privacy_SystemServices" of pane id "com.apple.preference.security"
   delay 3
   tell application "System Events"
       tell process "System Preferences"
           click (keystroke return)
       end tell
   end tell
   delay 3
   log "Contacts"
   reveal anchor "Privacy_Contacts" of pane id "com.apple.preference.security"
   delay 3
   log "Calendars"
   reveal anchor "Privacy_Calendars" of pane id "com.apple.preference.security"
   delay 3
   log "Reminders"
   reveal anchor "Privacy_Reminders" of pane id "com.apple.preference.security"
   delay 3
   log "Camera"
   reveal anchor "Privacy_Camera" of pane id "com.apple.preference.security"
   delay 3
   log "Microphone"
   reveal anchor "Privacy_Microphone" of pane id "com.apple.preference.security"
   delay 3
   log "Accessibility"
   reveal anchor "Privacy_Accessibility" of pane id "com.apple.preference.security"
   delay 3
   log "Full Disk Access"
   reveal anchor "Privacy_AllFiles" of pane id "com.apple.preference.security"
   delay 3
   log "Analytics"
   reveal anchor "Privacy_Diagnostics" of pane id "com.apple.preference.security"
   activate
end tell
 
delay 2
 
log "System Preferences: Spotlight"
tell application "System Preferences"
   reveal anchor "searchResults" of pane id "com.apple.preference.spotlight"
   delay 3
   reveal anchor "privacy" of pane id "com.apple.preference.spotlight"
   activate
end tell
 
delay 2
 
log "System Preferences: Notification"
tell application "System Preferences"
   reveal anchor "Main" of pane id "com.apple.preference.notifications"
   activate
end tell
 
delay 2
 
log "System Preferences: Built-in Retina Display"
tell application "System Preferences"
   -- set current pane to pane "com.apple.preference.displays"
   reveal anchor "displaysDisplayTab" of pane id "com.apple.preference.displays"
   --> Built-in Retina Display: Display
    
   (*
       OLD maybe deprecated reveal anchor "displaysGeometryTab" of pane id "com.apple.preference.displays"
   *)
    
   delay 2
   reveal anchor "displaysColorTab" of pane id "com.apple.preference.displays"
   --> Built-in Retina Display: Colour
   delay 2
   reveal anchor "displaysNightShiftTab" of pane id "com.apple.preference.displays"
   --> Built-in Retina Display: Night Shift Tab
   activate
end tell
 
delay 2
 
log "System Preferences: Energy Saver"
-- anchor pane are switching based on power input
tell application "System Preferences"
   activate
   reveal anchor "Sleep" of pane id "com.apple.preference.energysaver"
   -- reveal anchor "Options" of pane id "com.apple.preference.energysaver"
   -- delay 3
   -- reveal anchor "PortableOptions" of pane id "com.apple.preference.energysaver"
   delay 3
   reveal anchor "Schedule" of pane id "com.apple.preference.energysaver"
   delay 3
   tell application "System Events"
       tell process "System Preferences"
           click (keystroke return)
       end tell
   end tell
end tell
 
delay 2
 
log "System Preferences: Keyboards"
tell application "System Preferences"
   activate
   reveal anchor "keyboardTab" of pane id "com.apple.preference.keyboard"
   delay 3
   reveal anchor "Text" of pane id "com.apple.preference.keyboard"
   delay 3
   reveal anchor "shortcutsTab" of pane id "com.apple.preference.keyboard"
   delay 3
   reveal anchor "InputSources" of pane id "com.apple.preference.keyboard"
   delay 3
   reveal anchor "Dictation" of pane id "com.apple.preference.keyboard"
   delay 3
   reveal anchor "keyboardTab_ModifierKeys" of pane id "com.apple.preference.keyboard"
   delay 3
   tell application "System Events"
       tell process "System Preferences"
           click (keystroke return)
       end tell
   end tell
end tell
 
delay 2
 
log "System Preferences: Mouse"
tell application "System Preferences"
   reveal anchor "mouseTab" of pane id "com.apple.preference.mouse"
   activate
end tell
 
delay 2
 
log "System Preferences: Trackpad"
tell application "System Preferences"
   reveal anchor "trackpadTab" of pane id "com.apple.preference.trackpad"
   activate
end tell
 
delay 2
 
log "System Preferences: Printers & Scanners"
tell application "System Preferences"
   reveal anchor "print" of pane id "com.apple.preference.printfax"
   -- reveal anchor "fax" of pane id "com.apple.preference.printfax"
   -- delay 3   
   -- reveal anchor "share" of pane id "com.apple.preference.printfax"
   -- delay 3
   -- reveal anchor "scan" of pane id "com.apple.preference.printfax"
   activate
end tell
 
delay 2
 
log "System Preferences: Sound"
tell application "System Preferences"
   reveal anchor "effects" of pane id "com.apple.preference.sound"
   delay 3
   reveal anchor "output" of pane id "com.apple.preference.sound"
   delay 3
   reveal anchor "input" of pane id "com.apple.preference.sound"
   activate
end tell
 
delay 2
 
log "System Preferences: Startup Disk"
tell application "System Preferences"
   reveal anchor "StartupSearchGroup" of pane id "com.apple.preference.startupdisk"
   activate
end tell
 
delay 2
 
log "System Preferences: iCloud"
tell application "System Preferences"
   reveal anchor "iCloud" of pane id "com.apple.preferences.icloud"
   activate
end tell
 
delay 2
 
log "System Preferences: Internet Accounts"
tell application "System Preferences"
   reveal anchor "InternetAccounts" of pane id "com.apple.preferences.internetaccounts"
   -- delay 3
   -- reveal anchor "com.apple.account.Google" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.aol" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.126" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.163" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.qq" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.Exchange" of pane id "com.apple.preferences.internetaccounts"
   -- reveal anchor "com.apple.account.Yahoo" of pane id "com.apple.preferences.internetaccounts"
   activate
end tell
 
delay 2
 
log "System Preferences: Software Update"
tell application "System Preferences"
   reveal anchor "SoftwareUpdate" of pane id "com.apple.preferences.softwareupdate"
   activate
end tell
 
delay 2
 
(*
log "System Preferences: Network"
tell application "System Preferences"
   -- reveal anchor "Wi-Fi" of pane id "com.apple.preference.network"
   -- reveal anchor "TCP/IP" of pane id "com.apple.preference.network"
   -- reveal anchor "DNS" of pane id "com.apple.preference.network"
   -- reveal anchor "WINS" of pane id "com.apple.preference.network"
   -- reveal anchor "802.1X" of pane id "com.apple.preference.network"
   -- reveal anchor "Proxies" of pane id "com.apple.preference.network"
   -- reveal anchor "VPN" of pane id "com.apple.preference.network"
   -- reveal anchor "PPP" of pane id "com.apple.preference.network"
   -- reveal anchor "Bluetooth" of pane id "com.apple.preference.network"
   -- reveal anchor "Advanced Ethernet" of pane id "com.apple.preference.network"
   -- reveal anchor "Advanced VPN" of pane id "com.apple.preference.network"
   -- reveal anchor "6to4" of pane id "com.apple.preference.network"
   -- reveal anchor "Bond" of pane id "com.apple.preference.network"
   -- reveal anchor "Ethernet" of pane id "com.apple.preference.network"
   -- reveal anchor "WWAN" of pane id "com.apple.preference.network"
   -- reveal anchor "Advanced Modem" of pane id "com.apple.preference.network"
   -- reveal anchor "Advanced Wi-Fi" of pane id "com.apple.preference.network"
   -- reveal anchor "Modem" of pane id "com.apple.preference.network"
   -- reveal anchor "VLAN" of pane id "com.apple.preference.network"
   -- reveal anchor "PPPoE" of pane id "com.apple.preference.network"
   -- reveal anchor "TCP/IP" of pane id "com.apple.preference.network"
   -- reveal anchor "FireWire" of pane id "com.apple.preference.network"
   -- reveal anchor "VPN on Demand" of pane id "com.apple.preference.network"
   activate
end tell
*)
 
 
log "System Preferences: Bluetooth"
tell application "System Preferences"
   reveal anchor "Main" of pane id "com.apple.preferences.Bluetooth"
   activate
end tell
 
delay 2
 
log "System Preferences: Extensions"
tell application "System Preferences"
   reveal anchor "Extensions" of pane id "com.apple.preferences.extensions"
   activate
end tell
 
delay 2
 
log "System Preferences: Sharing"
tell application "System Preferences"
   reveal anchor "Main" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_ScreenSharing" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_PersonalFileSharing" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_PrinterSharing" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_RemoteLogin" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_ARDService" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_RemoteAppleEvent" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Internet" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_BluetoothSharing" of pane id "com.apple.preferences.sharing"
   delay 2
   reveal anchor "Services_ContentCaching" of pane id "com.apple.preferences.sharing"
   -- reveal anchor "Services_DVDorCDSharing" of pane id "com.apple.preferences.sharing"
   -- reveal anchor "Services_WindowsSharing" of pane id "com.apple.preferences.sharing"
   activate
end tell
 
delay 2
 
log "System Preferences: Users & Groups"
tell application "System Preferences"
   reveal anchor "passwordPref" of pane id "com.apple.preferences.users"
   delay 3
   reveal anchor "startupItemsPref" of pane id "com.apple.preferences.users"
   delay 3
   reveal anchor "loginOptionsPref" of pane id "com.apple.preferences.users"
   -- delay 3
   -- reveal anchor "mobilityPref" of pane id "com.apple.preferences.users"
   activate
end tell
 
delay 2
 
log "System Preferences: Parental Controls"
tell application "System Preferences"
   reveal anchor "system" of pane id "com.apple.preferences.parentalcontrols"
   -- reveal anchor "logs" of pane id "com.apple.preferences.parentalcontrols"
   -- delay 3
   -- reveal anchor "filtering" of pane id "com.apple.preferences.parentalcontrols"
   -- delay 3
   -- reveal anchor "timeLimits" of pane id "com.apple.preferences.parentalcontrols"
   -- delay
   -- reveal anchor "emailChat" of pane id "com.apple.preferences.parentalcontrols"
   activate
end tell
 
delay 2
 
log "System Preferences: Siri"
tell application "System Preferences"
   reveal anchor "Siri" of pane id "com.apple.preference.speech"
   -- reveal anchor "Dictation" of pane id "com.apple.preference.speech"
   activate
end tell
 
delay 2
 
log "System Preferences: Date & Time"
tell application "System Preferences"
   reveal anchor "DateTimePref" of pane id "com.apple.preference.datetime"
   delay 3
   reveal anchor "TimeZonePref" of pane id "com.apple.preference.datetime"
   delay 3
   reveal anchor "ClockPref" of pane id "com.apple.preference.datetime"
   activate
end tell
 
delay 2
 
log "System Preferences: Time Machine"
tell application "System Preferences"
   reveal anchor "main" of pane id "com.apple.prefs.backup"
   activate
end tell
 
delay 2
 
log "System Preferences: Accessibility"
tell application "System Preferences"
   reveal anchor "General" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Seeing_VoiceOver" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Seeing_Zoom" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Seeing_Display" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "TextToSpeech" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Media_Descriptions" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Captioning" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Hearing" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "SpeakableItems" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Siri" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Keyboard" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Mouse" of pane id "com.apple.preference.universalaccess"
   delay 3
   reveal anchor "Switch" of pane id "com.apple.preference.universalaccess"
   delay 5
   -- reveal anchor "Dwell" of pane id "com.apple.preference.universalaccess"
   -- reveal anchor "Virtual_Keyboard" of pane id "com.apple.preference.universalaccess"
   activate
end tell
 
delay 2
 
tell application "System Preferences"
   set show all to true
end tell