import os

def openSystemPreferences(tab='General', throw=True):
    res = True
    res = (0 == os.system('open "x-apple.systempreferences:com.apple.preference.security?' + tab + '"'))
    if not res and throw:
        raise NameError(f'Open tab "{tab}" of window "Security & Privacy" failed')
    return res

def closeSystemPrefernces():
    cmd = """
    osascript -e 'quit application "System Preferences"' 
    """
    return (0 == os.system(cmd))