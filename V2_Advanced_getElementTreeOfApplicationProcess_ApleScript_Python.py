from subprocess import Popen, PIPE
import json
import time

class UIElementsTree:
    def __init__(self, application="System Events", process="System Preferences"):
        self.windows = None

        self.application = application
        self.process = process

        self.__tree = dict()

        self.__isSub = False
        self.__includeNode = None
        self.__action = False

        self.__objectFinder = None
        self.__founder = []

        self.__ignoreProcesses = {"Terminal"}

        self.__apllescript_object_types = ["application processes", "application process", "UI element", "window", "anchor", "scroll area", "tab group", "splitter group", "static text", "sheet", "table", "checkbox", "button", "text field", "group", "scroll bar", "toolbar", "image", "menu bar item", "menu bar", "menu item", "menu", "application", "list", "row", "column"]

    def addIgnoreProcess(self, process):
        self.__ignoreProcesses.add(process)

    def __initProcessNode(self, process=None):
        if process == None:
            process = self.process

        self.__tree[process] = dict()
        self.__tree[process]['info'] = dict()
        self.__tree[process]['info']['object'] = 'root'
        self.__tree[process]['info']['parent'] = None
        self.__tree[process]['children'] = dict()

    def getElementsList(self, process=None):
        if process == None:
            process = self.process
        res = {process: []}
        cmd = f'''
        tell application "{self.application}"
            tell application processes "{process}"
                set uiElems to entire contents
                repeat with uiElem in uiElems
                    log uiElem
                    log "<<<>>>"
                end repeat
            end tell
        end tell
        '''
        args = ['2', '2']
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        output = stderr.split('<<<>>>')
        temp = []
        for str_ in output:
            str__ = str_.strip('\n')
            if str__ != '':
                res[process].append(str__)
        return res

    def getObjectName(self, element, parentInfo=None):
        if parentInfo['parent'] == None:
            pos = element.find(' of ')
            return element[0:pos], element[pos+4:]
        else:
            parent = parentInfo['object'] + ' of ' + parentInfo['parent']
            pos = element.find(' of ' + parent)
            return element[0:pos], parent

        return None, None

    def __addSubElements(self, element, elementsTree):
        # if self.__action:
        #     return
        
        if len(elementsTree['children']) == 0:
            name, parent = self.getObjectName(element, elementsTree['info'])
            elementsTree['children'][element] = dict()
            elementsTree['children'][element]['info'] = dict()
            elementsTree['children'][element]['info']['object'] = name
            elementsTree['children'][element]['info']['parent'] = parent
            elementsTree['children'][element]['children'] = dict()
            self.__action = True
            return

        self.__action = False
        for element_ in elementsTree['children']:
            # Child node Recusively
            if element.find(element_) > 0:
                self.__addSubElements(element, elementsTree['children'][element_])
                break
        
        if not self.__action:
            name, parent = self.getObjectName(element, elementsTree['info'])
            elementsTree['children'][element] = dict()
            elementsTree['children'][element]['info'] = dict()
            elementsTree['children'][element]['info']['object'] = name
            elementsTree['children'][element]['info']['parent'] = parent
            elementsTree['children'][element]['children'] = dict()
            self.__action = True
            return

    def buildTree(self, allWindows=False):
        if allWindows:
            elementsList = self.getAllWindowsElementsList()
        else:
            elementsList = self.getElementsList()

        self.__tree = dict()
        for process in elementsList:
            self.__initProcessNode(process)
            for element in elementsList[process]:
                self.__isSub = False
                self.__includeNode = None
                self.__addSubElements(element, self.__tree[process])
                self.__action = False

        return self

    def getTree(self):
        return self.__tree

    def dumpTree(self, file=None):
        if file == None:
            print(json.dumps(self.__tree, indent=4))
        else:
            with open(file, 'w') as f:
                f.write(json.dumps(self.__tree, indent=4))

    def setObjFinder(self, objFinder):
        self.__objectFinder = objFinder
        return self

    def __find(self, objStr=None, elementsTree=None, process=None):
        if objStr == None:
            if self.__objectFinder == None:
                return None
            objStr = self.__objectFinder
        if process == None:
            process = self.process
        if elementsTree == None:
            elementsTree = self.__tree[process]

        if elementsTree['info']['object'] == objStr:
            return elementsTree['info']
        
        for child in elementsTree['children']:
            # print(f'[Goto child]: "{child}"')
            founder = self.__find(objStr, elementsTree['children'][child], process)
            if founder != None:
                return founder

        return None

    def find(self, objStr=None, process=None):
        if process != None:
            if process not in self.__tree:
                print(f'Process "{process}" does not exists')
                return None
            return self.__find(objStr=objStr, process=process)

        for process in self.__tree:
            # print(f'===> Start find in process "{process}"')
            foundItem = self.__find(objStr=objStr, process=process)
            if foundItem != None:
                return foundItem
        return None

    def __findAll(self, objStr=None, elementsTree=None, process=None):
        if objStr == None:
            if self.__objectFinder == None:
                return None
            objStr = self.__objectFinder
        if process == None:
            process = self.process
        if elementsTree == None:
            elementsTree = self.__tree[process]

        if elementsTree['info']['object'].find(objStr) != -1:
            self.__founder.append(elementsTree['info'])
        
        for child in elementsTree['children']:
            self.__findAll(objStr, elementsTree['children'][child], process)

    def findAll(self, objStr=None, process=None):
        res = dict()
        self.__founder = []

        if process != None:
            if process not in self.__tree:
                print(f'Process "{process}" does not exists')
            else:
                self.__findAll(objStr=objStr, process=process)
                if len(self.__founder) != 0:
                    res[process] = self.__founder.copy()
        else:
            for process in self.__tree:
                self.__findAll(objStr=objStr, process=process)
                if len(self.__founder) != 0:
                    res[process] = self.__founder.copy()
                self.__founder = []
        return res

    # ---- For all Processes Windows on current screen - Begin
    def getAllProcessWindows(self):
        res = dict()

        cmd = f'''
        tell application "System Events"
            repeat with theProcess in processes
                if not background only of theProcess then
                    tell theProcess
                        set processName to name
                        set theWindows to windows
                    end tell
                    set windowsCount to count of theWindows

                    log processName
                    log windowsCount
                    log theWindows
                    
                    ---say processName
                    ---say windowsCount as text
                    if windowsCount is greater than 0 then
                        ---repeat with theWindow in theWindows
                        ---    log "found a window of " & processName
                        ---end repeat
                    end if

                    log "<<<>>>"
                end if
            end repeat
        end tell
        '''

        args = ['2', '2']
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        processes = stderr.strip().split('<<<>>>')

        for process in processes:
            details = process.strip('\n').split('\n')
            if len(details) >= 2:
                process_name = details[0]
                res[process_name] = {"window_number": 0, "windows": []}
                res[process_name]["window_number"] = int(details[1])
                if res[process_name]["window_number"] > 0:
                    windows = details[2].split(',')
                    for window in windows:
                        res[process_name]['windows'].append(window.strip())

        return res

    def getAllWindowsElementsList(self):
        res = {}

        start = time.time()
        print(f'[Start - GetAllElement]:')
        allWindows = self.getAllProcessWindows()
        for process in allWindows:
            # Bypass some processes
            if process in self.__ignoreProcesses:
                continue

            if allWindows[process]["window_number"] > 0:
                sub_start = time.time()
                # print(f'Get Elements for process "{process}"')
                elements = self.getElementsList(process=process)
                for element in elements:
                    res[element] = elements[element]
                print(f'\t[Runtime - GetElement - {process}]: {time.time()-sub_start}')

        print(f'[Runtime - GetAllElement]: {time.time()-start}')
        return res
    # ---- For all Processes Windows on current screen - End

    def generateEventScript(self, event='click', objStr=None, option=None, parrentSig=None, x=0, y=0):
        object_ = self.find(objStr)
        if object_ == None:
            return None

        extendScript = ''''''
        if event == 'doubleClick':
            event = '''
                        (*set p to position
                        set s to size

                        set xCoordinate to (item 1 of p) + (item 1 of s) / 2
                        set yCoordinate to (item 2 of p) + (item 2 of s) / 2

                        click at {xCoordinate, yCoordinate}
                        delay 0.1
                        click at {xCoordinate, yCoordinate}*)
                        click
                        delay 0.1
                        click
                    '''
        elif event == 'rightClick':
            if option != None:
                event = f'''
                            perform action "AXShowMenu"
                            delay 0.3
                            keystroke "{option}"
                            delay 0.2
                            keystroke return
                        '''
            else:
                event = f'''
                        perform action "AXShowMenu"
                        delay 0.3
                    '''
        elif event == 'moveToXY':
            event = '''
                        set p to position
                        set s to size

                        set xCoordinate to (item 1 of p) + (item 1 of s) / 2
                        set yCoordinate to (item 2 of p) + (item 2 of s) / 2

                        click at {xCoordinate, yCoordinate}

                        key down 
                    '''
        elif event == 'toFront':
            event = '''
                    perform action "AXRaise"
                    '''
        elif event == 'find':
            event = '''
                    '''
        else:
            return None
            
        objectType, objectContent = self.analystObject(object_['object'])
        mainStrAction = objectType + ' ' + objectContent

        objectParent = self.analystSyntax(object_['parent'])
        while len(objectParent['parent']) != 0:
            mainStrAction += ' of ' + objectParent['type'] + ' ' + objectParent['content']
            objectParent = objectParent['parent']
            # if len(objectParent['parent']) == 0:
            #     break

        cmd = f'''
            tell application "System Events"
                tell application process "{self.process}"
                    activate
                    delay 0.3
                    set xCoordinate to null
                    set yCoordinate to null
                    tell {mainStrAction}
                        {event}
                    end tell
                    {extendScript}
                end tell
            end tell
            '''

        return cmd

    def analystObject(self, object):
        objectType, objectContent = None, None
        pos = -1
        for key in self.__apllescript_object_types:
            if object.find(key) == 0:
                objectType = key
                objectContent = object[len(key)+1:]
                if not objectContent.isnumeric():
                    objectContent = '"' + objectContent + '"'
                break
        return objectType, objectContent

    def analystSyntax(self, strCode):
        res = dict()
        currentNode = res

        tempPos = strCode.find(' of ')
        while tempPos != -1:
            objTemp = strCode[:tempPos]
            if self.find(objStr=objTemp) != None:
                objectType, objectContent = self.analystObject(objTemp)
                currentNode["parent"] = {}
                currentNode['type'] = objectType
                currentNode['content'] = objectContent
                currentNode = currentNode["parent"]

                strCode = strCode[tempPos+4:]
                tempPos = strCode.find(' of ')
            else:
                break
        
        objectType, objectContent = self.analystObject(strCode)
        currentNode["parent"] = {}
        currentNode['type'] = objectType
        currentNode['content'] = objectContent

        return res

    def sendEvent(self, event='click', objStr=None, option=None, x=0, y=0):
        res = False

        cmd = self.generateEventScript(event, objStr, option=option, x=x, y=y)
        if cmd == None:
            return False
            
        print(f'[Run Script]: "{cmd}"')
        args = ['2', '2']
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        print('Ouput is: ', stderr)
        print('Status code is: ', p.returncode)

        if p.returncode == 0:
            res = True

        return res

def click(process='System Preferences', object='button OK', timeout=3):
    print(f'>> Click "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('click', object):
            return True
        time.sleep(1)
        
    return False

def doubleClick(process='System Preferences', object='button OK', timeout=3):
    print(f'>> doubleClick "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('doubleClick', object):
            return True
        time.sleep(1)
        
    return False

def rightClick(process='System Preferences', object='button OK', option=None,timeout=3):
    print(f'>> rightClick "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('rightClick', object, option=option):
            return True
        time.sleep(1)
        
    return False

def find(process='System Preferences', object='button OK', timeout=3):
    print(f'>> Find "{object}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('find', object):
            return True
        time.sleep(1)
        
    return False

def moveToXY(process='System Preferences', object='button OK', x=0, y=0, timeout=3):
    print(f'>> moveToXY "{object}" ({x}, {y}) of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('moveToXY', objStr=object, x=x, y=y):
            return True
        time.sleep(1)
        
    return False

def setWindowToFront(process='System Preferences', windowsName=None, timeout=3):
    print(f'>> setWindowToFrount "{windowsName}" of process "{process}"')
    uiTree = UIElementsTree(process=process)

    for i in range(timeout):
        print('\tTry time:', i)
        uiTree.buildTree(False)
        if uiTree.sendEvent('toFront', objStr=windowsName):
            return True
        time.sleep(1)
        
    return False

''' Grant Access - Begin '''
def allowFulldiskAccess(throw=True):
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

def allowGeneralAccess(throw=True):
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
def synchronousDatetime():
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


import sys
if __name__ == '__main__':
    # print(rightClick('Finder', 'image Applications'))#, "Compress \\\"Applications\\\"", 5))
    # print(rightClick('Finder', 'image MacScan', "Open", 5))
    # print(rightClick('Finder', 'menu item Safari', "Open", 5))
    # print(click('System Preferences', 'button Sign In', 5))
    # print(click("System Preferences", "checkbox 1", 5))
    # print(doubleClick('System Preferences', 'button Sign In', 3))
    # print(doubleClick('Finder', 'image Applications'))
    # print(doubleClick('Finder', 'menu item Safari'))
    # print(doubleClick('Finder', 'image test.py'))

    # print(moveToXY('Finder', 'image MacScan', 10, 10))
    print(find('Finder', 'image MacScan'))

    # setWindowToFront('Finder', 'window MacScan')

    sys.exit(0)

    uiTree = UIElementsTree(process='System Preferences')#System Preferences, ESET Cyber Security Pro/esets_gui
    uiTree.addIgnoreProcess("Electron")

    # start_time = time.time()
    uiTree.buildTree(True)
    # print(f'[Runtime]: Built tree in {time.time()-start_time} second(s)')

    # # uiTree.sendEvent('click', 'button', '"Smart scan"', "")
    # # uiTree.sendEvent('click', 'static text', '\"Smart scan\"', 'window 1 of application process \"esets_gui\"')

    uiTree.dumpTree(file='/Users/test/Desktop/result.json')
    # # uiTree.setObjFinder('button 1')
    # print(json.dumps(uiTree.find("menu item Safari"), indent=4))

    # # print(uiTree.generateEventScript())
    # # print(json.dumps(uiTree.analystSyntax('static text Computer of scroll area 1 of window 1 of application process esets_gui'), indent=4))
    # # print(json.dumps(uiTree.analystObject('static text 47,46'), indent=4))

    # # uiTree.generateEventScript('click', 'button Smart scan')
    # print(uiTree.sendEvent('click', 'button Sign In'))

    # # print(json.dumps(uiTree.getAllProcessWindows(), indent=4))
    # # print(uiTree.getAllWindowsElementsList())
