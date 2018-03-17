""" stickyCoord.py
    floating coordinate sprites
"""

import pygame
import infoGraphic56
import spriteBasic
import gfx56

COORDSIZE = 14
COORDCOLOR = (0,0,0)
BOXCOLOR_X = (173,90,250)
BOXCOLOR_Y = (250,90,173)

class StickyCoord(pygame.sprite.Sprite):
    """ a coordinate number sprite that moves with the editor along one edge
        - must specify vertical ('v') or horizontal ('h') edge stick location
    """

    def __init__(self, axis, number, startPos):
        pygame.sprite.Sprite.__init__(self)

        assert(axis == "x" or axis == "y")
        self.axis = axis

        # make image
        textImg = infoGraphic56.TextObject(str(number), COORDSIZE, COORDCOLOR).image
        if axis == "x":
            boxImg = spriteBasic.BasicRect((textImg.get_width()+2, textImg.get_height()+2), BOXCOLOR_X).image
        elif axis == "y":
            boxImg = spriteBasic.BasicRect((textImg.get_width()+2, textImg.get_height()+2), BOXCOLOR_Y).image
        self.image = gfx56.centerBlit(boxImg, textImg)
        self.rect = self.image.get_rect()

        if self.axis == "x":
            self.rect.midbottom = startPos
        elif self.axis == "y":
            self.rect.midleft = startPos

    def move(self, direction):
        """ override parent method to stick to one axis """
        step = 50
        x = self.rect.centerx
        y = self.rect.centery

        if self.axis == "x":
            if direction == "L":
                x += step
            elif direction == "R":
                x -= step
        elif self.axis == "y":
            if direction == "U":
                y += step
            elif direction == "D":
                y -= step

        self.rect.centerx = x
        self.rect.centery = y


if __name__ == '__main__':
    print("module intended for import only")
