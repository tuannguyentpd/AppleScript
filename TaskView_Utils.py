import os
from pynput.keyboard import Key, Controller



keyboard = Controller()

def showFocusWindow():
    cmd = """
    osascript -e 'tell application "System Events" to key code 125 using {control down}' 
    """
    return (0 == os.system(cmd))

def showTaskView():
    cmd = """
    osascript -e 'tell application "System Events" to key code 126 using {control down}' 
    """
    return (0 == os.system(cmd))

def focusWindow(img, attempts=3, similar=.9, throw=True):
    res = False
    if showFocusWindow():
        full_img_path = (img_path+'/'+img).encode('utf-8')
        for i in range(attempts*5):
            print(f'i = {i}')
            if C_find(full_img_path, similar, 1):#find(img, 1, attempts, throw=False):
                keyboard.press(Key.up)
                keyboard.release(Key.up)
                # sleep(0.5)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                res = True
                break
            
            # sleep(0.5)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
    
    if not res:
        showFocusWindow()
        if throw:
            raise NameError('Focus Windows (%s) failed' % (img))

    return res