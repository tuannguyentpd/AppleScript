def agetVersion(application, throw=False):
    cmd = f'''
    tell application "{application}"
        get version
    end tell
    '''
    args = ['2', '2']
    from subprocess import Popen, PIPE

    code = False
    res = ''
    try:
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        if 0 == p.returncode:
            res = stdout.strip()
            code = True
    except:
        pass
    
    if not code and throw:
        raise NameError(f'GetVersion for "{application}" failed! Detail is "{stderr}"') 

    return res
