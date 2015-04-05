"""
    bounceMask.py
    highlighting effect for arrow tiles
"""

import pygame
import dinosInSpace
import fpsSwitch

MASK_IMAGE_NAME = "bounceMask.png"
FLASHDELAY = 2
OFFSCREEN = (-200,-200)
ALPHA = 150

class BounceMask(pygame.sprite.Sprite):
    image = None

    def __init__(self, tile):
        pygame.sprite.Sprite.__init__(self)

        self.tile = tile
        if not BounceMask.image:
            BounceMask.image = dinosInSpace.loadImage(MASK_IMAGE_NAME, "2X", (0,0), ALPHA)
        self.image = BounceMask.image.copy()
        self.rect = self.image.get_rect()
        self.flashTick = 0
        self.FLASHDELAY = FLASHDELAY
        if fpsSwitch.FPSSwitch._fps == 60:
            self.FLASHDELAY *= 2

        self.CLASS = "BounceMask" # for compatability w/ StaticBlock

    def update(self):
        if self.flashTick > 0:
            self.flashTick -= 1
            self.rect.center = self.tile.rect.center
        else:
            self.rect.center = OFFSCREEN

    def flash(self):
        self.flashTick = self.FLASHDELAY
