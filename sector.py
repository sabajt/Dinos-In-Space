"""
sector.py
Sector class: visual aid for unlocking levels at milestones - used in

areaselect
"""


import pygame
import spriteBasic
import scroller56
import areaSelect
import infoGraphic56
import gfx56
import math


class Sector(spriteBasic.BasicCircle):

    def __init__(self, curProfile, color, center, radius, width=0, toUnlock=0, counterPos=(0,0), hideBelow=0):
        spriteBasic.BasicCircle.__init__(self, radius, color, center, width)

        self.minSpeed       = areaSelect.SelectScreen.me.getMinSpeed()
        self.unlocked       = False
        self.radius         = radius
        self.color          = color
        self.hideBelow      = hideBelow

        if curProfile.getMapsComplete() >= toUnlock:
            self.counter    = None
            self.unlocked   = True
            self.image.set_alpha(0, pygame.RLEACCEL)
        else:
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

    def makeSatellites(self, satRadius, speed, count, shadeStep, withTailSize=1):
        """ should be called once for each sector after initialization """
        satallites	= []
        startTime   = 0
        color       = self.color
        rgbLim      = (False, False, False)

        while startTime <= count:
            if startTime == count or startTime == 0:
                satRadius *= withTailSize
            satallites.append(SectorSatellite(self, satRadius, speed, startTime, color))
            if startTime == 0:
                satRadius /= withTailSize
            startTime += 1
            color, rgbLim = gfx56.shadeColor(color, shadeStep, rgbLim)

        return satallites

    def positionCounter(self, counterPos):
        self.counter.rect.centerx = self.rect.centerx + counterPos[0]
        self.counter.rect.centery = self.rect.centery + counterPos[1]


class SectorSatellite(spriteBasic.BasicCircle):

    def __init__(self, masterCircle, satRadius, speed, startTime, color):
        spriteBasic.BasicCircle.__init__(self, satRadius, color, (0,0))

        self.radius         = masterCircle.radius
        self.speed          = speed
        self.time           = startTime
        self.masterCircle   = masterCircle

        ## hacky solution to growing time values - causes animation 'hiccup" at reset
        self.TIMELIM = 9999

    def update(self):
        (self.rect.centerx,
        self.rect.centery) = SectorSatellite.calculateOrbitStep(self.masterCircle.rect.center,
                                                                self.radius,
                                                                self.speed,
                                                                self.time)
        self.time += 1
        if self.time > self.TIMELIM:
            self.time = 0
            
        if self.masterCircle.hideBelow:
            
            if self.rect.centery > (self.masterCircle.rect.centery + self.masterCircle.hideBelow):
                self.image.set_alpha(0, pygame.RLEACCEL)
            else:
                self.image.set_alpha(255, pygame.RLEACCEL)

    @staticmethod
    def calculateOrbitStep(orbitCenter, radius, speed, time):
        x = orbitCenter[0] + radius * math.cos(speed * time)
        y = orbitCenter[1] + radius * math.sin(speed * time)

        return x, y

class SectorCounter(pygame.sprite.Sprite):


    def __init__(self, toUnlock):
        pygame.sprite.Sprite.__init__(self)

        self.image  = self.makeImage(toUnlock)
        self.rect   = self.image.get_rect()

    def makeImage(self, toUnlock):
        textSize    = 18
        textColor   = (0,0,0)
        frame       = spriteBasic.BasicRect((30,40), (255,255,255)).image
        count       = areaSelect.ProfileDelegate.curProfile.getNumTilUnlock(toUnlock) ######### get data !!!!!!!!!!!!!!!!!!!!!!!
        countSurf   = infoGraphic56.TextObject(str(count), textSize, textColor).image
        image       = gfx56.centerBlit(frame, countSurf)

        return image

    def move(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy
