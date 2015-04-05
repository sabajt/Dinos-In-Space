""" 
    modeSwitch.py 
    access to bonus game modes
"""

MODES_DEFAULT = {
    "HATS" : 0, 
    "NYAN" : 0,
    "XTRA" : 0
}

class ModeSwitch(object):
    """ meant to be instantiated once from main function with no references """
    modes = None

    def __init__(self):
        if not ModeSwitch.modes:
            ModeSwitch.modes = MODES_DEFAULT.copy()
    
    @staticmethod
    def setMode(mode, state):
        assert mode in ModeSwitch.modes 
        assert state == 0 or state == 1
        ModeSwitch.modes[mode] = state

    @staticmethod
    def toggleMode(mode):
        if ModeSwitch.modes[mode] == 0:
            ModeSwitch.modes[mode] = 1
        else:
            ModeSwitch.modes[mode] = 0

    @staticmethod
    def resetModes():
        ModeSwitch.modes = MODES_DEFAULT.copy()
        