""" interface56.py

    class
        Sprite

            GridBox
            Cursor
            Icon
            IconCounter
            IconOverBlock
            CursorCounter
            XGlyph
    function
        makeGridBox
        wipe

"""

import pygame
import block56
import static56
import groupMods56
import soundFx56
import scroller56
import radar56
import dinosInSpace
import infoGraphic56

ICON_FONTSIZE = 13

class ItemMenu(infoGraphic56.InfoGraphic):
    """ an Item Box which controlls object placement """

    allChannels = None # [[obj1, obj2...], [obj1...]...] -> [channellist[objlist]]
    numChannels = None # int -> total number of channels
    avaliableCount = None # [int, int, int...] -> obj per channel
    currentChannel = 0 # index base 0
    arrowBlocks = []
    width = None # for MessageStub
    height = None # for spawnInfoBox and MessageStub
    me = None

    def __init__(self, game):
        """ make ItemMenu graphic in topleft """

        infoGraphic56.InfoGraphic.__init__(self)

        self.ALPHA = 180
        self.ItemMenuGroup = pygame.sprite.OrderedUpdates(self)
        self.createIcons(game)
        self.game = game
        ItemMenu.me = self

    @staticmethod
    def wipe():

        ItemMenu.allChannels = None
        ItemMenu.numChannels = None
        ItemMenu.avaliableCount = None
        ItemMenu.currentChannel = 0
        ItemMenu.arrowBlocks = []
        ItemMenu.width = None
        ItemMenu.height = None
        ItemMenu.me = None

    @staticmethod
    def assignData(allChannels):
        """ assigns data to ItemMenu class based on object creation """

        ItemMenu.allChannels = allChannels
        ItemMenu.numChannels = len(allChannels)
        avaliableCount = []
        sprNum = 0

        for channel in allChannels:

            for spr in channel:

                sprNum += 1

            avaliableCount.append(sprNum)
            sprNum = 0

        ItemMenu.avaliableCount = avaliableCount

    @staticmethod
    def changeChannel(direction):
        """ cycle through currentChannel """

        if ItemMenu.numChannels > 1:

            soundFx56.GameSoundManager.registerSound("cycle")
            Cursor.breakRecover()

            if direction == "R":

                ItemMenu.currentChannel += 1

            elif direction == "L":

                ItemMenu.currentChannel -= 1

            # wrap
            if ItemMenu.currentChannel > ItemMenu.numChannels - 1:

                ItemMenu.currentChannel = 0

            elif ItemMenu.currentChannel < 0:

                ItemMenu.currentChannel = ItemMenu.numChannels - 1

            CursorCounter.setRenderTrue() # notify counter to change

        else:
            pass
##            soundFx56.GameSoundManager.registerSound("noRecover")

    @staticmethod
    def reqAddObj():
        """ request to add an object """

        mousePos = pygame.mouse.get_pos()
        count = ItemMenu.avaliableCount[ItemMenu.currentChannel] # number of objects avaliable of a selected type
        objPool = ItemMenu.allChannels[ItemMenu.currentChannel] # all objects avaliable of selected type

        if count > 0: # are there objects to place?

            if not Cursor.canRotate:  # is the cursor not over a rotatable obj?

                if not Cursor.canLink:

                    if Cursor.canPlace: # is the cursor free to place something?

                        if  hasattr(Cursor.theCursor, "rect") and hasattr(GridBox.activeUnit, "rect"):
                            if pygame.sprite.collide_rect(Cursor.theCursor, GridBox.activeUnit):
                                # is cursor colliding with a box of the grid?

                                soundFx56.GameSoundManager.registerSound("place") # the object will be placed

                                for obj in objPool: # find first obj not in use

                                    if not obj.active: # if it's not already in use

                                        addThis = obj

                                        break

                                addThis.placeMe(GridBox.activeUnit.rect.center) # place
                                count -= 1 # 1 less of this obj aval
                                ItemMenu.avaliableCount[ItemMenu.currentChannel] = count # sync
                                CursorCounter.setRenderTrue() # notify counters
                                IconCounter.setRenderNext(ItemMenu.currentChannel)
                            else:
                                pass
#                                print "Cursor.theCursor   " + str(Cursor.theCursor)
#                                print "GridBox.activeUnit    " + str(GridBox.activeUnit)


                    else: # play 'noPlace' sound
                        pass
##                        soundFx56.GameSoundManager.registerSound("noPlace")

        else:
            soundFx56.GameSoundManager.registerSound("noPlace")

    @staticmethod
    def reqRecObj():
        """ user requests to recover an object """

        recoverThis = block56.Block.canRecoverThis

        if recoverThis: # is there an object eligible for recovery?

            soundFx56.GameSoundManager.registerSound("pickUp") # play sound
            i = 0

            for objList in ItemMenu.allChannels: # get object channel

                if recoverThis in objList: # where is it?

                    useThisIndex = i # it's in in this channel
                    break

                i += 1

            ItemMenu.avaliableCount[useThisIndex] += 1 # player has +1 obj to use
            recoverThis.hideMe()    # hide and deactivate object
            CursorCounter.setRenderTrue()
            IconCounter.setRenderNext(useThisIndex)

        else:
            pass
##            soundFx56.GameSoundManager.registerSound("noRecover")

    @staticmethod
    def getWidth():

        return ItemMenu.width

    @staticmethod
    def getHeight():

        return ItemMenu.height

    def createIcons(self, game):
        """ creates icons and iconCounters based on placement objects """

        totalIcons = len(ItemMenu.allChannels)
        locations, ICONSIZE = self.formatLocation(totalIcons)
        icons = []
        counters = []
        i = 0

        for objList in ItemMenu.allChannels:

            icon = Icon(objList[0], locations[i], ICONSIZE)   # make icons
            iconCounter = IconCounter(i, locations[i], ICONSIZE) # make iconCounters
            icons.append(icon)
            counters.append(iconCounter)
            i += 1

        overBlock = IconOverBlock(ICONSIZE) # make icon highlight box
        border = IconMenuBorder(self.image.get_size())
        self.ItemMenuGroup.add(icons, overBlock, counters, border)
        game.addGroup(self.ItemMenuGroup)

    def formatLocation(self, totalIcons):
        """ gets location for each icon while createIcons runs """

        OFFSET = 4
        ICONSIZE = 26
        STEP = ICONSIZE + OFFSET
        x = OFFSET
        y = 20
        locations = []

        for i in range(totalIcons):

            locations.append((x, y))
            x += STEP

        w = x
        h = y + STEP + OFFSET
        ItemMenu.width = w
        ItemMenu.height = h
        self.image = pygame.Surface((w, h))
        self.image.fill((0,0,0))
        self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.top   = 0
        self.rect.left  = 0

        return locations, ICONSIZE # list of coordinates to place icons

class GridBox(pygame.sprite.Sprite):

    imgCanPlace = None
    imgNoPlace = None
    imgEmpty = None

    activeUnit = None # holds ref to the active grid box

    def __init__(self, game, loc):

        pygame.sprite.Sprite.__init__(self)

        self.minSpeed = game.getMinSpeed()
        self.loadImages()
        self.rect = pygame.Rect(0,0,98,98)
        self.rect.center = loc

    def update(self):

        self.setSpeed()
        self.checkCollision()

    @staticmethod
    def wipe():

        GridBox.activeUnit = None

    def loadImages(self):

        if not GridBox.imgCanPlace:

            image = dinosInSpace.loadImage("canPlace.png", (100,100), (50,50))
            GridBox.imgCanPlace = image

        if not GridBox.imgNoPlace:

            image = dinosInSpace.loadImage("noPlace.png", (100,100), (50,50))
            GridBox.imgNoPlace = image

        if not GridBox.imgEmpty:

            image = GridBox.imgCanPlace.copy()
            image.set_alpha(0, pygame.RLEACCEL)
            GridBox.imgEmpty = image

        self.image = GridBox.imgEmpty

    def setImage(self, state):

        if state == "empty":

            self.image = GridBox.imgEmpty

        if state == "canPlace":

            self.image = GridBox.imgCanPlace

        if state == "noPlace":

            self.image = GridBox.imgNoPlace

    def setSpeed(self):

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

    def checkCollision(self):

        cursor = pygame.sprite.spritecollide(self, Cursor.cursorGroup, False)

        if cursor:

            self.setImage("canPlace")
            GridBox.activeUnit = self

        else:

            self.setImage("empty")

class Cursor(pygame.sprite.Sprite):
    """ displays object to be placed, or action glyph """

    objGlyphs = [] # [surf1, surf2, surf3...] - obj.image
    actionGlyphs = [] # [hand, rotate... more to come] - images/surf
    arrowGroup = None # pygame group object (if there are arrows)
    cursorGroup = groupMods56.SR_OrderedUpdates()
    xGroup = pygame.sprite.RenderUpdates() # perhaps give this job to the xGlyph itself?
    isRecover = False
    canRotate = False
    canLink = False
    canTestSwitch = False
    isLinking = False
    isLooking = False
    canPlace = True
    theCursor = None # ref to the obj itself (will only be one)
    arrowGlyphFacing = 1 # 1-NORTH, 2-EAST, 3-SOUTH, 4-WEST
    testSwitchDown = False
    NUMCHAINFRAMES = 20
    overSpawn = False

    def __init__(self, game, _fps):

        pygame.sprite.Sprite.__init__(self)

        self.frame = 0
        self.setGlyphs()
        self.buildMe(game) # set starting image and add to game group
        self.bindXGlyph(game)
        self.setSpin(_fps)
        self.game = game
        self.firstCycle = True
        Cursor.theCursor = self

    def update(self):
        if not self.firstCycle:
            self.setPosition()
            self.checkCollision()
            self.setImage()
        else:
            self.firstCycle = False
            self.rect.center = (2000,2000)

    @staticmethod
    def hideDuringMessages():
        Cursor.theCursor.image.set_alpha(0)

    @staticmethod
    def showAfterMessages():
        Cursor.theCursor.image.set_alpha(255)

#
#    @staticmethod
#    def hideDuringMessages():
#        ## hide offscreen - to be called during displayMessage and endPuzzle in dinosInSpace
#        for spr in Cursor.cursorGroup:
#            print spr
#            spr.rect.center = (-2000,-2000)
#        for spr in Cursor.arrowGroup:
#            print spr
#            spr.rect.center = (-2000,-2000)
#        for spr in Cursor.xGroup:
#            print spr
#            spr.rect.center = (-2000,-2000)
#
    @staticmethod
    def wipe():

        Cursor.objGlyphs = []
        Cursor.arrowGroup = None
        Cursor.cursorGroup = groupMods56.SR_OrderedUpdates()
        Cursor.xGroup = pygame.sprite.RenderUpdates()
        Cursor.isRecover = False
        Cursor.canRotate = False
        Cursor.canLink = False
        Cursor.canTestSwitch = False
        Cursor.isLinking = False
        Cursor.isLooking = False
        Cursor.canPlace = True
        Cursor.theCursor = None
        Cursor.arrowGlyphFacing = 1
        Cursor.testSwitchDown = False
        Cursor.overSpawn = False

    @staticmethod
    def toggleRecover(isRecover):

##        soundFx56.GameSoundManager.registerSound("toggleRecover")
        Cursor.isRecover = isRecover

##        if Cursor.isRecover:
##            Cursor.isRecover = False
##        else:
##            Cursor.isRecover = True

    @staticmethod
    def setBlockData(allChannels, arrowGroup):
        """ store user block images / data to cursor """

        for channel in allChannels:

            image = channel[0].image.copy() # transp copy of image for each ch
            image.set_alpha(60, pygame.RLEACCEL)
            clas = channel[0].CLASS # object.CLASS (string)
            objPair = [image, clas]
            Cursor.objGlyphs.append(objPair)

        if arrowGroup:

            Cursor.arrowGroup = arrowGroup

    @staticmethod
    def getArrowGlyphFacing():
        """ arrow blocks call this during placeMe() """

        return Cursor.arrowGlyphFacing

    @staticmethod
    def reqRotateArrowL():
        """ called during Game.getInput() """

        Cursor.theCursor.rotateArrowL()

    @staticmethod
    def reqRotateArrowR():
        """ called during Game.getInput() """

        Cursor.theCursor.rotateArrowR()

    @staticmethod
    def getTopLeft():
        """ called by CursorCounter and XGlyph """

        x, y = Cursor.theCursor.rect.center
        x -= 50
        y -= 50

        return (x, y)

    @staticmethod
    def breakLink():

        Cursor.isLinking = False

    @staticmethod
    def breakRecover():

        Cursor.isRecover = False

    @staticmethod
    def setLooking(isLooking):

        Cursor.isLooking = isLooking

    @staticmethod
    def reqLink():

        Cursor.canLink = False
        Cursor.isLinking = True

    @staticmethod
    def reqTestSwitch():

        cursor = Cursor.theCursor
        swGroup = static56.Switch.switchGroup
        switches = pygame.sprite.spritecollide(cursor, swGroup, False)

        if switches: # should only be 1...

            Cursor.testSwitchDown = True

            for s in switches: # but iterate because switches is list

                s.flipSwitch(True, True)

    def setGlyphs(self):
        """ load and store 'action glyph' images """

        if not Cursor.actionGlyphs:

            recoverGlyph = self.loadImageFile("nHand.png")
            rotateGlyph = self.loadImageFile("nRotate2.png")
            eyeGlyph = self.loadImageFile("nEye.png")
            testSwitchGlyph = self.loadImageFile("nTestSwitch.png")
            testSwitchDownGlyph = self.loadImageFile("nTestSwitchDown.png")
            infoGlyph = self.loadImageFile("infoOver.png")

            linkOffFrames, linkOnFrames = self.loadChainFrames()

            Cursor.actionGlyphs.append(recoverGlyph) # 0
            Cursor.actionGlyphs.append(rotateGlyph) #1
            Cursor.actionGlyphs.append(linkOffFrames) #2
            Cursor.actionGlyphs.append(linkOnFrames) #3
            Cursor.actionGlyphs.append(eyeGlyph) #4
            Cursor.actionGlyphs.append(testSwitchGlyph) #5
            Cursor.actionGlyphs.append(testSwitchDownGlyph)#6
            Cursor.actionGlyphs.append(infoGlyph) # 7

    def loadImageFile(self, file):

        image = dinosInSpace.loadImage(file, (100,100), (0,0))

        return image

    def loadChainFrames(self):
        """ return chainOffFrames, chainOnFrames """

        chainOffFrames = []
        chainOnFrames = []

        prefix = "000"

        for i in range(Cursor.NUMCHAINFRAMES):

            if i > 9:

                prefix = "00"

            file1 = "nChainOff" + prefix + str(i) + ".png"
            file2 = "nChainOn" + prefix + str(i) + ".png"
            img1 = self.loadImageFile(file1)
            img2 = self.loadImageFile(file2)

            chainOffFrames.append(img1)
            chainOnFrames.append(img2)

        return chainOffFrames, chainOnFrames

    def buildMe(self, game):
        """ get starting image and rect, called at init """

        self.image = Cursor.objGlyphs[0][0]
        self.rect = pygame.Rect(0,0,1,1)

        Cursor.cursorGroup.add(self)
        game.addGroup(Cursor.cursorGroup)

    def bindXGlyph(self, game):
        """ make XGlyph object and bind to self, called at init """

        xGlyph = XGlyph()
        Cursor.xGroup.add(xGlyph)
        game.addGroup(Cursor.xGroup)

    def setPosition(self):
        """ set cursor position / store position data """

        mousePos = pygame.mouse.get_pos()
        self.rect.center = mousePos

    def setImage(self):
        """ set correct cursor image """

        if Cursor.overSpawn:

            self.image = Cursor.actionGlyphs[7]
            CursorCounter.visible = False
            XGlyph.hideMe()

        elif Cursor.testSwitchDown:

            self.image = Cursor.actionGlyphs[6]
            CursorCounter.visible = False
            XGlyph.hideMe()

        elif Cursor.canTestSwitch:

            self.image = Cursor.actionGlyphs[5]
            CursorCounter.visible = False
            XGlyph.hideMe()

        elif Cursor.isLooking:

            self.image = Cursor.actionGlyphs[4]
            CursorCounter.visible = False
            XGlyph.hideMe()

        elif Cursor.isLinking:

            self.image = self.animate(Cursor.actionGlyphs[3])
            CursorCounter.visible = False
            XGlyph.hideMe()

        elif Cursor.isRecover:

            self.image = Cursor.actionGlyphs[0] # show recover hand glyph
            CursorCounter.visible = False
            XGlyph.hideMe()

        else:

            if Cursor.canRotate:

                self.spin() # rotate glyph
                CursorCounter.visible = False
                XGlyph.hideMe()

            elif Cursor.canLink:

                self.image = self.animate(Cursor.actionGlyphs[2])
                CursorCounter.visible = False
                XGlyph.hideMe()

            else:

                if Cursor.canPlace:

                    XGlyph.hideMe()

                else:

                    XGlyph.showMe() # can't place

                self.image = Cursor.objGlyphs[ItemMenu.currentChannel][0] # box to be placed
                CursorCounter.visible = True

    def animate(self, frameList):
        """ return image """

        image = frameList[self.frame]
        self.frame += 1

        if self.frame > (len(frameList) - 1):

            self.frame = 0

        return image

    def checkCollision(self):
        """ check if over placed blocks - if so, change state  """

        collisionSpawn = False
        collisionArrow = False
        collisionWarp = False
        collisionSwitch = False
        collisionOther = False
        colAny = pygame.sprite.spritecollideany
        hasCollide = False

        if not Cursor.isLinking:

            if not Cursor.isRecover:


                if static56.Spawn.spawnGroup and not hasCollide:

                    if colAny(self, static56.Spawn.spawnGroup):

                        collisionSpawn = True
                        hasCollide = True

                if Cursor.arrowGroup and not hasCollide:

                    if colAny(self, Cursor.arrowGroup):

                        collisionArrow = True
                        collisionWarp = False

                        hasCollide = True

                if block56.Warp.warpGroup and not hasCollide:

                    if colAny(self, block56.Warp.warpGroup):

                        collisionWarp = True
                        collisionArrow = False

                        hasCollide = True

                if static56.Switch.switchGroup and not hasCollide:

                    if colAny(self, static56.Switch.switchGroup):

                        collisionSwitch = True

                        hasCollide = True

                if static56.Goal.goalGroup \
                    or static56.StaticArrow.sArrowGroup \
                    or static56.Mine.mineGroup \
                    or static56.StaticArrowL.sArrowLGroup:

                    if not hasCollide:

                        if colAny(self, static56.Goal.goalGroup) \
                            or colAny(self, static56.StaticArrow.sArrowGroup) \
                            or colAny(self, static56.Mine.mineGroup) \
                            or colAny(self, static56.StaticArrowL.sArrowLGroup):

                            collisionOther = True
                            collisionArrow = False
                            collisionWarp = False
                            collisionSpawn = False

                            hasCollide = True

            if collisionSpawn:

                Cursor.overSpawn = True

                Cursor.canRotate = False
                Cursor.canLink = False
                Cursor.canTestSwitch = False
                Cursor.canPlace = False

            elif collisionArrow:

                Cursor.canRotate = True

                Cursor.overSpawn = False
                Cursor.canLink = False
                Cursor.canTestSwitch = False
                Cursor.canPlace = False

            elif collisionWarp:

                Cursor.canLink = True

                Cursor.overSpawn = False
                Cursor.canRotate = False
                Cursor.canTestSwitch = False
                Cursor.canPlace = False

            elif collisionSwitch:

                if self.game.mode == "puzzle" and not self.game.lock:

                    Cursor.canTestSwitch = True

                elif self.game.mode == "action" and self.game.lock:

                    Cursor.canTestSwitch = True

                else:

                    Cursor.overSpawn = False
                    Cursor.canTestSwitch = False

                Cursor.overSpawn = False
                Cursor.canLink = False
                Cursor.canRotate = False
                Cursor.canPlace = False

            elif collisionOther:

                Cursor.overSpawn = False
                Cursor.canPlace = False
                Cursor.canLink = False
                Cursor.canRotate = False
                Cursor.canTestSwitch = False

            else:

                Cursor.overSpawn = False
                Cursor.canRotate = False
                Cursor.canLink = False
                Cursor.canTestSwitch = False
                Cursor.canPlace = True

        else:

            Cursor.overSpawn = False
            Cursor.canPlace = False
            Cursor.canLink = False
            Cursor.canRotate = False
            Cursor.canTestSwitch = False

    def rotateArrowL(self):
        """ rotate arrow cursor L (if avaliable) before placement """

        clas = Cursor.objGlyphs[ItemMenu.currentChannel][1]

        if  clas == "Arrow":

            soundFx56.GameSoundManager.registerSound("rotate")

            for pair in Cursor.objGlyphs:

                if pair[1] == "Arrow":

                    pair[0] = pygame.transform.rotate(pair[0], 90)

            Cursor.arrowGlyphFacing -= 1

            if Cursor.arrowGlyphFacing < 1:

                Cursor.arrowGlyphFacing = 4

    def rotateArrowR(self):
        """ rotate arrow cursor R (if avaliable) before placement """

        clas = Cursor.objGlyphs[ItemMenu.currentChannel][1]

        if  clas == "Arrow":

            soundFx56.GameSoundManager.registerSound("rotate")

            for pair in Cursor.objGlyphs:

                if pair[1] == "Arrow":

                    pair[0] = pygame.transform.rotate(pair[0], -90)

            Cursor.arrowGlyphFacing += 1

            if Cursor.arrowGlyphFacing > 4:

                Cursor.arrowGlyphFacing = 1

    def setSpin(self, _fps):
        """ initiate spin cycle """

        self.spinStep = -12
        if _fps == 60:
            self.spinStep = -6
        self.spinDistance = 0

    def spin(self):
        """ rotate image -- now with colors """

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

        image = Cursor.actionGlyphs[1]  # get the colored image
        self.image = rotate(image, self.spinDistance)

class Icon(infoGraphic56.InfoGraphic):
    """ icon displayed on ItemMenu bar representing placement objects """

    locations = [] # [(x, y), (x, y)...]

    def __init__(self, obj, location, ICONSIZE):

        infoGraphic56.InfoGraphic.__init__(self)
        self.ALPHA = 255
        self.setImage(obj, ICONSIZE)
        (x, y) = location
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        Icon.locations.append((x, y))

    def setImage(self, obj, ICONSIZE):

        getAt = (0,0)
        scaleTo = (ICONSIZE, ICONSIZE)

        if obj.CLASS == "Warp":

            self.image = dinosInSpace.loadImage("warpIcon.png", scaleTo, getAt)

        elif obj.CLASS == "Arrow":

            if obj.objColor == "green":

                self.image = dinosInSpace.loadImage("ArrIconG.png", scaleTo, getAt)

            elif obj.objColor == "blue":

                self.image = dinosInSpace.loadImage("ArrIconB.png", scaleTo, getAt)

            elif obj.objColor == "red":

                self.image = dinosInSpace.loadImage("ArrIconR.png", scaleTo, getAt)

            elif obj.objColor == "yellow":

                self.image = dinosInSpace.loadImage("ArrIconY.png", scaleTo, getAt)

            else:

                self.image = dinosInSpace.loadImage("ArrIconW.png", scaleTo, getAt)



    @staticmethod
    def wipe():

        Icon.locations = []

    @staticmethod
    def getLocation(channel):
        """ get location of current channel for highlight box """

        loc = Icon.locations[channel]
        return loc

class IconCounter(infoGraphic56.InfoGraphic):
    """ number displayed above icon showing count """

    allIconCounters = {} # {ch1 : obj1, ch2 : obj2...}
    renderNext = None
    channel = None

    def __init__(self, channel, location, ICONSIZE):
        infoGraphic56.InfoGraphic.__init__(self)

        self.ALPHA = 255
        IconCounter.allIconCounters[channel] = self
        self.font = dinosInSpace.FontBank.getFont(ICON_FONTSIZE)
        self.image = self.renderCount(channel)
        self.rect = self.image.get_rect()
        (x, y) = location
        y -= 8
        x += (ICONSIZE / 2)
        self.rect.center = (x, y)

        self.originalCenter = self.rect.center

    def update(self):
        if IconCounter.renderNext == self and infoGraphic56.InfoGraphic.visible:
            self.image = self.renderCount(IconCounter.channel)

        if infoGraphic56.InfoGraphic.visible:
            self.rect.center = self.originalCenter
        else:
            self.rect.center = (-200,-200)


    @staticmethod
    def wipe():
        IconCounter.allIconCounters = {}
        IconCounter.renderNext = None
        IconCounter.channel = None

    @staticmethod
    def setRenderNext(channel):
        """ called by init and ItemMenu when counter needs to be rendered """
        IconCounter.renderNext = IconCounter.allIconCounters[channel]
        IconCounter.channel = channel

    def renderCount(self, channel):
        count = ItemMenu.avaliableCount[channel]
        image = self.font.render(str(count), True, (255,255,255))
        IconCounter.renderNext = None # don't render again until we need to

        return image

class IconOverBlock(infoGraphic56.InfoGraphic):
    """ highlighted box over icon that indicates selected item """

    def __init__(self, ICONSIZE):

        infoGraphic56.InfoGraphic.__init__(self)
        self.ALPHA = 255
        self.ICONSIZE = ICONSIZE
        scaleTo = (ICONSIZE + 1, ICONSIZE + 1)
        self.image = dinosInSpace.loadImage("iconOver.png", scaleTo, (0,0))
        self.rect = self.image.get_rect()

    def update(self):
        """ sync w/ current channel """

        channel = ItemMenu.currentChannel # get channel from ItemMenu
        (x, y) = Icon.getLocation(channel) # get loc from Icon
        x += (self.ICONSIZE / 2)
        y += (self.ICONSIZE / 2)
        self.rect.center = (x, y)

class IconMenuBorder(infoGraphic56.InfoGraphic):

    def __init__(self, size):
        infoGraphic56.InfoGraphic.__init__(self)

        self.ALPHA = 255
        image = pygame.Surface(size)
        image.fill((0,0,0))
        col = image.get_at((0,0))
        image.set_colorkey(col, pygame.RLEACCEL)
        r = image.get_rect()
        pygame.draw.rect(image, (255,255,255), r, 2)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

class CursorCounter(pygame.sprite.Sprite):
    """ the counter graphic to be displayed on the cursor glyph """

    needRender = False
    visible = True
    me = None

    def __init__(self, game):
        """ create font, give group to game """

        pygame.sprite.Sprite.__init__(self)
        self.COLOR = (0,0,255)
        self.font = dinosInSpace.FontBank.getFont(22)
        self.image = self.renderCount()
        self.rect = self.image.get_rect()
        countGroup = pygame.sprite.RenderUpdates(self)
        game.addGroup(countGroup)
        CursorCounter.me = self

    def update(self):
        """ change image if needed, follow mouse, or hide """

        if CursorCounter.needRender:    # re-render if state changes
            self.image = self.renderCount()
        if CursorCounter.visible == True:   # display on glyph
            self.rect.topleft = Cursor.getTopLeft()
        else:   # hide offscreen if cursor is not an obj glyph
            self.rect.center = (-100,-100)

    @staticmethod
    def wipe():

        CursorCounter.needRender = False
        CursorCounter.visible = True
        CursorCounter.me = None

    @staticmethod
    def setRenderTrue():
        """ called by init and ItemMenu when counter needs to be rendered """

        CursorCounter.needRender = True

    def renderCount(self):
        """ take the object count from ItemMenu and render into new surface """

        count = ItemMenu.avaliableCount[ItemMenu.currentChannel]
        image = self.font.render(str(count), True, self.COLOR)
        CursorCounter.needRender = False # don't render again until we need to

        return image

class XGlyph(pygame.sprite.Sprite):
    """ displayed over cursor if can't place item """

    visible = False
    OFFSCREEN = (-200,-200)
    currentXGlyph = None

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = dinosInSpace.loadImage("noGo.png", (100,100), (50,10))
        self.rect = self.image.get_rect()
        XGlyph.currentXGlyph = self

    def update(self):

        if XGlyph.visible:

            self.rect.topleft = Cursor.getTopLeft()

        else:

            self.rect.center = XGlyph.OFFSCREEN

    @staticmethod
    def wipe():

        XGlyph.visible = False
        XGlyph.currentXGlyph = None

    @staticmethod
    def showMe():

        XGlyph.visible = True

    @staticmethod
    def hideMe():

        XGlyph.visible = False

def makeGridBox(game, gridSize):
    gbGroup = groupMods56.SR_OrderedUpdates()

    (x, y) = radar56.Radar.getTrackerLoc() # topleft of field
    (w, h) = scroller56.Scroller.getFieldBounds() # field size
    x += 50
    y += 50
    xStep, yStep = gridSize # num of boxes to make
    xOriginal = x

    for i in range(yStep):
        for j in range(xStep):
            gb = GridBox(game, (x, y))
            gbGroup.add(gb)
            x += 100

        x = xOriginal
        y += 100

    game.addGroup(gbGroup)


def wipe():

    ItemMenu.wipe()
    Icon.wipe()
    IconCounter.wipe()
    IconOverBlock.wipe()
    Cursor.wipe()
    CursorCounter.wipe()
    XGlyph.wipe()
    GridBox.wipe()

CLASS_LIST = [
    ItemMenu,
    GridBox,
    Cursor,
    Icon,
    IconCounter,
    CursorCounter
]

##def hideCursorCounter():
##    """ for endmessage run state access """
##    CursorCounter.me.rect.center = (2000,2000)
##

def hideCursorItems():
    """ for endmessage run state access """
    if CursorCounter.me:
        CursorCounter.me.rect.center = (2000,2000)
    if XGlyph.currentXGlyph:
        XGlyph.currentXGlyph.rect.center = (2000,2000)

if __name__ == "__main__":
    print "module for import only"



