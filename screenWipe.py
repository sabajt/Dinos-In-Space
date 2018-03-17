""" screenWipe.py
    screen wiping effect
"""

import pygame
import math
import dinosInSpace
import soundFx56

SPEED_DIVISOR = 15
WIDTH_TRANS_FIX = 0
HEIGHT_TRANS_FIX = 0
MIDBAR_WIDTH = 20

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:
            ImgLib.imgDict = {
                "CURSOR" : dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print("image, " + name + " not found")

def wipe(_fps, imageFrom, imageTo, direction):
    """ imageTo slides over imageFrom in the direction indicated
        - imageFrom should be last frame of captured screen from previous state
        - imageTo should first frame of capturd screen from new state
        - direction: "left", "right", "up", "down"

    """
##    soundFx56.SoundPlayer.requestSound("woosh_b")
    if not ImgLib.imgDict:
        ImgLib()

    if imageFrom:
        assert(direction == "left" or direction == "right" or direction == "up" or direction == "down")
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        if direction == "left" or direction == "right":
            speed = screen.get_width()/SPEED_DIVISOR + WIDTH_TRANS_FIX
        else:
            speed = screen.get_height()/SPEED_DIVISOR + HEIGHT_TRANS_FIX
        blitAt = 0
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        destValue = 0
        blitFix = 0
        cursor = Cursor()
        cursorGroup = pygame.sprite.GroupSingle(cursor)

        screen.blit(imageFrom, (0,0))
        cleanScreen = screen.copy() # needed for use with cursor

        if _fps == 30:
            speed *= 2

        if direction == "left":
            blitAt = screenWidth
            speed *= -1
        elif direction == "right":
            destValue = screenWidth
            blitFix = -screenWidth
        elif direction == "up":
            blitAt = screenHeight
            speed *= -1
        elif direction == "down":
            destValue = screenHeight
            blitFix = -screenHeight


        while math.fabs(destValue - blitAt) >= math.fabs(speed):
            clock.tick(_fps)
            blitAt += speed

            for event in pygame.event.get(): # must call for pygame to register mouse movement
                pass

            if direction == "left" or direction == "right":
                cleanScreen.blit(imageTo, (blitAt + blitFix, 0))
            else:
                cleanScreen.blit(imageTo, (0, blitAt + blitFix))

            screen.blit(cleanScreen, (0,0))
            cursorGroup.update()
            cursorGroup.draw(screen)
            pygame.display.update()
            cursorGroup.clear(screen, cleanScreen)

        screen.blit(imageTo, (0,0))

class Cursor(pygame.sprite.Sprite):
    """ for aesthetic purposes only during screen transition """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image  = ImgLib.getImage("CURSOR")
        self.rect   = pygame.rect.Rect((0,0,1,1))

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

