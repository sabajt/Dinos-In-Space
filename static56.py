
""" static56.py

    class
    Sprite
    StaticBlock
    Spawn
    Goal
    Mine
    StaticArrow
    StaticArrowL
    Switch
    GoalCounter
    function
    gridToCoord
    buildSpawn
    buildGoal
    buildMine
    buildStaticArrow
    buildStaticArrowL
    buildSwitch
    makeGoalCounter
    wipe

    """

import pygame
import random
import dinosInSpace
import scroller56
import radar56
import groupMods56
import interface56
import soundFx56
import tracer56
import infoGraphic56
import dino56
import snack
import spriteBasic
import fpsSwitch
import bounceMask

STATION_SPINDELAY = 2

BLACK = (0,0,0)
WHITE = (255,255,255)
DGREY = (60,60,60)
LTGREY = (200,200,200)
ORANGE = (255,125,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

CHANNEL_NUMBER_SIZE = 30
CHANNEL_NUMBER_COLOR_ARROW = ORANGE
CHANNEL_NUMBER_COLOR_SWITCH = BLACK
SLOT_DISTANCE_FROM_MIDDLE = 15
SLOT_RIGHT_FIX = -1
SLOT_BOTTOM_FIX = -1
SPAWNSLOT_SIZE = (15,15)
SPAWN_BLINK_DELAY = 5

DINO_BLUE = (29,139,255)
DINO_GREEN = (159,247,23)
DINO_RED = (226,70,79)
DINO_YELLOW = (255,246,0)

class StaticBlock(pygame.sprite.Sprite):
    staticGroup = groupMods56.SR_OrderedUpdates() # group to add to game / radar

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.minSpeed = dinosInSpace.Game.getMinSpeed()
        StaticBlock.staticGroup.add(self)

    def update(self):
        self.setSpeed()

    @staticmethod
    def addSpriteToGroup(spr):
        StaticBlock.staticGroup.add(spr)

    @staticmethod
    def wipe():
        StaticBlock.staticGroup = groupMods56.SR_OrderedUpdates()

    @staticmethod
    def getStaticGroup():
        return StaticBlock.staticGroup

    def setSpeed(self):
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

    def reverseStep(self):
        xSpeedRat, ySpeedRat = scroller56.Scroller.speedData
        dx = -(xSpeedRat * self.minSpeed)
        dy = -(ySpeedRat * self.minSpeed)
        return dx, dy

class Spawn(StaticBlock):
    """ starting point(s) for dinos """
    numSpawns = 0
    spawnDict = {}
    spawnGroup = groupMods56.SR_OrderedUpdates()
    originalFrames = None

    framesNorth = []
    framesSouth = []
    framesEast = []
    framesWest = []

    def __init__(self, game, loc, dinoData):

        self.CLASS = "Spawn"
        StaticBlock.__init__(self, game)
        Spawn.numSpawns += 1
        Spawn.spawnDict[Spawn.numSpawns] = self

        self.active = False
        self.direction = 1 # 1 == north, 2 == east, 3 == south, 4 == west (for dino)
        self.myFrames = []
        self.frame = 0
        self.FDELAY = SPAWN_BLINK_DELAY
        if fpsSwitch.FPSSwitch._fps == 60:
            self.FDELAY *= 2

        self.frameTick = self.FDELAY
        self.loadImages()
        self.rect = self.image.get_rect()
        self.rect.bottomright = loc
        self.setInfoBox(game, dinoData)
        Spawn.spawnGroup.add(self)

        self.slotObjects = self.setColorSlots(dinoData) # for hideSlots ref
        self.slotCount = 0

    @staticmethod
    def quickReset():
        for s in Spawn.spawnGroup:
            s.quickResetMe()

    def getCenter(self):
        return self.rect.center

    def quickResetMe(self):
        self.active = False
        self.showSlots()
        self.slotCount = 0

    def update(self):
        StaticBlock.update(self)
        self.tickFrames()
        self.checkMouseOver()

    def checkMouseOver(self):
        if pygame.sprite.collide_rect(self, interface56.Cursor.theCursor):
            self.infoBox.showMe()
        else:
            self.infoBox.hideMe()

    @staticmethod
    def wipe():
        Spawn.numSpawns = 0
        Spawn.spawnDict = {}
        Spawn.spawnGroup = groupMods56.SR_OrderedUpdates()

    @staticmethod
    def activate():
        for s in Spawn.spawnGroup:
            s.active = True

    def tickFrames(self):
        """ animation frames """
        self.frameTick -= 1
        if self.frameTick < 1:
            self.frame += 1
            if self.frame > len(self.myFrames) - 1:
                self.frame = 0
            self.image = self.myFrames[self.frame]
            self.frameTick = self.FDELAY

    def setInfoBox(self, game, dinoData):
        """ displays order, number, direction, and color of dinos to launch """
        self.infoBox = infoGraphic56.SpawnInfoBox(game, dinoData)

    def getDirection(self):
        return self.direction    # give to dino

    def setDirection(self, direction):
        """ rotate image and set launch direction """
        if direction == "north":
            self.myFrames = Spawn.framesNorth
            self.direction = 1
        elif direction == "east":
            self.myFrames = Spawn.framesEast
            self.direction = 2
        elif direction == "south":
            self.myFrames = Spawn.framesSouth
            self.direction = 3
        elif direction == "west":
            self.myFrames = Spawn.framesWest
            self.direction = 4

        self.image = self.myFrames[0]

#    def loadImages(self):
#        if not Spawn.originalFrames:
#            fileName = "nSpawn"
#            Spawn.originalFrames = []
#
#            for i in range(16):
#                imageFile = fileName + str(15-i) +  ".png" # generate a unique file name
#                image = dinosInSpace.loadImage(imageFile, (100,100), (0,0))
#                Spawn.originalFrames.append(image)
#
#            for i in Spawn.originalFrames:
#                Spawn.framesNorth.append(i.copy())
#
#            for i in Spawn.originalFrames:
#                i = pygame.transform.rotate(i.copy(), -90)
#                Spawn.framesEast.append(i)
#
#            for i in Spawn.originalFrames:
#                i = pygame.transform.rotate(i, 180)
#                Spawn.framesSouth.append(i)
#
#            for i in Spawn.originalFrames:
#                i = pygame.transform.rotate(i, 90)
#                Spawn.framesWest.append(i)
#
#        self.image = Spawn.originalFrames[self.frame].copy()
#
    def loadImages(self):
        if not Spawn.originalFrames:
            image0 = dinosInSpace.loadImage("fnSpawn0.png", "2X", (0,0))
            image1 = dinosInSpace.loadImage("fnSpawn1.png", "2X", (0,0))
            Spawn.originalFrames = [image0, image1]

            for i in Spawn.originalFrames:
                Spawn.framesNorth.append(i.copy())
            for i in Spawn.originalFrames:
                i = pygame.transform.rotate(i.copy(), -90)
                Spawn.framesEast.append(i)
            for i in Spawn.originalFrames:
                i = pygame.transform.rotate(i, 180)
                Spawn.framesSouth.append(i)
            for i in Spawn.originalFrames:
                i = pygame.transform.rotate(i, 90)
                Spawn.framesWest.append(i)

        self.image = Spawn.originalFrames[self.frame].copy()

    def setColorSlots(self, dinoData):
        # [type, num, color, speed, spawn, delayStart(int*25), delayStep(25)]
        catchSlots = []
        allSlots = [] # just to compare numbers

        myDataSets = []
        for d in dinoData:
            if d[4] == Spawn.numSpawns:
                myDataSets.append(d)

        for d in myDataSets:
            color = d[2]
            delayStep = d[5]
            assert(delayStep % 25 == 0)
            slot = delayStep / 25
            catchSlots.append((slot, color))
            allSlots.append(slot)

        ## fill out slots with empty entries -- max of 4
        defSlots = [(1, "empty"), (2, "empty"), (3, "empty"), (4, "empty")]

        slots = []
        index = 0
        catchIndex = 0
        for s in defSlots:
            if s[0] in allSlots:
                slots.append(catchSlots[catchIndex])
                catchIndex += 1
            else:
                slots.append(defSlots[index])
            index += 1

        assert(len(slots) == 4)

        ## make color blocks according to slots
        slotObjects = []
        for s in slots:
            if s[1] == "green":
                color = DINO_GREEN
            elif s[1] == "red":
                color = DINO_RED
            elif s[1] == "blue":
                color = DINO_BLUE
            elif s[1] == "yellow":
                color = DINO_YELLOW
            elif s[1] == "empty":
                color = None

            if color:
                newSlot = SpawnSlot(self, s[0], color)
                slotObjects.append(newSlot)
                StaticBlock.addSpriteToGroup(newSlot)

        return slotObjects # for hideSlot ref

    def hideSlot(self):
        self.slotObjects[self.slotCount].hide()
        self.slotCount += 1

    def showSlots(self):
        for s in self.slotObjects:
            s.show()

class SpawnSlot(spriteBasic.BasicRect):

    def __init__(self, spawnTile, slot, color):
        spriteBasic.BasicRect.__init__(self, SPAWNSLOT_SIZE, color) # ... + topleft, rimsize, alpha, opaque cnt
        self.spawnTile = spawnTile

        if slot == 1:
            self.distanceFromMid = (-SLOT_DISTANCE_FROM_MIDDLE, -SLOT_DISTANCE_FROM_MIDDLE)
        elif slot == 2:
            self.distanceFromMid = (SLOT_DISTANCE_FROM_MIDDLE + SLOT_RIGHT_FIX, -SLOT_DISTANCE_FROM_MIDDLE)
        elif slot == 3:
            self.distanceFromMid = (-SLOT_DISTANCE_FROM_MIDDLE, SLOT_DISTANCE_FROM_MIDDLE + SLOT_BOTTOM_FIX)
        elif slot == 4:
            self.distanceFromMid = (SLOT_DISTANCE_FROM_MIDDLE + SLOT_RIGHT_FIX, SLOT_DISTANCE_FROM_MIDDLE + SLOT_BOTTOM_FIX)

        self.CLASS = "SpawnSlot" # for compatibility with stupid earlier code

    def update(self):
        self.rect.center = (
            self.spawnTile.rect.centerx + self.distanceFromMid[0],
            self.spawnTile.rect.centery + self.distanceFromMid[1]
        )

    def hide(self):
        self.image.set_alpha(0, pygame.RLEACCEL)

    def show(self):
        self.image.set_alpha(255, pygame.RLEACCEL)


class Goal(StaticBlock):
    saved = 0
    goalGroup = groupMods56.SR_OrderedUpdates()
    colors = None # holds different colored images

    def __init__(self, game, loc, objColor, _fps):
        self.CLASS = "Goal"
        StaticBlock.__init__(self, game)
        self.frame = 0
        self.FDELAY = STATION_SPINDELAY
        if _fps == 60:
            self.FDELAY*=2
        self.frameTick = self.FDELAY
        self.colorIndex = self.setColor(objColor)  # color att and colorIndex
        self.loadImages()   # load images AND set self's image
        self.rect = self.image.get_rect()
        self.rect.bottomright = loc
        self.setSpin(_fps)
        Goal.goalGroup.add(self)

    def update(self):
        """ called every tick by game """
        self.setSpeed()
        self.spin()
        self.frameTick -= 1

        if self.frameTick < 1:
            self.changeFrame()
            self.frameTick = self.FDELAY

    def changeFrame(self):
        self.frame += 1
        if self.frame > 32:
            self.frame = 0

    @staticmethod
    def wipe():
        Goal.saved = 0
        Goal.goalGroup = groupMods56.SR_OrderedUpdates()

    @staticmethod
    def quickReset():
        Goal.saved = 0

    @staticmethod
    def saveDino():
        Goal.saved += 1

    @staticmethod
    def getSaved():
        return Goal.saved

    def loadImages(self):
        """ load images for all colors / animation """
        if not Goal.colors:
            Goal.colors = []
            fileName = ""

            for i in range(5):
                frames = []
                if i == 0:
                    fileName = "nStationG"
                elif i == 1:
                    fileName = "nStationB"
                elif i == 2:
                    fileName = "nStationR"
                elif i == 3:
                    fileName = "nStationY"
                elif i == 4:
                    fileName = "nStationW"

                for j in range(33):
                    imageFile = fileName + str(j) +  ".png" # generate a unique file name
                    image = dinosInSpace.loadImage(imageFile, (100,100), (0,0))
                    frames.append(image)

                Goal.colors.append(frames)

        self.image = Goal.colors[self.colorIndex][self.frame]
        self.original = self.image.copy()

    def setColor(self, objColor):
        self.objColor = objColor # green, blue, red, yellow or none - this is the attr used for collision detect
        if objColor == "green":
            colorIndex = 0
        elif objColor == "blue":
            colorIndex = 1
        elif objColor == "red":
            colorIndex = 2
        elif objColor == "yellow":
            colorIndex = 3
        else:
            colorIndex = 4  # grey (wild)

        return colorIndex

    def setSpin(self, _fps):
        """ initiate spin cycle """
        self.original = self.image.copy()
        self.spinStep = 1
        self.spinDistance = 0
        self.spinTick = 0
        self.SPINDELAY = 0
        if _fps == 60:
            self.SPINDELAY = 2

    def setSpeed(self):
        """ set speed from Scroller """
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

    def spin(self):
        """ rotate image """
        self.spinTick -= 1
        if self.spinTick <= 0:
            self.spinTick = self.SPINDELAY

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

            image = Goal.colors[self.colorIndex][self.frame]    # get the colored image
            self.image = rotate(image, self.spinDistance)

class Mine(StaticBlock):

    mineGroup = pygame.sprite.RenderUpdates()
    imageList = []   # list of surface
    spinActive = False

    def __init__(self, game, loc):
        self.CLASS = "Mine"
        StaticBlock.__init__(self, game)

        self.IMAGERANGE = 4 # file image range

        self.setImage()
        self.setRect(loc)
        self.setSpin(-1, 1)

        Mine.mineGroup.add(self)

    def update(self):
        StaticBlock.update(self)
        self.spin()

    @staticmethod
    def wipe():
        Mine.mineGroup = pygame.sprite.RenderUpdates()
        Mine.spinActive = False

    def setImage(self):
        if not Mine.imageList:
            fileName = "rock"
            for i in range(self.IMAGERANGE):
                Mine.imageList.append(dinosInSpace.loadImage(fileName + str(i) + ".png", "2X", (0,0)))

        self.image = Mine.imageList[random.randrange(self.IMAGERANGE)].copy()
        self.original = self.image.copy()

    def setRect(self, loc):

        self.rect = self.image.get_rect()
        self.rect.bottomright = loc

    def setSpin(self, rangeStart, rangeStop):
        """ initiate spin cycle """

        self.spinStep = 0

        while self.spinStep > -0.2 and self.spinStep < 0.2:   # not too slow

            self.spinStep = random.uniform(rangeStart, rangeStop)

        self.spinDistance   = 0

    def spin(self):
        """ rotate image """
        if Mine.spinActive:
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


class StaticArrow(StaticBlock):
    """ like normal arrow, but pre-placed / can't rotate or be removed """

    sArrowGroup = pygame.sprite.RenderUpdates()
    colors = None

    def __init__(self, game, loc, objColor, facing):

        self.CLASS = "StaticArrow"
        StaticBlock.__init__(self, game)

        self.setFacing(facing)
        self.colorIndex = self.setColor(objColor)  # color att and colorIndex
        self.loadImages()   # load images AND set self's image
        self.rect = self.image.get_rect()
        self.rect.bottomright = loc
        StaticArrow.sArrowGroup.add(self)

        self.bounceMask = bounceMask.BounceMask(self)
        StaticBlock.addSpriteToGroup(self.bounceMask)

    @staticmethod
    def wipe():

        StaticArrow.sArrowGroup = pygame.sprite.RenderUpdates()

    def flashBounceMask(self):
        self.bounceMask.flash()

    def setFacing(self, facing):
        if facing == "north":
            self.facing = 1
        elif facing == "east":
            self.facing = 2
        elif facing == "south":
            self.facing = 3
        elif facing == "west":
            self.facing = 4

    def setColor(self, objColor):
        self.objColor = objColor # green, blue, red, yellow or none - for collision detect
        if objColor == "green":
            colorIndex = 0
        elif objColor == "blue":
            colorIndex = 1
        elif objColor == "red":
            colorIndex = 2
        elif objColor == "yellow":
            colorIndex = 3

        else:

            colorIndex = 4  # grey

        return colorIndex

    def loadImages(self):
        """ load images for color change """

        if not StaticArrow.colors:

            StaticArrow.colors = []

            for i in range(5):

                imageFile = "sArrow" + str(i + 1) +  ".png" # generate a unique file name
                image = dinosInSpace.loadImage(imageFile, (100,100), (0,0))

                #image.set_clip((0,0,50,50))
                #newImage = pygame.Surface((50,50))
                #newImage.blit(image, (0,0))
                #StaticArrow.colors.append(newImage)

                StaticArrow.colors.append(image)

        self.image = StaticArrow.colors[self.colorIndex]

        if self.facing == 2:

            self.image = pygame.transform.rotate(self.image, -90) # east

        elif self.facing == 3:

            self.image = pygame.transform.rotate(self.image, 180) # south

        elif self.facing == 4:

            self.image = pygame.transform.rotate(self.image, 90) # west

        self.original = self.image.copy()

#############################
#def setColorSlots(self, dinoData):
#	# [type, num, color, speed, spawn, delayStart(int*25), delayStep(25)]
#
#	## convert dino data to list of slot paired with color [(slot, color), ...]
#	catchSlots = []
#	allSlots = [] # just to compare numbers
#	dataSet = dinoData[Spawn.numSpawns - 1]
#	if len(dataSet) > 1:
#	    for d in dataSet:
#            color = d[2]
#            delayStep = d[5]
#            assert(delayStep % 25 == 0)
#            slot = delayStep / 25
#            catchSlots.append((slot, color))
#            allSlots.append(slot)
#	else:
#	    color = dataSet[2]
#	    delayStep = d[5]
#	    assert(delayStep % 25 == 0)
#	    slot = delayStep / 25
#	    catchSlots.append((slot, color))
#
#	## fill out slots with empty entries -- max of 4
#	defSlots = [(1, "empty"), (2, "empty"), (3, "empty"), (4, "empty")]
#	slots = []
#	index = 0
#	catchIndex = 0
#	for s in defSlots:
#	    if s in allSlots:
#            slots.append(catchSlots[catchIndex])
#            catchIndex += 1
#	    else:
#            slots.append(defSlots[index])
#	    index += 1
#
#	assert(len(slots) == 4)
#
#	## make color blocks according to slots
#	print slots
#############################

class StaticArrowL(StaticArrow):
    """ Static Arrow w/ 2 states linked to switch """
    # SArrowGroup still exists.... fix this
    sArrowLGroup = pygame.sprite.OrderedUpdates()
    colors = None
    hiddenImage = None


    def __init__(self, game, loc, objColor, state1, state2, switchNum):

        self.CLASS = "StaticArrowL"
        StaticBlock.__init__(self, game) # not sure why i did this... works for now

        self.location = loc # use this to see if arrows overlap (make "hidden" frame invisible)
        self.switchNum = switchNum
        self.colorIndex = self.setColor(objColor)  # color att and colorIndex
        self.loadImages()   # load images AND set self's image
        self.state1 = state1
        self.state2 = state2
        self.setState(1)
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.location

        channelNum = ChannelNumber(str(switchNum), CHANNEL_NUMBER_SIZE, CHANNEL_NUMBER_COLOR_ARROW, self)
       	StaticArrowL.sArrowLGroup.add(self)
    #StaticArrowL.sArrowLGroup.add(channelNum)

        self.bounceMask = bounceMask.BounceMask(self)
        StaticBlock.addSpriteToGroup(self.bounceMask)

    @staticmethod
    def wipe():

        StaticArrowL.sArrowLGroup = pygame.sprite.RenderUpdates()

    def getCenter(self):
        return self.rect.center

    def getSwitchNum(self):
        return self.switchNum

    def setState(self, stateNum):
        if stateNum == 1:
            s = self.state1
        elif stateNum == 2:
            s = self.state2
        if s == "north":
            self.facing = 1
            self.image = self.original
            self.active = True
        elif s == "east":
            self.facing = 2
            self.image = pygame.transform.rotate(self.original, -90)
            self.active = True
        elif s == "south":
            self.facing = 3
            self.image = pygame.transform.rotate(self.original, 180)
            self.active = True
        elif s == "west":
            self.facing = 4
            self.image = pygame.transform.rotate(self.original, 90)
            self.active = True
        elif s == "hidden":
            self.facing = None
            self.image =  StaticArrowL.hiddenImage.copy()
            self.active = False
            for spr in StaticArrowL.sArrowLGroup: # check for overlapping to hide empty frame
                if spr.__class__ == StaticArrowL:
                    if spr != self and spr.location == self.location:
                        self.image.set_alpha(0, pygame.RLEACCEL)
        else:
            print "StaticArrowL state not recognized"

    def loadImages(self):
        """ load images for color change and empty frame """

        if not StaticArrowL.colors:

            greenImg = dinosInSpace.loadImage("linkedArrG.png", (100,100), (0,0))
            blueImg = dinosInSpace.loadImage("linkedArrB.png", (100,100), (0,0))
            redImg = dinosInSpace.loadImage("linkedArrR.png", (100,100), (0,0))
            yellowImg = dinosInSpace.loadImage("linkedArrY.png", (100,100), (0,0))
            greyImg = dinosInSpace.loadImage("linkedArrW.png", (100,100), (0,0))
            StaticArrowL.colors = [greenImg, blueImg, redImg, yellowImg, greyImg]

        self.image = StaticArrowL.colors[self.colorIndex]
        self.original = self.image.copy()

        if not StaticArrowL.hiddenImage:

            image = dinosInSpace.loadImage("blockFrame.png", (100,100), (0,0))
            StaticArrowL.hiddenImage = image


class ChannelNumber(infoGraphic56.TextObject):
    """ number of channel for switches and linked for display """

    def __init__(self, text, size, color, tile):
        self.CLASS = "ChannelNumber" # stupid, only for compatibility with previous stupid code
        infoGraphic56.TextObject.__init__(self, text, size, color)
        self.myTile = tile
        StaticBlock.addSpriteToGroup(self)

    def update(self):
        self.rect.topleft = self.myTile.rect.topleft


class Switch(StaticBlock):  # todo: make common class (look at Mine)
    """ one-time switch that sends state changes to static objects """

    switchGroup = groupMods56.SR_OrderedUpdates()
    imageFrames = None # on and off only

    def __init__(self, game, loc):
        self.CLASS = "Switch"
        StaticBlock.__init__(self, game)
        self.game = game
        self.loadImages()
        self.setRect(loc)
        self.hasFlipped = False
        self.on = False
        self.myTracers = []
        self.snackTags = None # set in setLinked

        Switch.switchGroup.add(self)

    @staticmethod
    def wipe():
        Switch.switchGroup = groupMods56.SR_OrderedUpdates()
        Switch.channelCount = 0

    @staticmethod
    def quickReset():
        for s in Switch.switchGroup:
            s.hasFlipped = False
        Switch.resetAll()

    @staticmethod
    def resetAll():
        for s in Switch.switchGroup:
            if s.__class__ == Switch:
                s.flipSwitch(False, True) # on, isTest

                interface56.Cursor.testSwitchDown = False

                isSnax = False
                for l in s.linkedObjs:
                    if l.__class__ == snack.Snack:
                        s.linkedObjs.remove(l)
                        isSnax = True
                if isSnax:
                    for sx in snack.Snack.snaxGroup:
                        if sx.imageKey in s.snackTags:
                            s.appendLinked(sx)


    @staticmethod
    def makeTracers():
        for switch in Switch.switchGroup:
            if switch.__class__ == Switch:
                for obj in switch.linkedObjs:
                    t = tracer56.SwitchTracer(switch, obj)
                    switch.myTracers.append(t)

    def getCenter(self):

        return self.rect.center

    def setLinked(self, linkedObjs):
        """ set self.linkedObjs """
        self.linkedObjs = linkedObjs
        channelNum = ChannelNumber(str(self.linkedObjs[0].switchNum), CHANNEL_NUMBER_SIZE, CHANNEL_NUMBER_COLOR_SWITCH, self)
        #Switch.switchGroup.add(channelNum)

        ## record snackList initially -- use ...
        snackTags = []
        for l in linkedObjs:
            if l.__class__ == snack.Snack:
                snackTags.append(l.imageKey)
        self.snackTags = snackTags


    def appendLinked(self, linkedObj):
        self.linkedObjs.append(linkedObj)

    def flipSwitch(self, on, isTest):

        if not self.hasFlipped:

            if on:

                self.requestScreenSnd("switch")
                self.image = Switch.imageFrames[1]
                self.on = True

                for obj in self.linkedObjs:

                    obj.setState(2)

                if isTest:

                    for t in self.myTracers:

                        t.activate()

            else:

                if self.on:

##                    self.requestScreenSnd("switch")
                    self.image = Switch.imageFrames[0]
                    self.on = False

                    for t in self.myTracers:

                        t.deactivate()

                for obj in self.linkedObjs:

                    obj.setState(1)

        if not isTest:

            self.hasFlipped = True

    def loadImages(self):

        if not Switch.imageFrames:

            Switch.imageFrames = []
            fileName = "nSwitch"

            for i in range(2):

                imageFile = fileName + str(i) +  ".png" # generate a unique file name
                image = dinosInSpace.loadImage(imageFile, (100,100), (0,0))

                Switch.imageFrames.append(image)

        self.image = Switch.imageFrames[0].copy()

    def setRect(self, loc):

        self.rect = self.image.get_rect()
        self.rect.bottomright = loc

    def requestScreenSnd(self, sound):
        """ only play these sounds if on screen """

        if self.rect.right > 0 \
            and self.rect.left < self.game.screen.get_width() \
            and self.rect.bottom > 0 \
            and self.rect.top < self.game.screen.get_height():

            soundFx56.GameSoundManager.registerSound(sound)

class GoalCounter(infoGraphic56.InfoGraphic):

    gCounterGroup = pygame.sprite.RenderUpdates()

    def __init__(self, game, text, color, topRight):

        infoGraphic56.InfoGraphic.__init__(self)
        self.ALPHA = 255
        self.font = dinosInSpace.FontBank.getFont(25)
        self.text = text
        self.color = color
        self.topRight = topRight
        self.total = str(dino56.Dino.totalCount) # only get once
        GoalCounter.gCounterGroup.add(self)

    def update(self):   # todo: make only happen when needed? similar to cursor-counter

        message = self.getMessage()

        if infoGraphic56.InfoGraphic.visible:

            self.image = self.font.render(message, False, self.color)
            self.rect = self.image.get_rect()
            self.rect.topright = self.topRight

    def getMessage(self):

        saved = str(Goal.getSaved())
        total = self.total
        message = self.text + " " + saved + "/" + total + " "

        return message

    @staticmethod
    def wipe():

        GoalCounter.gCounterGroup = pygame.sprite.RenderUpdates()

def gridToCoord((xGridLoc, yGridLoc)):
    """ returns: coordinate pair for playing field """

    xDist = xGridLoc * 100
    yDist = yGridLoc * 100
    tx, ty = radar56.Radar.getTrackerLoc()
    x = tx + xDist
    y = ty + yDist

    return (x, y)

def buildGoal(game, gridCoord, color, _fps):
    """ return: goal object """

    loc = gridToCoord(gridCoord)
    goal = Goal(game, loc, color, _fps)

    return goal

def buildSpawn(game, gridCoord, facing, dinoData):
    """ return: spawn object """

    loc = gridToCoord(gridCoord)
    spawn = Spawn(game, loc, dinoData)
    spawn.setDirection(facing)

    return spawn

def buildStaticArrow(game, gridCoord, color, facing):
    """ return: static arrow object """

    loc = gridToCoord(gridCoord)
    sArrow = StaticArrow(game, loc, color, facing)

    return sArrow

def buildLinkedArrow(game, gridCoord, color, state1, state2, switchNum):
    """ return: static arrow object linked to switch """

    loc = gridToCoord(gridCoord)
    linkArrow = StaticArrowL(game, loc, color, state1, state2, switchNum)

    return linkArrow

def buildMine(game, gridCoord):
    """ return: mine object """

    loc = gridToCoord(gridCoord)
    mine = Mine(game, loc)

    return mine

def buildSwitch(game, gridCoord):
    """ return: switch object """

    loc = gridToCoord(gridCoord)
    switch = Switch(game, loc)

    return switch

def makeGoalCounter(game):  # this fx must be seperate from goal and spawn because it is diplayed on top
    """ make goal counter(s) - customize parameters here """

    text = "SAFE: "
    color = (0,0,255)
    topRight = (game.screen.get_width(), 0)
    GoalCounter(game, text, color, topRight)
    game.addGroup(GoalCounter.gCounterGroup)

def wipe():

    Goal.wipe()
    GoalCounter.wipe()
    Spawn.wipe()
    StaticArrow.wipe()
    Mine.wipe()
    Switch.wipe()
    StaticArrowL.wipe()
    StaticBlock.wipe()

def freezeRocks(freeze):
    if freeze:
        Mine.spinActive = False
    else:
        Mine.spinActive = True


if __name__ == "__main__":
    print "module for import only"