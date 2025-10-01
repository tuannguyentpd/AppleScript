def asetPositionOfWindow(process, window, x=0, y=0, timeout=3, throw=True):
    location = '{'+str(x)+', '+str(y)+'}'
    window_ = window
    try:
        int(window)
    except:
        window_ = '"'+window+'"'
    
    cmd = f'''
            tell application "System Events"
                tell window {window_} of application process "{process}"
                    set position to {location}
                end tell
            end tell
            '''
    print(cmd)
    args = ['2', '2']
    from subprocess import Popen, PIPE

    code = False
    for i in range(timeout):
        print('\tTry time:', i)
        try:
            p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdout, stderr = p.communicate(cmd)
            if 0 == p.returncode:
                code = True
                break
        except:
            pass
        sleep(1)
    
    if not code and throw:
        raise NameError(f'Setposition for window "{window}" failed! Detail is "{stderr}"') 

    return code