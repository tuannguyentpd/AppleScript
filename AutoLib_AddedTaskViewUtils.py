import os
import json
import ctypes
import time
from pynput.keyboard import Key, Controller


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
##
##############
c_char_p, ctypes.c_char_p]
##############
''' Define API - End '''


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


def extractVirus(virus7z=home+"/Desktop/Services/virus.7z", location=home+"/Desktop/", password="test"):
    C_extractVirus(virus7z.encode('utf-8'),
                   location.encode('utf-8'), password.encode('utf-8'))


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


# def type(text):
#     keyboard.type(text)
#     return True


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

''' Custom API - End '''
