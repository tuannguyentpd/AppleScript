from subprocess import Popen, PIPE
import json
import time

class UIElementsTree:
    def __init__(self, application="System Events", process="System Preferences"):
        self.windows = None

        self.application = application
        self.process = process

        self.__tree = dict()
        self.__tree['info'] = dict()
        self.__tree['info']['object'] = 'root'
        self.__tree['info']['parent'] = None
        self.__tree['children'] = dict()

        self.__isSub = False
        self.__includeNode = None
        self.__action = False

        self.__objectFinder = None
        self.__founder = []

    def getElementsList(self, process=None):
        if process == None:
            process = self.process
        res = []
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
                res.append(str__)
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

        for i in range(0, len(elementsList)):
            self.__isSub = False
            self.__includeNode = None
            self.__addSubElements(elementsList[i], self.__tree)
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

    def find(self, elementsTree=None):
        if elementsTree == None:
            elementsTree = self.__tree
        
        if self.__objectFinder == None:
            return None

        if elementsTree['info']['object'] == self.__objectFinder:
            return elementsTree['info']
        
        for child in elementsTree['children']:
            founder = self.find(elementsTree['children'][child])
            if founder != None:
                return founder

        return None

    def __findAll(self, elementsTree=None):
        if elementsTree == None:
            elementsTree = self.__tree
        
        if self.__objectFinder == None:
            return None

        if elementsTree['info']['object'].find(self.__objectFinder) != -1:
            self.__founder.append(elementsTree['info'])
        
        for child in elementsTree['children']:
            self.__findAll(elementsTree['children'][child])

    def findAll(self, elementsTree=None):
        self.__founder = []
        self.__findAll(elementsTree)
        return self.__founder

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
        res = []

        start = time.time()
        print(f'[Start - GetAllElement]:')
        allWindows = self.getAllProcessWindows()
        for process in allWindows:
            # Bypass some processes
            if process == "Terminal" or process == "Electron":
                continue

            if allWindows[process]["window_number"] > 0:
                sub_start = time.time()
                # print(f'Get Elements for process "{process}"')
                res.extend(self.getElementsList(process=process))
                print(f'\t[Runtime - GetElement - {process}]: {time.time()-sub_start}')

        print(f'[Runtime - GetAllElement]: {time.time()-start}')
        return res
    # ---- For all Processes Windows on current screen - End

    def sendEvent(self, event='click', object_='button', objectContent='"Continue"', applicationPath=''):
        res = False

        cmd = 'unknown'
        if event == 'click':
            cmd = f'''
            tell application "System Events"
                tell {applicationPath}
                    activate
                    delay 0.3
                    {event} {object_} {objectContent}
                end tell
            end tell
            '''
        
        print(f'[Run Script]: "{cmd}"')

        args = ['2', '2']
        p = Popen(['osascript', '-']+args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(cmd)
        output = stderr.split('<<<>>>')
        temp = []
        for str_ in output:
            str__ = str_.strip('\n')
            if str__ != '':
                res.append(str__)
        return res


if __name__ == '__main__':
    uiTree = UIElementsTree()#System Preferences, ESET Cyber Security Pro/esets_gui

    start_time = time.time()
    uiTree.buildTree(True)
    print(f'Runtime: {time.time()-start_time}')

    # uiTree.sendEvent('click', 'button', '"Smart scan"', "")
    # uiTree.sendEvent('click', 'static text', '\"Smart scan\"', 'window 1 of application process \"esets_gui\"')


    uiTree.dumpTree(file='/Users/test/Desktop/result.json')
    # print(uiTree.setObjFinder('Computer').findAll())

    # print(json.dumps(uiTree.getAllProcessWindows(), indent=4))
    # print(uiTree.getAllWindowsElementsList())