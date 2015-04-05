"""
    simpleLabel
    independent label with text
    made for title label to hover above the pause menu because controlMenu56 is so fucked
"""

import pygame
import dinosInSpace
import spriteBasic
import infoGraphic56
import gfx56

WHITE = (255,255,255)
GREEN = (0,255,0)

LABEL_SIZE = (450, 60)
LABEL_COLOR = WHITE
LABEL_ALPHA = 255
LABEL_FONT_SIZE = 20
LABEL_FONT_COLOR = GREEN

class Label(pygame.sprite.Sprite):

    def __init__(self, text, center=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        frame = ImgLib.getImage("FRAME")
        text = infoGraphic56.TextObject(text, LABEL_FONT_SIZE, LABEL_FONT_COLOR).image.copy()
        self.image = gfx56.centerBlit(frame, text)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.visible = False
        self.alpha = 0
        self.image.set_alpha(self.alpha)

    def update(self):
        if self.visible:
            if self.alpha != 255:
                self.alpha = 255
                self.image.set_alpha(255)
        else:
            if self.alpha != 0:
                self.alpha = 0
                self.image.set_alpha(0)


class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):

        if not ImgLib.imgDict:
            # basic rect: size, color, topLeft=(0,0), rimSize=None, alpha=None, opaqueCenter=False
            _labelFrame = spriteBasic.BasicRect(LABEL_SIZE, LABEL_COLOR, (0,0), 2, LABEL_ALPHA, True).image.copy()

            ImgLib.imgDict = {
                "FRAME" : _labelFrame,
            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image, " + name + " not found"

def initImgLib():
    ImgLib()

if __name__ == '__main__':
    print "module intended for import only"
