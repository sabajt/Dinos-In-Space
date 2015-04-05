"""
    sector.py
    Sector class: visual aid for unlocking levels at milestones - used in areaselect
"""

import pygame
import spriteBasic
import scroller56
import areaSelect
import infoGraphic56
import gfx56
import math

class Sector(spriteBasic.BasicCircle):

    def __init__(self, radius, color, center, width=0, toUnlock=0, counterPos=(0,0)):
        spriteBasic.BasicCircle.__init__(self, radius, color, center, width)

        self.minSpeed       = areaSelect.SelectScreen.me.getMinSpeed()
        self.unlocked       = False
        self.radius         = radius
        self.color          = color

        if areaSelect.ProfileDelegate.curProfile.getMapsComplete() >= toUnlock:
            self.counter    = None
            self.unlocked   = True

        else:
            self.satallites = None
            self.counter    = SectorCounter(toUnlock)

            self.positionCounter(counterPos)

    def update(self):
        self.setSpeed()

    def setSpeed(self):
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

        if self.counter:
            self.counter.move(dx, dy)


    def _makeSatellites(self, speed):
        satallites  = []
        timeStep    = 0
        x           = self.rect.centerx + self.radius
        y           = self.rect.centery


        self.radius * math.cos(speed * time)


        return satallites

    def getSatellites(self):
        return self.satallites

    def positionCounter(self, counterPos):
        self.counter.rect.centerx = self.rect.centerx + counterPos[0]
        self.counter.rect.centery = self.rect.centery + counterPos[1]

class SectorSatellite(pygame.sprite.Sprite):

    def __init__(self, masterCircle, startPoint, speed):
        pygame.sprite.Sprite.__init__(self)

        self.radius         = masterCircle.radius
        self.startPoint     = startPoint
        self.speed          = speed
        self.image          = pygame.Surface((10,10))
        self.rect           = self.image.get_rect()
        self.rect.center    = self.startPoint
        self.time           = 0
        self.orbitCenter    = masterCircle.rect.center

        self.image.fill((255,255,255))

    #        self.startpoint     = (self.radius, pygame.display.get_surface().get_height())

    def update(self):
        self.rect.centerx   = self.orbitCenter[0] + self.radius * math.cos(self.speed * self.time)
        self.rect.centery   = self.orbitCenter[1] + self.radius * math.sin(self.speed * self.time)

        self.time           += 1


class SectorCounter(pygame.sprite.Sprite):

    def __init__(self, toUnlock):
        pygame.sprite.Sprite.__init__(self)

        self.image  = self.makeImage(toUnlock)
        self.rect   = self.image.get_rect()

    def makeImage(self, toUnlock):
        textSize    = 18
        textColor   = (0,0,0)
        frame       = spriteBasic.BasicRect((30,40), (255,255,255)).image
        count       = areaSelect.ProfileDelegate.curProfile.getNumTilUnlock(toUnlock)
        countSurf   = infoGraphic56.TextObject(str(count), textSize, textColor).image
        image       = gfx56.centerBlit(frame, countSurf)

        return image

    def move(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy


