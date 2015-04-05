"""
    sparkleTrail.py
    John Saba
"""
import pygame
import random

class SparkleTrail(pygame.sprite.Sprite):

    def __init__(self, unitSize, unitColor, bounds, frequency, fadeSpeed, spriteToTrail, virtualCenter=None, moving=None):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()

        self.unitSize = unitSize
        self.unitColor = unitColor
        self.rangeX = (-bounds[0]/2, bounds[0]/2)
        self.rangeY = (-bounds[1]/2, bounds[1]/2)

        self.frequency = frequency
        self.fadeSpeed = fadeSpeed
        self.spriteToTrail = spriteToTrail
        self.virtualCenter = virtualCenter
        self.newUnitTick = self.frequency
        self.moving = moving

        if self.virtualCenter:
            self.center = virtualCenter
        else:
            self.center = spriteToTrail.rect.center


    def update(self):
        if self.virtualCenter:
            self.center = self.virtualCenter
        else:
            self.center = self.spriteToTrail.rect.center
        self.newUnitTick -= 1
        newUnit = None
        if self.newUnitTick <= 0:
            self.newUnitTick = self.frequency
            newUnit = self.makeUnit()

        return newUnit

    def makeUnit(self):
        x = self.center[0] + random.randrange(self.rangeX[0], self.rangeX[1])
        y = self.center[1] + random.randrange(self.rangeY[0], self.rangeY[1])
        unitCenter = (x, y)
        newUnit = SparkleUnit(self.unitSize, self.unitColor, unitCenter, self.fadeSpeed, self.moving)

        return newUnit


class SparkleUnit(pygame.sprite.Sprite):

    def __init__(self, size, color, center, fadeSpeed, velocity=None):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.fadeSpeed = fadeSpeed
        self.velocity = velocity
        self.curAlpha = 255

    def update(self):
        if self.curAlpha - self.fadeSpeed <= 0:
            self.kill()
        else:
            self.curAlpha -= self.fadeSpeed
            self.image.set_alpha(self.curAlpha)

        if self.velocity:
            self.rect.centerx += self.velocity[0]
            self.rect.centery += self.velocity[1]