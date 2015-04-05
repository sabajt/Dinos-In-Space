"""
    endingDino.py
    the flashing dino that appears during games ending run state
"""
import pygame
import fpsSwitch

FLASH_DELAY = 3
ALPHA = 100

class EndingDino(pygame.sprite.Sprite):

    def __init__(self, image, center):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.flashDelay = FLASH_DELAY
        if fpsSwitch.FPSSwitch._fps == 60:
            self.flashDelay *= 2
        self.flashTick = self.flashDelay

    def updateEnding(self): # for identification by Game.endPuzzle()
        pass

    def update(self):
        self.flashTick -= 1
        if self.flashTick <= 0:
            self.flashTick = self.flashDelay
            self.switchAlpha()

    def switchAlpha(self):
        if self.image.get_alpha() == ALPHA:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(ALPHA)
