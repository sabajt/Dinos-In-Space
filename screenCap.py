"""
    screenCap.py
    a module for saving surfaces as images into temporary file
    -- requires dataStorage

"""

import pygame
import dataStorage56

class ScreenCamera(object):

    def __init__(self):
        pass

    def takePicture(self, surface, sourceName, editOrPlay, scaleToOrBy=None):
        """ scaleToOrBy can be an int or float for ratio scale or custom tuple """
        assert(editOrPlay == "EDIT" or editOrPlay == "PLAY")

        newSurf = surface.copy()
        if scaleToOrBy:
            if type(scaleToOrBy) is int or type(scaleToOrBy) is float:
                newSurf = pygame.transform.smoothscale(newSurf, (int(newSurf.get_width()*scaleToOrBy), int(newSurf.get_height()*scaleToOrBy)))
            elif type(scaleToOrBy) is tuple:
                newSurf = pygame.transform.smoothscale(newSurf, scaleToOrBy)
            else:
                print("'scaleToOrBy' incorrectly specified, image is not being scaled ")

        dataStorage56.saveDynamicImage(newSurf, sourceName, editOrPlay)

