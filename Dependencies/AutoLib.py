import os
import json
import ctypes
import time
from pynput.keyboard import Key, Controller
from applescript import *



home = os.path.expanduser("~")

img_path = home + "/Desktop/Services/product/images/"
lib_path = home + "/Desktop/Services/libUtils.dylib"

auto_lib = ctypes.cdll.LoadLibrary(lib_path)


''' Define API - Begin '''
##############
# UI lib
C_find = auto_lib.find
C_find.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_dragDrop = auto_lib.dragDrop
C_dragDrop.argtypes = [ctypes.c_char_p,
                       ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_paste = auto_lib.paste
C_paste.argtypes = [ctypes.c_char_p]
C_type = auto_lib.type
C_type.argtypes = [ctypes.c_char_p, ctypes.c_int]
C_doubleClick = auto_lib.doubleClick
C_doubleClick.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_click = auto_lib.click
C_click.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_rightClick = auto_lib.rightClick
C_rightClick.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_dragToXY = auto_lib.dragToXY
C_dragToXY.argtypes = [ctypes.c_char_p, ctypes.c_int,
                       ctypes.c_int, ctypes.c_float, ctypes.c_int]

C_moveMouse = auto_lib.moveMouse
C_moveMouse.argtypes = [ctypes.c_int, ctypes.c_int]

C_extractVirus = auto_lib.extractVirus
C_extractVirus.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# Pattern
C_getRegion = auto_lib.getRegion
C_getRegion.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_getRegion.restype = ctypes.c_char_p
C_getCenter = auto_lib.getCenter
C_getCenter.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_int]
C_getCenter.restype = ctypes.c_char_p
C_left = auto_lib.left
C_left.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_float, ctypes.c_int]
C_left.restype = ctypes.c_char_p
C_right = auto_lib.right
C_right.argtypes = [ctypes.c_char_p,
                    ctypes.c_int, ctypes.c_float, ctypes.c_int]
C_right.restype = ctypes.c_char_p
C_above = auto_lib.above
C_above.argtypes = [ctypes.c_char_p,
                    ctypes.c_int, ctypes.c_float, ctypes.c_int]
C_above.restype = ctypes.c_char_p
C_below = auto_lib.below
C_below.argtypes = [ctypes.c_char_p,
                    ctypes.c_int, ctypes.c_float, ctypes.c_int]
C_below.restype = ctypes.c_char_p
##
# Setting
C_setDelayAfterDrag = auto_lib.setDelayAfterDrag
C_setDelayAfterDrag.argtypes = [ctypes.c_int]
C_setDelayBeforeDrop = auto_lib.setDelayBeforeDrop
C_setDelayBeforeDrop.argtypes = [ctypes.c_int]

C_setDelayAfterDrag(300)
C_setDelayBeforeDrop(300)

''' Wrap API - Begin '''
##############
# UI lib


def moveMouse(x, y, throw=True):
    if False == C_moveMouse(x, y):
        if throw:
            raise NameError('Move to (%d, %d) failed' % (x, y))
        return False
    return True


def find(img, attempts=3, similar=.9, throw=True):
    if False == C_find((img_path+'/'+img).encode('utf-8'), similar, attempts):
        if throw:
            raise NameError('Find image %s is failed!' % (img))
        return False
    return True


def type(text, attempts=3, throw=True):
    if False == C_type(text.encode('utf-8'), attempts):
        if throw:
            raise NameError('Type %s is failed!' % (text))
        return False
    return True


def click(img, attempts=3, similar=.9, throw=True):
    if False == C_click((img_path+'/'+img).encode('utf-8'), similar, attempts):
        if throw:
            raise NameError('Click image %s is failed!' % (img))
        return False
    return True


def rightClick(img, attempts=3, similar=.9, throw=True):
    if False == C_rightClick((img_path+'/'+img).encode('utf-8'), similar, attempts):
        if throw:
            raise NameError('Click image %s is failed!' % (img))
        return False
    return True


def doubleClick(img, attempts=3, similar=.9, throw=True):
    if False == C_doubleClick((img_path+'/'+img).encode('utf-8'), similar, attempts):
        if throw:
            raise NameError('DoubleClick image %s is failed!' % (img))
        return False
    return True


def dragDrop(imgDrag, imgDrop, attempts=3, similar=.9, throw=True):
    if False == C_dragDrop((img_path+'/'+imgDrag).encode('utf-8'), (img_path+'/'+imgDrop).encode('utf-8'), similar, attempts):
        if throw:
            raise NameError('Drag image %s to %d is failed!' %
                            (imgDrag, imgDrop))
        return False
    return True


def move(imgDrag, x, y, attempts=3, similar=.9, throw=True):
    if False == C_dragToXY((img_path+'/'+imgDrag).encode('utf-8'), x, y, similar, attempts):
        if throw:
            raise NameError('Drag image %s to (%d, %d) is failed!' %
                            (imgDrag, x, y))
        return False
    return True
##############
''' Wrap API - End '''

''' API '''
# Settings


def setDelayBeforeDrop(time_in_milisecond):
    C_setDelayBeforeDrop(time_in_milisecond)


def setDelayAfterDrag(time_in_milisecond):
    C_setDelayAfterDrag(time_in_milisecond)
# Pattern


class Pattern:
    def __init__(self, img='', similar=.9, timeout=3):
        self.__x = 0
        self.__y = 0
        self.__h = 0
        self.__w = 0

        self.__similar = float(similar)
        self.__img = img
        self.__timeout = int(timeout)

    def setTimeout(self, timeout):
        self.__timeout = timeout
        return self

    def setSimilar(self, similar):
        self.__similar = similar
        return self

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getW(self):
        return self.__w

    def getH(self):
        return self.__h

    def find(self, throw=True):
        region_info = C_getRegion(
            (img_path+'/'+self.__img).encode('utf-8'), self.__similar, self.__timeout)
        region_info = json.loads(region_info)

        self.__x = region_info['x']
        self.__y = region_info['y']
        self.__w = region_info['width']
        self.__h = region_info['height']

        if True == throw:
            if self.__x == 0 and self.__y == 0:
                raise NameError(
                    '[Pattern] Find image %s is failed!' % (self.__img))

        return self

    def center(self):
        return self.__x+int(self.__w/2), self.__y-int(self.__h/2)

    def region(self):
        return self.__x, self.__y, self.__w, self.__h

    def left(self, range):
        c_x, c_y = self.center()
        return c_x-range, c_y

    def right(self, range):
        c_x, c_y = self.center()
        return c_x+range, c_y

    def below(self, range):
        c_x, c_y = self.center()
        return c_x, c_y+range

    def above(self, range):
        c_x, c_y = self.center()
        return c_x, c_y-range


def sleep(seconds):
    time.sleep(seconds)

C_mouseScroll = auto_lib.mouseScroll
C_mouseScroll.argtypes = [ctypes.c_int]


def scrollWheelMouse(range=1):
    C_mouseScroll(range)


def paste(text, attempts=3, throw=True):
    if False == C_paste(text.encode('utf-8')):
        if throw:
            raise NameError('Paste text %s is failed!' % (text))
        return False
    return True


''' Custom API - Begin '''
keyboard = Controller()


def closeFocusWindow():
    keyboard.press(Key.cmd_l)
    keyboard.press('w')
    keyboard.release(Key.cmd_l)
    keyboard.release('w')
    return True


def openSpotLight():
    keyboard.press(Key.cmd_l)
    keyboard.press(' ')
    keyboard.release(' ')
    keyboard.release(Key.cmd_l)
    return True


def openFrontAppPreferences():
    keyboard.press(Key.cmd_l)
    keyboard.press(',')
    keyboard.release(',')
    keyboard.release(Key.cmd_l)
    return True

def openAppFromSpotLight(search_string, app_image_recommened):
    openSpotLight()
    sleep(2)
    type(search_string)
    sleep(5)
    if click(app_image_recommened, throw=False):
        return True
    openSpotLight()
    return False


def type(text):
    keyboard.type(text)
    return True

''' Custom API - End '''


''' Applescript API - Begin '''
''' Applescript API - Begin '''
def aclick(process='System Preferences', object='button OK', timeout=3, index=None, throw=True):
    print(f'>> aclick "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('click', object, index=index):
            return True
        time.sleep(1)

    if throw:
        raise NameError('aclick %s  failed!' % (object))
    return False

def adoubleClick(process='System Preferences', object='button OK', timeout=3, index=None, throw=True):
    print(f'>> adoubleClick "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('doubleClick', object, index=index):
            return True
        time.sleep(1) 

    if throw:
        raise NameError('adoubleClick %s  failed!' % (object))
    return False

def arightClick(process='System Preferences', object='button OK', option=None, timeout=3, index=None, throw=True):
    print(f'>> arightClick "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('rightClick', object, option=option, index=index):
            return True
        time.sleep(1) 

    if throw:
        raise NameError('arightClick %s  failed!' % (object))
    return False

def afind(process='System Preferences', object='button OK', timeout=3, index=None, throw=True):
    print(f'>> afind "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('find', object, index=index):
            return True
        time.sleep(1) 

    if throw:
        raise NameError('afind %s  failed!' % (object))
    return False

def asetWindowToFront(process='System Preferences', windowsName=None, timeout=3, throw=True):
    print(f'>> asetWindowToFrount "{windowsName}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('toFront', objStr=windowsName, index=index):
            return True
        time.sleep(1) 

    if throw:
        raise NameError('asetWindowToFront %s  failed!' % (windowsName))
    return False

def adumpTree(process=None, file=None):
    if process == None:
        uiTree = UIElementsTree(process='System Preferences')
    else:
        uiTree = UIElementsTree(process=process)
    uiTree.addIgnoreProcess("Electron")

    if process == None:
        uiTree.buildTree(True)
    else:
        uiTree.buildTree(False)

    uiTree.dumpTree(file)

def afindAllElement(process=None, element='button'):
    if process == None:
        uiTree = UIElementsTree(process='System Preferences')
    else:
        uiTree = UIElementsTree(process=process)
    uiTree.addIgnoreProcess("Electron")

    if process == None:
        uiTree.buildTree(True)
    else:
        uiTree.buildTree(False)

    print(json.dumps(uiTree.findAll(element), indent=4))
''' Applescript API - End '''

def atype(process='System Preferences', object='button OK', text='test', timeout=3, index=None):
    print(f'>> Type "{text}" to "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('type', object, text=text, index=index):
            return True
        time.sleep(1) 
    return False

''' Grant Access - Begin '''
def aallowFulldiskAccess(throw=True):
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

    delay 10

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
            -- keystroke "f" using command down
            -- keystroke tab
            -- delay 0.25

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
                    set value of text field "Enter password"  to "test"
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

def aallowGeneralAccess(throw=True):
    cmd = '''
    set myUserName to "test"
    set myPassword to "test"

    set nameOfRowToSelect to "Full Disk Access"

    tell application "System Preferences"
        activate
        reveal anchor "General" of pane "com.apple.preference.security"
    end tell
    log "line 124"
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
                    set value of text field "Enter password"  to "test"
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
                        --- Detail button - many componentsÔøΩ- End
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
''' Grant Access - End '''

''' Datetime - Begin '''
def asynchronousDatetime():
    cmd = 'echo test | sudo -S systemsetup -setusingnetworktime'
    for i in range(5):
        if 0 != os.system(cmd + ' off'):
            return False
        sleep(1.5)
        if 0 != os.system(cmd + ' on'):
            return False
        sleep(1.5)
    return True
''' Datetime - End '''
