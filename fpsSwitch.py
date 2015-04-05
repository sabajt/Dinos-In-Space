"""
    fpsSwitch.py
    -frames per second control utility
    John Saba
"""

class FPSSwitch(object):
    _fps = 60

    @staticmethod
    def setFPS(fps):
        FPSSwitch._fps = fps