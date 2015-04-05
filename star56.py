""" star56

    class
        StarBuilder
        Sprite
            DistantStar
            ScrollingBkg
    function
        construct
        wipe

"""

import math
import pygame
import random
import dinosInSpace
import scroller56
import static56
import groupMods56
import radar56

MAX_NYANCATS = 4

class StarBuilder(object):
    """ create and scatter stars """

    def __init__(self, game, screen, size, step, color):

        points = self.getPoints(screen, step)
        starGroup = self.build(screen, size, points, color)
        game.addGroup(starGroup)

    def getPoints(self, screen, step):
        """ get points to place step^2 stars 'randomly' """

        starStepX = screen.get_width() / step
        starStepY = screen.get_height() / step
        starBufferX = 3 * starStepX / 4
        starBufferY = 3 * starStepY / 4
        points = []

        for stepx in range(step):

            for stepy in range(step):

                x = stepx * starStepX + random.randrange(-starBufferX, starBufferX)
                y = stepy * starStepY + random.randrange(-starBufferY, starBufferY)
                point = (x, y)
                points.append(point)

        duds = []   # remove all points created outside screen

        for point in points:

            for p in point:

                if p < 0:

                    duds.append(point)

        for dud in duds:

            if dud in points:

                points.remove(dud)

        return points

    def build(self, screen, size, points, color):
        """ create star sprites """

        starGroup = pygame.sprite.RenderUpdates()

        for point in points:

            star = DistantStar(screen, size, color, point)
            starGroup.add(star)

        return starGroup

class DistantStar(pygame.sprite.Sprite):
    """ super class for stars as backdrop, created by StarBuilder """

    def __init__(self, screen, size, color, point):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.setSize(size)
        self.color = color
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (point)

    def setSize(self, size):

        self.size = size

class ScrollingBkg(pygame.sprite.Sprite):
    """ parent class for scrolling background objects """

    imageDict = {}
    myGroup = groupMods56.SR_OrderedUpdates()

    def __init__(self, game, minSpeed, center, imageFile, scaleTo, getAt, spinRange):

        pygame.sprite.Sprite.__init__(self)
        self.minSpeed = minSpeed
        self.setImage(imageFile, scaleTo, getAt)
        self.rect = self.image.get_rect()
        self.rect.center = center

        if spinRange:

            self.hasSpin = True
            self.setSpin(spinRange)

        else:

            self.hasSpin = False

        ScrollingBkg.myGroup.add(self)

    def update(self):

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

        if self.hasSpin:

            self.spin()

    @staticmethod
    def wipe():

        ScrollingBkg.myGroup = groupMods56.SR_OrderedUpdates()

    def setImage(self, imageFile, scaleTo, getAt):

        load = dinosInSpace.loadImage

        if imageFile not in ScrollingBkg.imageDict:

            ScrollingBkg.imageDict[imageFile] = load(imageFile, scaleTo, getAt)

        image = ScrollingBkg.imageDict[imageFile].copy()

#        if scaleTo:
#
#            if scaleTo == "2X":
#
#                image = pygame.transform.scale2x(image)
#
#            else:
#
#                image = pygame.transform.scale(image, scaleTo)

#        if getAt:
#
#            col = image.get_at(getAt)
#            image.set_colorkey(col, pygame.RLEACCEL)

        self.original = image
        self.image = self.original.copy()

    def setSpin(self, range):
        """ initiate spin cycle """

        rangeStart = -range; rangeStop = range
        self.spinStep = 0

        while self.spinStep > -0.3 and self.spinStep < 0.3: # not too slow

            self.spinStep = random.uniform(rangeStart, rangeStop)

        self.spinDistance = 0

    def spin(self):
        """ rotate image """

        self.spinDistance += self.spinStep

        if self.spinStep > 0:

            if self.spinDistance >= 360:

                startHere = self.spinDistance - 360
                self.spinDistance = startHere   # reset spinDistance

        else:

            if self.spinDistance <= -360:

                starHere = self.spinDistance + 360
                self.spinDistance = starHere

        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.spinDistance)

class FloatingBkg(ScrollingBkg):
    """ ScrollingBkg object that has a floating speed as well """

    def __init__(self, game, minSpeed, center, imageFile, scaleTo, getAt, spinRange, floatSpeed):

        ScrollingBkg.__init__(self, game, minSpeed, center, imageFile, scaleTo, getAt, spinRange)
        self.setFramesToSkip(floatSpeed)

    def update(self):

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        scrollingDx = xSpeedRatio * self.minSpeed
        scrollingDy = ySpeedRatio * self.minSpeed

        if self.frameDelayX:

            doMove = self.skipFrames("x")

            if doMove:

                self.rect.centerx += scrollingDx + self.floatDx

            else:

                self.rect.centerx += scrollingDx

        else:

            self.rect.centerx += scrollingDx + self.floatDx

        if self.frameDelayY:

            doMove = self.skipFrames("y")

            if doMove:

                self.rect.centery += scrollingDy + self.floatDy

            else:

                self.rect.centerx += scrollingDy

        else:

            self.rect.centery += scrollingDy + self.floatDy

        if self.hasSpin:

            self.spin()

    def setFramesToSkip(self, floatSpeed):

        self.floatDx, self.floatDy = floatSpeed

        if self.floatDx != 0:

            self.framesToSkipX = 1 // self.floatDx

        else:

            self.framesToSkipX = 0

        if self.floatDy != 0:

            self.framesToSkipY = 1 // self.floatDy

        else:

            self.framesToSkipY = 0



        if self.framesToSkipX > 1:

            self.frameDelayX = self.framesToSkipX

            if self.floatDx < 0:

                self.floatDx = -1

            else:

                self.floatDx = 1

        else:

            self.frameDelayX = None



        if self.framesToSkipY > 1:

            self.frameDelayY = self.framesToSkipY

            if self.floatDy < 0:

                self.floatDy = -1

            else:

                self.floatDy = 1

        else:

            self.frameDelayY = None

    def skipFrames(self, axis):

        if axis == "x":

            self.frameDelayX -= 1

            if self.frameDelayX < 1:

                self.frameDelayX = self.framesToSkipX
                doMove = True

            else:

                doMove = False

        elif axis == "y":

            self.frameDelayY -= 1

            if self.frameDelayY < 1:

                self.frameDelayY = self.framesToSkipY
                doMove = True

            else:

                doMove = False

        return doMove

class WrappingBkg(FloatingBkg):
    """ FloatingBkg obj that wraps around the field """

    def update(self):
        FloatingBkg.update(self)
        self.checkWrap()

    def checkWrap(self):
        (rBoxX, rBoxY) = radar56.Radar.getTrackerLoc()

        if self.rect.left - rBoxX > scroller56.Scroller.fieldWidth:
            self.rect.right = rBoxX
        elif rBoxX - self.rect.right > 0:
            self.rect.left = scroller56.Scroller.fieldWidth
        elif self.rect.top - rBoxY > scroller56.Scroller.fieldHeight:
            self.rect.bottom = rBoxY
        elif rBoxY - self.rect.bottom > 0:
            self.rect.top = scroller56.Scroller.fieldHeight

class NyanCat(FloatingBkg):
    """ background object for nyan bonus mode """
    frames = []
    yQueue = []
    FRAMESKIP = 4

    def __init__(self, game, minSpeed, gridPos, frames, scaleTo, getAt, floatSpeed, gridSize):

        if not NyanCat.frames:
            for imgFile in frames:
                img = dinosInSpace.loadImage(imgFile, scaleTo, getAt)
                NyanCat.frames.append(img)

        center = static56.gridToCoord(gridPos)
        FloatingBkg.__init__(self, game, minSpeed, center, frames[0], scaleTo, getAt, 0, floatSpeed)

        self.gridSize = gridSize
        self.currentFrame = 0
        self.frameTick = NyanCat.FRAMESKIP

    def update(self):
        FloatingBkg.update(self)
        self.animate()
        self.checkWrap()

    def animate(self):
        self.frameTick -= 1
        if self.frameTick < 0:
            self.frameTick = NyanCat.FRAMESKIP
            self.currentFrame += 1
            if self.currentFrame >= len(NyanCat.frames):
                self.currentFrame = 0
            self.image = NyanCat.frames[self.currentFrame]


    def checkWrap(self):
	"""
	    specialized wrap method for nyan cats
	    - only handles going off right side of field
	    - moves to left side and shifts y axis to an open point (not in queue)
	"""
        (rBoxX, rBoxY) = radar56.Radar.getTrackerLoc()

        if self.rect.left - rBoxX > scroller56.Scroller.fieldWidth:
            self.rect.right = rBoxX
            self.rect.bottom = self.shift_y()

    def shift_y(self):
        """ shift y axis to open position after wrapping """
        y = 0
        while (y in NyanCat.yQueue) or (y == 0):
            y = random.randint(1, self.gridSize[1] - 1)

        NyanCat.updateQueue(y)
        trashthis, yPoint = static56.gridToCoord((0, y))

        return yPoint

    @staticmethod
    def buildQueue(queueList):
        queueList.sort()
        NyanCat.yQueue = list(queueList)

    @staticmethod
    def updateQueue(yVal):
        NyanCat.yQueue.insert(0, yVal)
        if len(NyanCat.yQueue) > MAX_NYANCATS:
            NyanCat.yQueue.pop()

    @staticmethod
    def wipe():
        NyanCat.yQueue = []


class CyborgCow(WrappingBkg):
    """ flash 2nd frame at simi-random intervals """

    def __init__(self, game, minSpeed, center, imageFile, scaleTo, getAt, spinRange, floatSpeed, flashData):

        WrappingBkg.__init__(self, game, minSpeed, center, imageFile, scaleTo, getAt, spinRange, floatSpeed)
        self.OFFTIME, self.VAR_RANGE= flashData
        self.orgOff = self.original # should be cow1.png (unlit)
        self.setImage("testCowLit.png", scaleTo, (0,0))# sets self.original = cow2.png (lit)
        self.orgOn = self.original # cow2.png (lit)
        self.resetCountDown()

    def spin(self):
        """ rotate image """

        self.spinDistance += self.spinStep

        if self.spinStep > 0:

            if self.spinDistance >= 360:

                startHere = self.spinDistance - 360
                self.spinDistance = startHere   # reset spinDistance

        else:

            if self.spinDistance <= -360:

                starHere = self.spinDistance + 360
                self.spinDistance = starHere

        self.setFrame()

    def setFrame(self):

        rotate = pygame.transform.rotate
        self.flashCountDown -= 1

        if self.flashCountDown < 1:

            self.image = rotate(self.orgOn, self.spinDistance)

        else:

            self.image = rotate(self.orgOff, self.spinDistance)

        if self.flashCountDown < 0:

            self.flashCountDown = self.resetCountDown()



    def resetCountDown(self):
        """ set timer count down to flash """

        variation = random.randrange(-self.VAR_RANGE, self.VAR_RANGE)
        self.flashCountDown = self.OFFTIME + variation

        return self.flashCountDown

def construct(game, data):
    """ generates a default 2 layer scrolling background """

    screen = game.screen
    needAdd = False

    # nyan bonus ###
    takenNyanCoords_X = [0]
    takenNyanCoords_Y = [0]
    queueList = [] # x vals
    ################

    for dataSet in data:

        if dataSet[0] == "star":
            XX, step, color = dataSet
            StarBuilder(game, screen, 2, step, color) # stateObj, screen, size, step, col)

        elif dataSet[0] == "scroll":
            XX, minSpeed, gridPair, imgFile, scaleTo, getAt, spinRange = dataSet
            center = static56.gridToCoord(gridPair)
            ScrollingBkg(game, minSpeed, center, imgFile, scaleTo, getAt, spinRange)
            needAdd = True

        elif dataSet[0] == "float":
            XX, minSpeed, gridPair, imgFile, scaleTo, getAt, spinRange, floatSpeed = dataSet
            center = static56.gridToCoord(gridPair)
            FloatingBkg(game, minSpeed, center, imgFile, scaleTo, getAt, spinRange, floatSpeed)
            needAdd = True

        elif dataSet[0] == "wrap":
            XX, minSpeed, gridPair, imgFile, scaleTo, getAt, spinRange, floatSpeed = dataSet
            center = static56.gridToCoord(gridPair)
            WrappingBkg(game, minSpeed, center, imgFile, scaleTo, getAt, spinRange, floatSpeed)
            needAdd = True

        elif dataSet[0] == "cow":
            XX, minSpeed, gridPair, imgFile, scaleTo, getAt, spinRange, floatSpeed, flashData = dataSet
            center = static56.gridToCoord(gridPair)
            CyborgCow(game, minSpeed, center, imgFile, scaleTo, getAt, spinRange, floatSpeed, flashData)
            needAdd = True

        elif dataSet[0] == "nyan":

            XX, minSpeed, gridSize, frames, scaleTo, getAt, floatSpeed = dataSet # note gridPair replaced w/ gridSize!

            x = 0
            y = 0
            while (x in takenNyanCoords_X) or (y in takenNyanCoords_Y) :
                x = random.randint(1, gridSize[0] - 1)
                y =  random.randint(1, gridSize[1] - 1)
            takenNyanCoords_X.append(x)
            takenNyanCoords_Y.append(y)
            queueList.append(x)

            NyanCat(game, minSpeed, (x, y), frames, scaleTo, getAt, floatSpeed, gridSize)
            needAdd = True


    if queueList:
        assert(len(queueList) == MAX_NYANCATS)
        NyanCat.buildQueue(queueList)

    if needAdd:
        game.addGroup(ScrollingBkg.myGroup)

def wipe():
    ScrollingBkg.wipe()
    FloatingBkg.wipe()
    NyanCat.wipe()

if __name__ == "__main__":

    input("module for import only")