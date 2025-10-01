import os
from time import sleep

def synchronousDatetime():
    cmd = 'echo test | sudo -S systemsetup -setusingnetworktime'
    for i in range(5):
        if 0 != os.system(cmd + ' off'):
            return False
        sleep(1)
        if 0 != os.system(cmd + ' on'):
            return False
        sleep(1)
    return True