"""
    snackPacket.py
    class for collected snack icon that follows dino to station after collection
"""
import pygame
import dinosInSpace
import infoGraphic56
import gfx56
import fpsSwitch

WHITE = (255,255,255)
BLACK = (0,0,0)
FONTCOLOR = BLACK
FONTSIZE = 16
RELATIVE_TO_DINO_CENTER = (-40,-40)
SCALESTEP = 2
SCALESTARTSIZE = (2,2)
BOUNCEMAX = 30 # size above 1x scale before image contracts
#SPINSTEP = 10

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:
            ImgLib.imgDict = {
                "SP_FRAME" : dinosInSpace.loadImage("packetFrame.png", "2X", (0,0)) # pygame.Surface((40,40))
            }
#            ImgLib.imgDict["SP_FRAME"].fill(WHITE)

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image, " + name + " not found"

def initImgLib():
    ImgLib()


class SnackPacket(pygame.sprite.Sprite):
    """ collected snack icon that follow dino to statoin after collection
        - can 'combine' with other packets to increase count
        - are only created if dino collides with a snack
    """
    packetList = []
    packetAtStation = {}

    def __init__(self, dino):
        pygame.sprite.Sprite.__init__(self)

        self.originalFrame = ImgLib.getImage("SP_FRAME")
        self.count = 1
        self.dino = dino
        self.image = self.renderCurrentCount()
        self.rect = self.image.get_rect()
        self.followDino()
        self.atStation = None
        self.isScalingIntoView = True
        self.isBouncing = False
        self.isSpinning = False
        self.bounceReset = False # switch for bounce interuption handling
        self.scaleStep = SCALESTEP
        self.scaleSize = SCALESTARTSIZE
#        self.spinDistance = 0
#        self.spinStep = SPINSTEP
        self.originalFrameSize = self.originalFrame.get_size()
        self.bounceMax = self.originalFrameSize[0] + BOUNCEMAX
        self.scaleDirection = 1 # 1 or -1 switch for self.bounce
        if fpsSwitch.FPSSwitch._fps == 60:
            self.scaleStep *= 2
#            self.spinStep *= 2

        SnackPacket.packetList.append(self)

    def renderCurrentCount(self):
        """ return image with current count """
        textSurface = infoGraphic56.TextObject("+ " + str(self.count), FONTSIZE, FONTCOLOR).image
        image = gfx56.centerBlit(self.originalFrame.copy(), textSurface)
        return image

    def update(self):
        if self.atStation:
            self.followStation()
        else:
            self.followDino()

        if self.isScalingIntoView:
            self.scaleIntoView()
        if self.isBouncing:
            self.bounce()
#        if self.isSpinning:
#            self.spin()

    def followDino(self):
        self.rect.center = (self.dino.rect.center[0] + RELATIVE_TO_DINO_CENTER[0], self.dino.rect.center[1] + RELATIVE_TO_DINO_CENTER[1])

    def followStation(self):
        self.rect.center = (self.atStation.rect.center[0] + RELATIVE_TO_DINO_CENTER[0], self.atStation.rect.center[1] + RELATIVE_TO_DINO_CENTER[1])

    def addCount(self, count=1):
        self.count += count
        self.image = self.renderCurrentCount()
        self.isBouncing = True
        self.bounceReset = True

    def hookToStation(self, station):
        self.dino = None
        if station in SnackPacket.packetAtStation:
            SnackPacket.packetAtStation[station].addCount(self.count)
            self.kill()
        else:
            SnackPacket.packetAtStation[station] = self
            self.atStation = station
            self.followStation()

#    def spin(self):
#        """ update callback
#            - spins image once
#        """
#        # increment spinDistance
#        self.spinDistance += self.spinStep
#
#        # ending condition
#        if self.spinDistance >= 360:
#            self.spinDistance = 0
#            self.image = pygame.transform.scale(self.originalFrame, self.scaleSize)
#            self.isSpinning = False
#        else:
#            image = self.originalFrame.copy()
#            if self.scaleSize != self.originalFrameSize:
#                image = pygame.transform.scale(self.originalFrame.copy(), self.scaleSize)
#            self.image = pygame.transform.rotate(image, self.spinDistance)



    def scaleIntoView(self):
        """ update callback
            - scales self.image up by self.scaleStep
            - when original image size is met, self.isScalingIntoView set to False
        """
        self.centerScale(self.scaleSize)
        self.scaleSize = (self.scaleSize[0] + self.scaleStep, self.scaleSize[1] + self.scaleStep)

        if self.scaleSize[0] >= self.originalFrameSize[0]:
            self.isScalingIntoView = False
            self.isBouncing = True

#        if self.scaleSize >= self.originalFrameSize:
#            center = self.rect.center
#            self.image = self.renderCurrentCount()
#            self.rect = self.image.get_rect()
#            self.rect.center = center
#            self.isScalingIntoView = False
#        else:
#            self.centerScale(self.scaleSize)
#            self.scaleSize = (self.scaleSize[0] + self.scaleStep, self.scaleSize[1] + self.scaleStep)

    def bounce(self):
        """ update callback
            - scales image up to bounce max, then down to original size
            - when original image size is met, self.isBouncing sets to False
        """
        # anything not following scaleIntoView resets the image in case of interuptions
        if self.bounceReset:
            center = self.rect.center
            self.image = self.renderCurrentCount()
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.scaleSize = self.originalFrameSize
            self.bounceReset = False
        # scale image
        else:
            self.centerScale(self.scaleSize)

        # bounce ending condition
        if self.scaleSize[0] < self.originalFrameSize[0]:
            center = self.rect.center
            self.image = self.renderCurrentCount()
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.scaleSize = self.originalFrameSize
            self.isBouncing = False
            self.scaleDirection = 1 # reset so can bounce again
        # bounce reaches changing point
        elif self.scaleSize[0] >= self.bounceMax:
            self.scaleDirection = -1

        # increment scaleSize based on direction
        self.scaleSize = (self.scaleSize[0] + self.scaleDirection * self.scaleStep, self.scaleSize[1] + self.scaleDirection * self.scaleStep)


    def centerScale(self, size):
        """ scale self.image in place from center """
        center = self.rect.center
        self.image = pygame.transform.scale(self.renderCurrentCount(), size)
        self.rect = self.image.get_rect()
        self.rect.center = center

    @staticmethod
    def wipe():
        for p in SnackPacket.packetList:
            p.kill()
        SnackPacket.packetList = []
        SnackPacket.packetAtStation = {}

    @staticmethod
    def quickReset():
        SnackPacket.wipe()


def quickReset():
    SnackPacket.quickReset()

def wipe():
    SnackPacket.wipe()


