""" block56.py

    class
        Sprite
            Block
                Arrow
                Warp
    function
        buildUserBlocks
        wipe

"""

import pygame
import interface56
import scroller56
import dinosInSpace
import radar56
import soundFx56
import math
import bounceMask

class Block(pygame.sprite.Sprite):
    """ superclass for objects that can be placed """

    OFFSCREEN = (-100,-100)
    minSpeed = dinosInSpace.Game.getMinSpeed()

    canRecoverThis = None # any obj that is eligible for recovery, if any
    canRotateThis = None # arrow obj that is eligible for rotation, if any
    canLinkThis = None # warp obj that is eligible for opening link, if any
    canEndLinkThis = None # warp obj that is eligible for closing link, if any

    activeGroup = pygame.sprite.RenderUpdates() # all active (on screen) blocks
    blockGroup = pygame.sprite.RenderUpdates() # all blocks, for radar

    def __init__(self):
        """ initiate pygame's sprite class """

        pygame.sprite.Sprite.__init__(self)

        self.active = False
        Block.blockGroup.add(self)

    def update(self):

        self.checkActions()

        if self.active:

            self.setSpeed()

    @staticmethod
    def wipe():

        Block.OFFSCREEN = (-100,-100)
        Block.minSpeed = dinosInSpace.Game.getMinSpeed()
        Block.canRecoverThis = None
        Block.canRotateThis = None
        Block.canLinkThis = None
        Block.canEndLinkThis = None
        Block.activeGroup = pygame.sprite.RenderUpdates()
        Block.blockGroup = pygame.sprite.RenderUpdates()

    @staticmethod
    def getBlockGroup():

        return Block.blockGroup

    def setSpeed(self):
        """ set speed from Scroller """

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * Block.minSpeed
        dy = ySpeedRatio * Block.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

    def setRect(self):

        self.rect = self.image.get_rect()
        self.rect.center = Block.OFFSCREEN

    def checkActions(self):
        """ handle recovery / arrow rotation request from user """

        if not Block.canRecoverThis: # make sure no other obj ready for recovery

            if not Block.canRotateThis:

                if not Block.canLinkThis:

                    if not Block.canEndLinkThis:

                        if self.rect.colliderect(interface56.Cursor.theCursor.rect): # cursor is over self

                            if interface56.Cursor.isRecover:    # pressing recover key

                                Block.canRecoverThis = self   # make self the item ready for recovery

                            elif interface56.Cursor.canRotate:

                                if self.CLASS == "Arrow":

                                    Block.canRotateThis = self    # make self the item ready for rotation

                            elif interface56.Cursor.canLink:

                                if self.CLASS == "Warp":

                                    Block.canLinkThis = self # make self item ready for opening link

                            elif interface56.Cursor.isLinking:

                                if self.CLASS == "Warp":

                                    Block.canEndLinkThis = self # make self item ready for closing link



        if Block.canRecoverThis == self:  # if self is ready for recovery (should ONLY BE 1)

            if self.rect.colliderect(interface56.Cursor.theCursor.rect): # cursor is over self

                if not interface56.Cursor.isRecover:    # not pressing recover key

                     Block.canRecoverThis = None

            else: # cursor is not over self

                Block.canRecoverThis = None

        elif Block.canRotateThis == self:

            if not self.rect.colliderect(interface56.Cursor.theCursor.rect) \
                or interface56.Cursor.isRecover:

                Block.canRotateThis = None

        elif Block.canLinkThis == self:

            if not self.rect.colliderect(interface56.Cursor.theCursor.rect) \
                or interface56.Cursor.isRecover:

                Block.canLinkThis = None

        elif Block.canEndLinkThis == self:

            if not self.rect.colliderect(interface56.Cursor.theCursor.rect) \
                or interface56.Cursor.isRecover:

                Block.canEndLinkThis = None

    def placeMe(self, mousePos):
        """ place object on screen where user clicks, make active """

        self.rect.center = mousePos
        self.image = self.original
        self.active = True
        Block.activeGroup.add(self)

        if self.CLASS == "Arrow":

            self.facing = interface56.Cursor.getArrowGlyphFacing()

            if self.facing == 1:

                pass

            elif self.facing == 2:

                self.image = pygame.transform.rotate(self.image, -90)

            elif self.facing == 3:

                self.image = pygame.transform.rotate(self.image, -180)

            elif self.facing == 4:

                self.image = pygame.transform.rotate(self.image, -270)

    def hideMe(self):
        """ hide object offscreen, make inactive """

        self.rect.center = Block.OFFSCREEN
        self.active = False
        Block.activeGroup.remove(self)

        if self.CLASS == "Arrow":

            self.facing = 1

        elif self.CLASS == "Warp":

            if self.linkedWarp:

                self.resetAll(True)

            else:

                self.resetAll(False)


class Arrow(Block):
    """ child of placementObject - red for now """

    colors = None
    arrowGroup = pygame.sprite.RenderUpdates()
    maskGroup = pygame.sprite.Group()

    def __init__(self, objColor):

        Block.__init__(self)

        self.CLASS = "Arrow"
        self.facing = 1
        self.colorIndex = self.setColor(objColor)  # color att and colorIndex
        self.loadImages()   # load images and set
        self.setRect()

        Arrow.arrowGroup.add(self)

        self.bounceMask = bounceMask.BounceMask(self)
        Arrow.maskGroup.add(self.bounceMask)

    def flashBounceMask(self):
        self.bounceMask.flash()

    @staticmethod
    def wipe():
        Arrow.arrowGroup = pygame.sprite.RenderUpdates()
        Arrow.maskGroup = pygame.sprite.Group()

    @staticmethod
    def reqRotate():
        """ request to rotate 90 deg """

        obj = Block.canRotateThis

        if obj:

            obj.facing += 1 # 1-North, 2-East, 3-South, 4-West

            if obj.facing > 4:

                obj.facing = 1

            soundFx56.GameSoundManager.registerSound("rotate")    # play sound
            obj.image = pygame.transform.rotate(obj.image, -90)

    def setColor(self, objColor):

        self.objColor = objColor # green, blue, red, yellow

        if objColor == "green":

            colorIndex = 0

        elif objColor == "blue":

            colorIndex = 1

        elif objColor == "red":

            colorIndex = 2

        elif objColor == "yellow":

            colorIndex = 3

        else:

            colorIndex = 4 # grey

        return colorIndex

    def loadImages(self):
        """ multiple colors """

        if not Arrow.colors:

            Arrow.colors = []

            for i in range(5):

                imageFile = "nArrow" + str(i + 1) +  ".png" # generate a unique file name
                image = dinosInSpace.loadImage(imageFile, "2X", (0,0))

                Arrow.colors.append(image)

        self.image = Arrow.colors[self.colorIndex]
        self.original = self.image.copy()

class Warp(Block):
    """ blocks that warps dinos """

    defaultImage = None # surface
    warpReadyImage = None # surface
    NUMFRAMES = 24 # frames in active animation
    SEQFRAMES = 11 # frames in opening / closing animation
    PAIRS = ["A", "B", "C", "D", "E"] # all unique warps

    imagePairDict = {} # { 1 : [framesInList, framesOutList, inUse=False], etc... }
    readyForLink = None # obj - hold ready during link ready period
    transferInFrames = None # frames to transfer to new enter state
    transferSeqFrames = None # seq frames to transfer to new enter state
    warpGroup = pygame.sprite.RenderUpdates()

    def __init__(self):

        Block.__init__(self)

        self.CLASS = "Warp"

        self.setDefaultImage()
        self.state = "default"
        self.setImagePairs()
        self.rect = self.image.get_rect()
        self.rect.center = Block.OFFSCREEN
        self.warpNumIndex = None
        self.linkedWarp = None
        self.activeFrames = None # list of frames, depending on pair assignment
        self.seqFrames = None # list of frames for opening / closing sequence
        self.currentFrameSet = None # current set of frames to animate
        self.frame = 0

        Warp.warpGroup.add(self)

    def update(self):

        Block.update(self)

        if self.state == "enter" or self.state == "exit" or self.state == "default":

            if self.currentFrameSet:

                self.changeFrame(self.currentFrameSet)

    @staticmethod
    def wipe():

        Warp.readyForLink = None
        Warp.transferInFrames = None
        Warp.transferSeqFrames = None
        Warp.warpGroup = pygame.sprite.RenderUpdates()

        for i in Warp.imagePairDict:

            Warp.imagePairDict[i][2] = False

    @staticmethod
    def getImagePair():
        """ return inFramesList, outFramesList, imagePairDict key """

        for i in Warp.imagePairDict:

            if not Warp.imagePairDict[i][2]:

                inFramesList = Warp.imagePairDict[i][0]
                outFramesList = Warp.imagePairDict[i][1]
                inSeqList = Warp.imagePairDict[i][3]
                outSeqList = Warp.imagePairDict[i][4]

                Warp.imagePairDict[i][2] = True

                break

        return inFramesList, outFramesList, inSeqList, outSeqList, i

    @staticmethod
    def resetImagePair(i):
        """ make image pair avaliable for future use """

        if i:

            Warp.imagePairDict[i][2] = False

    @staticmethod
    def reqInitLink():
        """ setState 'ready' for warp """

        canLinkThis = Block.canLinkThis

        if canLinkThis:

            soundFx56.GameSoundManager.registerSound("chain")

            if canLinkThis.linkedWarp:

                canLinkThis.linkedWarp.setState("default")

            canLinkThis.setState("ready")
            interface56.Cursor.reqLink()
            Tracer.activate(canLinkThis)

    @staticmethod
    def reqMakeLink():
        """ setState 'enter' and 'exit' for warps """

        canEndLink = Block.canEndLinkThis

        if canEndLink:

            if Warp.readyForLink != canEndLink:

                soundFx56.GameSoundManager.registerSound("openWarp")

                if canEndLink.linkedWarp:

                    canEndLink.linkedWarp.setState("default")

                canEndLink.setState("exit")
                interface56.Cursor.breakLink()

        else:

            interface56.Cursor.breakLink()
            Warp.readyForLink.resetAll(False)

    def getCenter(self):

        return self.rect.center

    def changeFrame(self, frameSet):

        if frameSet == "active":

            if self.frame + 1 > len(self.activeFrames):

                self.frame = 0

            self.image = self.activeFrames[self.frame]
            self.frame += 1

        elif frameSet == "open":

            self.image = self.seqFrames[self.frame]
            self.frame += 1

            if self.frame + 1 > (len(self.seqFrames) - 1):

                self.frame = 0
                self.currentFrameSet = "active"

        elif frameSet == "close":

            if self.frame < 0:

                self.frame = 0
                self.image = Warp.defaultImage
                self.currentFrameSet = None

            else:

                self.image = self.seqFrames[self.frame]
                self. frame -= 1


    def setDefaultImage(self):
        """ set Warp.defaultImage, Warp.warpReadyImage, self.image, self.original """

        if not Warp.defaultImage:

            image = dinosInSpace.loadImage("warpClosed.png", (100,100), (0,0))
            image2 = dinosInSpace.loadImage("warpReady.png", (100,100), (0,0))

            Warp.defaultImage = image
            Warp.warpReadyImage = image2

        self.image = Warp.defaultImage
        self.original = self.image

    def setImagePairs(self):
        """ set Warp.imagePairDict, the unique letter warp pairs """

        if not Warp.imagePairDict:

            dictKey = 1

            for i in Warp.PAIRS:

                inFramesList = []
                outFramesList = []
                inSeqList = []
                outSeqList = []
                prefix = "000"

                for j in range(Warp.NUMFRAMES):

                    imgInFile = "warpOpenIn" + i + str(j) + ".png"
                    imgOutFile = "warpOpenOut" + i + str(j) + ".png"
                    imgIn = dinosInSpace.loadImage(imgInFile, (100,100), (0,0))
                    imgOut = dinosInSpace.loadImage(imgOutFile, (100,100), (0,0))

                    inFramesList.append(imgIn)
                    outFramesList.append(imgOut)

                for k in range(Warp.SEQFRAMES):

                    if k > 9:

                        prefix = "00"

                    inSeqFile = "warpInSeq" + i + prefix + str(k) + ".png"
                    outSeqFile = "warpOutSeq" + i + prefix + str(k) + ".png"
                    imgInSeq = dinosInSpace.loadImage(inSeqFile, (100,100), (0,0))
                    imgOutSeq = dinosInSpace.loadImage(outSeqFile, (100,100), (0,0))

                    inSeqList.append(imgInSeq)
                    outSeqList.append(imgOutSeq)

                Warp.imagePairDict[dictKey] = [inFramesList, outFramesList, False, inSeqList, outSeqList]
                dictKey += 1

    def resetAll(self, animate):
        """ setStates of linked warps to 'default' """

        if self.linkedWarp:

            if animate:

                self.linkedWarp.setState("default")

            else:

                Warp.resetImagePair(self.linkedWarp.warpNumIndex)
                self.linkedWarp.state = "default"
                self.linkedWarp.setWarpNumIndex(None)
                self.linkedWarp.image = Warp.defaultImage
                self.linkedWarp.currentFrameSet = None
                self.linkedWarp = None

        if animate:

            self.setState("default")

        else:

            Warp.resetImagePair(self.warpNumIndex)
            self.state = "default"
            self.setWarpNumIndex(None)
            self.image = Warp.defaultImage
            self.currentFrameSet = None
            self.linkedWarp = None

        Warp.readyForLink = None

    def setState(self, state):
        """ set self.state, self.image """

        self.state = state

        if state == "default":

            Warp.resetImagePair(self.warpNumIndex)
            self.setWarpNumIndex(None)
            self.linkedWarp = None

            self.currentFrameSet = "close"
            self.frame = Warp.SEQFRAMES - 1

        elif state == "ready":

            Warp.readyForLink = self
            self.linkedWarp = None
            self.image = Warp.warpReadyImage

        elif state == "enter":

            self.activeFrames = Warp.transferInFrames
            self.seqFrames = Warp.transferSeqFrames
            self.currentFrameSet = "open"
            self.frame = 0

        elif state == "exit":

            inFramesList, outFramesList, inSeqList, outSeqList, i = Warp.getImagePair()
            self.setWarpNumIndex(i)
            Warp.transferInFrames = inFramesList
            Warp.transferSeqFrames = inSeqList
            Warp.readyForLink.setState("enter")
            Warp.readyForLink.setLinkedWarp(self)
            Warp.readyForLink.setWarpNumIndex(i)
            self.setLinkedWarp(Warp.readyForLink)
            Warp.readyForLink = None
            self.activeFrames = outFramesList
            self.seqFrames = outSeqList
            self.currentFrameSet = "open"
            self.frame = 0

    def setWarpNumIndex(self, i):

        self.warpNumIndex = i

    def setLinkedWarp(self, w):

        self.linkedWarp = w

class Tracer(pygame.sprite.Sprite):
    """ Line from warp to cursor """

    traceFrom = None
    tracerGroup = pygame.sprite.RenderUpdates()
    color = (255,122,66)
    size = 1

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.clearImage()
        Tracer.tracerGroup.add(self)

    def update(self):

        if Tracer.traceFrom:

            if interface56.Cursor.isLinking:

                self.tracePath()

            else:

                Tracer.traceFrom = None
                self.clearImage()

    @staticmethod
    def wipe():

        Tracer.traceFrom = None
        Tracer.tracerGroup = pygame.sprite.RenderUpdates()

    @staticmethod
    def activate(traceFrom):

        Tracer.traceFrom = traceFrom

    def tracePath(self):
        """ draw a line from warp to cursor """

        abs = math.fabs
        mouseX, mouseY = pygame.mouse.get_pos()
        traceX, traceY = Tracer.traceFrom.rect.center
        w = abs(mouseX - traceX)
        h = abs(mouseY - traceY)

        if w < 3:

            w = 3

        if h < 3:

            h = 3

        self.image = pygame.Surface((w, h))
        self.image.fill((255,255,255))
        transparent = self.image.get_at((0,0))
        self.image.set_colorkey(transparent, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        imgW = self.image.get_width()
        imgH = self.image.get_height()
        c = Tracer.color
        s = Tracer.size

        if mouseX >= traceX and mouseY <= traceY:

            self.rect.bottomleft = (traceX, traceY)
            pygame.draw.line(self.image, c, (0, imgH), (imgW, 0), s)

        elif mouseX >= traceX and mouseY >= traceY:

            self.rect.topleft = (traceX, traceY)
            pygame.draw.line(self.image, c, (0, 0), (imgW, imgH), s)

        elif mouseX <= traceX and mouseY <= traceY:

            self.rect.bottomright = (traceX, traceY)
            pygame.draw.line(self.image, c, (imgW, imgH), (0, 0), s)

        elif mouseX <= traceX and mouseY >= traceY:

            self.rect.topright = (traceX, traceY)
            pygame.draw.line(self.image, c, (imgW, 0), (0, imgH), s)

    def clearImage(self):

        self.image = pygame.Surface((2,2))
        self.rect = self.image.get_rect()

def buildUserBlocks(game, keyList):
    """ Block instances created here """

    allChannels = []
    arrowGroup = pygame.sprite.RenderUpdates()

    for k in keyList:

        channelList = []
        objType = k[0]
        objColor = k[1]
        numToMake = k[2]

        for num in range(numToMake):

            if objType == "arrow": # make arrow block

                newObj = Arrow(objColor)
                channelList.append(newObj)
                arrowGroup.add(newObj)

            if objType == "warp": # make warp block
                newObj = Warp()
                channelList.append(newObj)

        allChannels.append(channelList)

    game.addGroup(Arrow.arrowGroup)
    game.addGroup(Arrow.maskGroup)
    game.addGroup(Warp.warpGroup)

    # pass data to other objects
    interface56.ItemMenu.assignData(allChannels)
    interface56.Cursor.setBlockData(allChannels, arrowGroup)

def wipe():

    Block.wipe()
    Arrow.wipe()
    Warp.wipe()
    Tracer.wipe()

if __name__ == "__main__":
    print "module for import only"

