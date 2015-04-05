""" userMaps """
import pygame
import dinosInSpace
import os
import dataStorage56
import cannon
import groupMods56
import random
import spriteBasic
import gfx56
import screenWipe
import infoGraphic56
import soundFx56

DARKYEL = (183,171,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (150,150,150)
BLUE = (0,0,255)
GREEN = (0,255,0)

STD_FSIZE = 20
BUTTON_FONTSIZE = 16

TOPBUFF = 10

# ------------------------------------------- complete overlay
COMP_TEXTSIZE = 20
COMP_HEIGHT = 50

# --------------------------------------------colors
COL_BACKGROUND = BLACK
COL_MAPBUTTON_OFF = BLACK
COL_MAPBUTTON_ON = DARKYEL
COL_MAPBUTTON_TXT = WHITE
COL_MAPBOX = BLACK
COL_EXIT_OFF = GREY
COL_EXIT_ON = DARKYEL
COL_EXIT_TXT= COL_BACKGROUND
COL_RECTS = WHITE

# --------------------------------------------canons

INT_FLYERDELAY = 0
INT_FLYERVAR = 0
INT_FLYERSPD = 0
INT_FLYERSPIN = 0

# -------------------------------------------- wavething
WAVE_NUMFRAMES = 13
WAVE_DELAY = 3
WAVE_CENTER = (600, 100)
WAVE_SIZE = (200, 80) # after scaled 2x... for antenae placement on background only

class UserImgLib(object):

    imgDict = None

    def __init__(self):
        if not UserImgLib.imgDict:

            STARSMALL, STARMED, STARBIG = self.makeStars()

            SPINNER_ADD = dinosInSpace.loadImage("spinnerAdd.png", "2X", (0,0))
            SPINNER_SUB = dinosInSpace.loadImage("spinnerSub.png", "2X", (0,0))
            SPINNER_ADD_B = dinosInSpace.loadImage("spinnerAddBlack.png", "2X", (0,0))
            SPINNER_SUB_B = dinosInSpace.loadImage("spinnerSubBlack.png", "2X", (0,0))
            SCROLLUP = dinosInSpace.loadImage("fileScrollUp.png", "2X", (0,0))
            SCROLLDOWN = dinosInSpace.loadImage("fileScrollDown.png", "2X", (0,0))
            GRID_SPN_UP = dinosInSpace.loadImage("gridSpnUp.png", "2X", (0,0))
            GRID_SPN_DOWN = dinosInSpace.loadImage("gridSpnDown.png", "2X", (0,0))
            USERUP = dinosInSpace.loadImage("userScrollUp.png", "2X", (0,0))
            USERDOWN = dinosInSpace.loadImage("userScrollDown.png", "2X", (0,0))
            ROCK = dinosInSpace.loadImage("rock2.png", "2X", (0,0))
            FLYERGREENSMALL = dinosInSpace.loadImage("flyerGreen.png", None, (0,0))
            FLYERGREEN = dinosInSpace.loadImage("flyerGreen.png", "2X", (0,0))
            FLYERGREENMED = dinosInSpace.loadImage("flyerGreen.png", (75,75), (0,0))
            FLYERGREENBIG = dinosInSpace.loadImage("flyerGreen.png", (100,100), (0,0))
            NEW_MAP = dinosInSpace.loadImage("newMapTest.png", None, None)
            COMPLETE = dinosInSpace.loadImage("testUserMapComplete.png", (400,300), None, 100)
            PREVIEW = dinosInSpace.loadImage("userPreviewDefault.png", "2X")
            PREVBOTTOM = dinosInSpace.loadImage("userPreviewBottom.png", "2X", (0,0))
            PREVTOP = dinosInSpace.loadImage("userPreviewTop.png", "2X", (0,0))

            # to animate

            DINOG1 = dinosInSpace.loadImage("dCG1.png", "2X", (0,0))
            DINOG2 = dinosInSpace.loadImage("dCG2.png", "2X", (0,0))
            DINOG1b = dinosInSpace.loadImage("dCG1b.png", "2X", (0,0))
            DINOG2b = dinosInSpace.loadImage("dCG2b.png", "2X", (0,0))

            UserImgLib.imgDict = {
                "STARSMALL" : STARSMALL,
                "STARMED" : STARMED,
                "STARBIG" : STARBIG,

                "SPINNER_ADD" : SPINNER_ADD,
                "SPINNER_SUB" : SPINNER_SUB,
                "SPINNER_ADD_B" : SPINNER_ADD_B,
                "SPINNER_SUB_B": SPINNER_SUB_B,
                "SCROLLUP" : SCROLLUP,
                "SCROLLDOWN" : SCROLLDOWN,
                "GRID_SPN_DOWN" : GRID_SPN_DOWN,
                "GRID_SPN_UP" : GRID_SPN_UP,
                "USERUP" : USERUP,
                "USERDOWN" : USERDOWN,
                "ROCK" : ROCK,
                "FLYERGREENSMALL" : FLYERGREENSMALL,
                "FLYERGREEN" : FLYERGREEN,
                "FLYERGREENMED" : FLYERGREENMED,
                "FLYERGREENBIG" : FLYERGREENBIG,
                "NEW_MAP" : NEW_MAP,
                "COMPLETE" : COMPLETE,
                "PREVIEW" : PREVIEW,
                "PREVBOTTOM" : PREVBOTTOM,
                "PREVTOP" : PREVTOP,

                "DINOG1" : DINOG1,
                "DINOG2" : DINOG2,
                "DINOG1b" : DINOG1b,
                "DINOG2b" : DINOG2b
            }

    @staticmethod
    def getImage(name):
        if name in UserImgLib.imgDict:
            return UserImgLib.imgDict[name].copy()

    def makeStars(self):
        STARSMALL = pygame.Surface((2,2))
        STARMED = pygame.Surface((3,3))
        STARBIG = pygame.Surface((4,4))

        STARSMALL.fill(COL_RECTS)
        STARMED.fill(COL_RECTS)
        STARBIG.fill(COL_RECTS)

        return STARSMALL, STARMED, STARBIG

class UserLauncher(object):
    """ state that runs before user maps are launched """

    me = None

    def __init__(self, BOXSIZE, LBOX_TOPLEFT, FONTSIZE):
        self.screen = pygame.display.get_surface()
        self.bkg = pygame.Surface(self.screen.get_size())
        self.bkg.fill(COL_BACKGROUND)

        terminal = UserImgLib.getImage("PREVBOTTOM")
        tip = UserImgLib.getImage("PREVTOP")
        self.bkg.blit(terminal, (self.screen.get_width() - terminal.get_width(), self.screen.get_height() - terminal.get_height() - 50))
        self.bkg.blit(tip, (600 - WAVE_SIZE[0]/2, WAVE_CENTER[1]))
        self.bkg.blit(tip, (600 + WAVE_SIZE[0]/2 - 8, WAVE_CENTER[1]))

        self.screen.blit(self.bkg, (0,0))

        self.flyerGroup = groupMods56.SR_OrderedUpdates()
        self.maskGroup = pygame.sprite.RenderUpdates()
        self.FB_group = pygame.sprite.RenderUpdates()
        self.ES_group = pygame.sprite.OrderedUpdates()
        self.mapsGroup = pygame.sprite.RenderUpdates()
        self.cursorGroup = pygame.sprite.GroupSingle()
        self.loadData = None # map data to load is stored here if requested

        # boxes to be drawn
        self.BOXSIZE = BOXSIZE
        self.LBOX_TOPLEFT = LBOX_TOPLEFT
        self.FONTSIZE = FONTSIZE

        bttn_w = UserImgLib.getImage("SPINNER_ADD").get_width()

        self.lbox = pygame.rect.Rect(self.LBOX_TOPLEFT, self.BOXSIZE)
        self.fileBox = pygame.rect.Rect((self.LBOX_TOPLEFT[0] + 6, self.LBOX_TOPLEFT[1] + FONTSIZE + 6), (self.BOXSIZE[0] - bttn_w - 12, self.BOXSIZE[1] - FONTSIZE - 12))

        self.cannons = [] # use addCannnon to add

        UserLauncher.me = self

    @staticmethod
    def wipe():
        UserLauncher.me = None

    @staticmethod
    def getFileBounds():
        bottom = UserLauncher.me.LBOX_TOPLEFT[1] + UserLauncher.me.FONTSIZE + TOPBUFF
        top = bottom - UserLauncher.me.FONTSIZE + UserLauncher.me.BOXSIZE[1] - TOPBUFF
#        bottom = STD_FSIZE + TOPBUFF
#        top = 600 - STD_FSIZE

        return top, bottom

    @staticmethod
    def addObject(obj):
        UserLauncher.me.ES_group.add(obj)

    @staticmethod
    def addSpriteToGroup(spr, group):
        if group == "MAPS":
            UserLauncher.me.mapsGroup.add(spr)
        elif group == "CURSOR":
            UserLauncher.me.cursorGroup.add(spr)
        else:
            print "addSpriteToGroup error: unrecognized group"

    @staticmethod
    def addFB(obj):
        UserLauncher.me.FB_group.add(obj)

    @staticmethod
    def setLoadData(loadData):
        UserLauncher.me.loadData = loadData

    def getFlyerGroup(self):
        return self.flyerGroup

    def addCannonList(self, cList):
        for c in cList:
            self.cannons.append(c)

    def removeCannon(self, c):
        self.cannons.remove(c)

    def addMask(self, m):
        self.maskGroup.add(m)

    def runMe(self, _fps, imageFrom, swipeDirection):
        clock = pygame.time.Clock()
        dest = None

        while not dest:
            clock.tick(_fps)
            dest = self.getInput()

            for c in self.cannons:
                c.update()

##            self.flyerGroup.clear(self.screen, self.bkg)
            self.maskGroup.clear(self.screen, self.bkg)
            self.FB_group.clear(self.screen, self.bkg)
            self.ES_group.clear(self.screen, self.bkg)
            self.cursorGroup.clear(self.screen, self.bkg)

##            self.flyerGroup.update()
            self.maskGroup.update()
            self.FB_group.update()
            self.ES_group.update()
            self.cursorGroup.update()

##            self.flyerGroup.draw(self.screen)
            self.maskGroup.draw(self.screen)
            self.FB_group.draw(self.screen)
            self.ES_group.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), swipeDirection)
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, self.bkg)

        self.flyerGroup.draw(self.screen)
        self.maskGroup.draw(self.screen)
        self.FB_group.draw(self.screen)
        self.ES_group.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        soundFx56.SoundPlayer.requestSound("woosh_b")
        return dest, snapshot

    def getInput(self):
        dest = None

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dest = "_EXIT"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    dest = UserCursor.me.checkPressed()

        return dest

class UserButton(pygame.sprite.Sprite):
    """ basic text button for user map screen """

    def __init__(self, size, color0, color1, text, fontSize, fontColor, topLeft, myDest):

        pygame.sprite.Sprite.__init__(self)
        self.mouseOver = False
        self.makeButtons(size, color0, color1, text, fontSize, fontColor)
        self.image = self.imgOff
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft
        self.myDest = myDest

        if self.__class__ != UserMapButton: # use addFB to place in bkg group
            UserLauncher.me.addObject(self)

    def update(self):
        if pygame.sprite.collide_rect(self, UserCursor.me):
            self.image = self.imgOn
            self.mouseOver = True

        else:
            self.image = self.imgOff
            self.mouseOver = False

    def makeButtons(self, size, color0, color1, text, fontSize, fontColor):

        self.imgOff = pygame.Surface(size)
        self.imgOff.fill(color0)
        self.imgOn = pygame.Surface(size)
        self.imgOn.fill(color1)
        font = dinosInSpace.FontBank.getFont(fontSize)
        text = font.render(text, True, fontColor)
        textBlitX = ( size[0] - text.get_width() ) / 2
        textBlitY = ( size[1] - text.get_height() ) / 2
        self.imgOff.blit(text, (textBlitX, textBlitY))
        self.imgOn.blit(text, (textBlitX, textBlitY))

    def getDest(self):

        return self.myDest

class UserMapButton(UserButton):
    """ each is a link to play a user map """
    mapsRecord = None

    def __init__(self, master, size, color0, color1, colorDel, text, fontSize, fontColor, topLeft, myDest, mapData):
        UserButton.__init__(self, size, color0, color1, text, fontSize, fontColor, topLeft, myDest)

        if not UserMapButton.mapsRecord:
            UserMapButton.mapsRecord = dataStorage56.getUserMapsRecord()

        UserLauncher.me.addFB(self)
        UserLauncher.addSpriteToGroup(self, "MAPS")
        self.STEP = 8
        self.mapData = mapData
        self.mapName = text
        self.master = master
        self.previewImg = self.requestPreviewImg()

    def update(self):
        """ override to inlcude map preview """
        top, bottom = UserLauncher.getFileBounds()
        if self.rect.centery > bottom and self.rect.centery < top and pygame.sprite.collide_rect(self, UserCursor.me):
            self.image = self.imgOn
            self.mouseOver = True
            MapPreviewImage.me.setImage(self.previewImg)

        else:
            self.image = self.imgOff
            self.mouseOver = False

    def getMapName(self):
        return self.mapName

    def move(self, direction):
        if direction == "UP":
            self.rect.centery -= self.STEP
        elif direction == "DOWN":
            self.rect.centery += self.STEP

    def requestPreviewImg(self):
        image = None

        for r in UserMapButton.mapsRecord:
            if r == self.mapName:
                image = dataStorage56.getDynamicImage(self.mapName, "PLAY")

                # overlay 'complete' if player has solved
                if UserMapButton.mapsRecord[r]:
                    # make text box
                    frame = pygame.Surface((400,COMP_HEIGHT))
                    frame.fill(GREEN)
                    text = infoGraphic56.TextObject("COMPLETE", COMP_TEXTSIZE, BLACK).image
                    textBox = gfx56.centerBlit(frame, text)
                    textBox.set_alpha(150, pygame.RLEACCEL)

                    # overlay
                    image.blit(textBox, (0, image.get_height()/2 - COMP_HEIGHT/2))
                break

        if not image:
            image = spriteBasic.BasicRect((400,300), BLUE, None, 4, None, True).image

            # make text box
            frame = pygame.Surface((400,COMP_HEIGHT))
            frame.fill(BLUE)
            text = infoGraphic56.TextObject("NEW MAP", COMP_TEXTSIZE, WHITE).image
            textBox = gfx56.centerBlit(frame, text)

            # overlay
            image.blit(textBox, (0, image.get_height()/2 - COMP_HEIGHT/2))

            ##image = UserImgLib.getImage("NEW_MAP")

        return image

    @staticmethod
    def wipe():
        UserMapButton.mapsRecord = None

class MapPreviewImage(pygame.sprite.Sprite):
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        MapPreviewImage.me = self
##        self.EMPTY_IMG = pygame.Surface((400,300))
##        self.EMPTY_IMG.fill((0,0,0))
        self.EMPTY_IMG = UserImgLib.getImage("PREVIEW")
        self.image = self.EMPTY_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (600,300)

    def update(self):
        if self.image != self.EMPTY_IMG:
            if not pygame.sprite.spritecollideany(UserCursor.me, UserLauncher.me.mapsGroup):
                self.setImage(self.EMPTY_IMG)
            if pygame.mouse.get_pos()[1] > 546: ## bugfix
                self.setImage(self.EMPTY_IMG)

    def setImage(self, image):
        self.image = image

    def clearImage(self):
        self.image = self.EMPTY_IMG

    @staticmethod
    def wipe():
        MapPreviewImage.me = None

class UserMapScroller(object):
    """ generates and keeps track of user map buttons """

    me = None

    def __init__(self):
        UserMapScroller.me = self
        self.userButtonList = []

        self.BUTTON_W = UserLauncher.me.fileBox.width
        self.BUTTON_H = 40
        self.BUTTON_X = UserLauncher.me.fileBox.left
        self.BUTTON_Y = UserLauncher.me.fileBox.top
        self.BOTTOM = UserLauncher.me.fileBox.bottom

        self.head = None # scroller bounds
        self.tail = None

    @staticmethod
    def wipe():
        UserMapScroller.me = None

    def scroll(self, direction):
        if self.userButtonList:
            if direction == "DOWN":
                if self.head.rect.top < self.BUTTON_Y: # BUTTON_Y == top of gridbox
                    for b in self.userButtonList:
                        b.move(direction)
            else:
                if self.tail.rect.bottom > self.BOTTOM:
                    for b in self.userButtonList:
                        b.move(direction)

    def makeUserButtons(self):
        size = (self.BUTTON_W, self.BUTTON_H)
        colorDel = (255,0,0)
        fontSize = 16
        fontColor = (255,255,255)
        myDest = "LOAD"
        x = self.BUTTON_X
        y = self.BUTTON_Y

        os.chdir("maps")
        os.chdir("user")
        fileList = os.listdir(".")
        fileList.sort()

        os.chdir("..")
        os.chdir("..")

        if fileList:
            for f in fileList:
                if f[-4:] == ".dat":
                    mapName = f[:-4]
                    topLeft = (x,y)
                    mapData = dataStorage56.getMap(mapName, True)

                    b = UserMapButton( self, size, COL_MAPBUTTON_OFF, COL_MAPBUTTON_ON, colorDel, mapName, fontSize, COL_MAPBUTTON_TXT, topLeft, myDest, mapData)
                    self.userButtonList.append(b)
                    y += self.BUTTON_H

        if self.userButtonList:
            self.head = self.userButtonList[0]
            self.tail = self.userButtonList[-1]

class UserMapScrollerButton(pygame.sprite.Sprite):
    """ button that controlls the user map buttons (links to user maps) """

    def __init__(self, surf, topLeft, direction):

        pygame.sprite.Sprite.__init__(self)
        self.imgOff = surf
        self.image = self.imgOff
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft
        self.direction = direction
        self.mouseOver = False
        self.makeOverImg()

    def update(self):
        if pygame.sprite.collide_rect(self, UserCursor.me):
            self.mouseOver = True
            self.image = self.imgOn
        else:
            self.mouseOver = False
            self.image = self.imgOff
        if self.mouseOver:
            UserMapScroller.me.scroll(self.direction)

    def makeOverImg(self):
        if self.direction == "DOWN":
            self.imgOn = dinosInSpace.loadImage("userUpOver.png", "2X", (0,0))
        else:
            self.imgOn = dinosInSpace.loadImage("userDownOver.png", "2X", (0,0))

class UserCursor(pygame.sprite.Sprite):
    image = None
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not UserCursor.image:
            UserCursor.image = dinosInSpace.loadImage("controlCursor.png", "2X", (21,21))

        self.image = UserCursor.image
        self.rect = pygame.Rect((0,0,1,1))
        UserCursor.me = self
        UserLauncher.me.addObject(self)

        self.firstCycle = True

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()
        else:
            self.rect.topleft = (2000,2000)
            self.firstCycle = False

    @staticmethod
    def wipe():
        UserCursor.me = None

    def checkPressed(self):
        dest = None

        for spr in UserLauncher.me.ES_group:
            if spr.__class__ == UserButton and spr.mouseOver:
                dest = spr.getDest()
                break

        for spr in UserLauncher.me.FB_group:
            bounds = UserLauncher.me.getFileBounds() # top, bottom
            yPos = pygame.mouse.get_pos()[1]

            if yPos < bounds[0] and yPos > bounds[1]:
                if spr.__class__ == UserMapButton and spr.mouseOver:
                    dest = spr.getDest()
                    UserLauncher.setLoadData(spr.getMapName())
                    break

        return dest


class UserTxt(pygame.sprite.Sprite):

    def __init__(self, text, fontSize, fontColor, center):
        pygame.sprite.Sprite.__init__(self)

        font = dinosInSpace.FontBank.getFont(fontSize)
        self.image = font.render(text, True, fontColor)
        self.rect = self.image.get_rect()
        self.rect.center = center

        UserLauncher.addObject(self)


class UserSol(spriteBasic.BasicRect):
    """
        subclass of BasicRect
        -adds isMask=False tag and automates state object addition by default
    """

    def __init__(self, size, color, topLeft, width=None, isMask=False):
        spriteBasic.BasicRect.__init__(self, size, color, topLeft, width)

        if not isMask: # if mask, add object to state manually
            UserLauncher.me.addObject(self)

class WaveThing(pygame.sprite.Sprite):
    FRAMES = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not WaveThing.FRAMES:
            for i in range(WAVE_NUMFRAMES):
                postfix = "000"
                if i > 9:
                    postfix = "00"
                fileName = "yellowWave2" + postfix + str(i) + ".png"
                WaveThing.FRAMES.append(dinosInSpace.loadImage(fileName, "4X", (0,0)))

        self.image = WaveThing.FRAMES[0]
        self.rect = self.image.get_rect()
        self.rect.center = WAVE_CENTER
        self.FRAMEDELAY = WAVE_DELAY
        self.delayTick = self.FRAMEDELAY
        self.currentFrame = 0

    def update(self):
        self.delayTick -= 1
        if self.delayTick < 0:
            self.delayTick = self.FRAMEDELAY
            self.animate()

    def animate(self):
        self.currentFrame += 1
        if self.currentFrame > len(WaveThing.FRAMES) - 1:
            self.currentFrame = 0
        self.image = WaveThing.FRAMES[self.currentFrame]




def launchUserMaps(_fps, snapshot, swipeDirection):

    UserImgLib()
    img = UserImgLib.getImage
    screen = pygame.display.get_surface()

    sbu_w = img("SPINNER_ADD").get_width() # scroll button width
    BOX_SIZE = (400, 550)
    BOX_TOP = 0
    BOX_BOTTOM = BOX_TOP + BOX_SIZE[1]
    LEFTBOX_LEFT = 0
    RIGHTBOX_LEFT = LEFTBOX_LEFT + BOX_SIZE[0]
    SET_BTTN_H = 40
    FONTSIZE = 20
    FILEBOX_SIZE = (BOX_SIZE[0] - sbu_w - 12, BOX_SIZE[1] - FONTSIZE - TOPBUFF)
    FILEBOX_LEFT = LEFTBOX_LEFT + 6
    FILEBOX_RIGHT = FILEBOX_LEFT + FILEBOX_SIZE[0]

    CANNON_X = 100
    STARCANNON_X = screen.get_width()
    STARSMALL_ROWS = 8
    STARMED_ROWS = 7
    STARBIG_ROWS = 6

    userLauncher = UserLauncher(BOX_SIZE, (LEFTBOX_LEFT, BOX_TOP), FONTSIZE)
    flyerGroup = userLauncher.getFlyerGroup()

#    # group, flyers... pos, step, var, speed, spin, edge
#
#    smallStars = []
#    medStars = []
#    bigStars = []
#
#    starVar = 0
#
#    starFrq = 6
#    starSpd = (-10, 0)
#    starSpn = 0
#    starStepY = screen.get_height()/STARSMALL_ROWS
#    star_y = starStepY - 30
#    for y in range(STARSMALL_ROWS):
#        smallStars.append(cannon.Cannon(flyerGroup, [img("STARSMALL")], (STARCANNON_X, star_y), starFrq, starVar, starSpd, starSpn, "L"))
#        star_y += starStepY
#
#    starFrq = 12
#    starSpn = 0
#    starSpd = (-9, 0)
#    starStepY = screen.get_height()/STARMED_ROWS
#    star_y = starStepY - 50
#    for y in range(STARMED_ROWS):
#        medStars.append(cannon.Cannon(flyerGroup, [img("STARMED")], (STARCANNON_X, star_y), starFrq, starVar, starSpd, starSpn, "L"))
#        star_y += starStepY
#
#    starFrq = 24
#    starSpn = 0
#    starSpd = (-8, 0)
#    starStepY = screen.get_height()/STARBIG_ROWS
#    star_y = starStepY - 30
#    for y in range(STARBIG_ROWS):
#        bigStars.append(cannon.Cannon(flyerGroup, [img("STARBIG")], (STARCANNON_X, star_y), starFrq, starVar, starSpd, starSpn, "L"))
#        star_y += starStepY
#
#    c1 = cannon.Cannon(flyerGroup, [img("FLYERGREENSMALL")], (CANNON_X, 500), 130, 70, (7, 0), 9, "R")
#    c2 = cannon.Cannon(flyerGroup, [img("FLYERGREEN")], (CANNON_X, 150), 150, 80, (5, 0), 7, "R")
#    c3 = cannon.Cannon(flyerGroup, [img("FLYERGREENMED")], (CANNON_X, 50), 200, 90, (4, 0), 3, "R")
#    c4 = cannon.Cannon(flyerGroup, [img("FLYERGREENBIG")], (CANNON_X, 300), 300, 100, (3, 0), 2, "R")
#
#    dc1Start = random.randrange(0,screen.get_height()/2)
#    dc2Start = random.randrange(screen.get_height()/2, screen.get_height() - 100)
#
#    dc1 = cannon.Cannon(flyerGroup, [img("DINOG1"), img("DINOG2")], [CANNON_X, dc1Start], 350, 100, (4, 0), 4, "R")
#    dc1.setFrameStep(15)
#    dc1.setJump("y")
#    dc1.setCountDown(50)
#
#    dc2 = cannon.Cannon(flyerGroup, [img("DINOG1b"), img("DINOG2b")], [CANNON_X, dc2Start], 500, 200, (4, 0), 4, "R")
#    dc2.setFrameStep(15)
#    dc2.setJump("y")
#    dc2.setCountDown(250)
#
#    userLauncher.addCannonList(smallStars)
#    userLauncher.addCannonList(medStars)
#    userLauncher.addCannonList(bigStars)
#    userLauncher.addCannonList([c1,c2,c3,c4,dc1, dc2])

    UserSol((BOX_SIZE[0], BOX_TOP + FONTSIZE + TOPBUFF), COL_BACKGROUND, (LEFTBOX_LEFT, 0)) # file hider top
    UserSol((BOX_SIZE[0], 100), COL_BACKGROUND, (LEFTBOX_LEFT, BOX_BOTTOM - 6)) # file hider bottom
    UserSol(BOX_SIZE, COL_RECTS, (LEFTBOX_LEFT, BOX_TOP), 2) # menu outline
    UserSol(FILEBOX_SIZE, COL_RECTS, (LEFTBOX_LEFT + 6, FONTSIZE + TOPBUFF), 2) # file outline

    UserButton((BOX_SIZE[0], SET_BTTN_H), COL_EXIT_OFF, COL_EXIT_ON, "BACK", 20, COL_EXIT_TXT, (LEFTBOX_LEFT, BOX_BOTTOM + 9), "_EXIT")
    UserSol((BOX_SIZE[0], BOX_SIZE[1]), COL_RECTS, (0, BOX_BOTTOM - 2), 2) # back button outline


    # masks
    msk = UserSol((BOX_SIZE[0], screen.get_height()), COL_BACKGROUND, (0,0), None, True)
    userLauncher.addMask(msk)

    mapScroller = UserMapScroller()
    mapScroller.makeUserButtons()

    SCROLLBTN_H = img("USERUP").get_height()

    scrollButtonUp = UserMapScrollerButton(img("USERUP"), (RIGHTBOX_LEFT - sbu_w - 4, BOX_TOP + FONTSIZE + 7), "DOWN")
    scrollButtonDown = UserMapScrollerButton(img("USERDOWN"), (RIGHTBOX_LEFT - sbu_w - 4, BOX_BOTTOM - SCROLLBTN_H - 6), "UP")
    UserLauncher.me.addObject(scrollButtonUp)
    UserLauncher.me.addObject(scrollButtonDown)

    # header text
    headerText = infoGraphic56.TextObject("Select Puzzle:", STD_FSIZE, DARKYEL, (FILEBOX_SIZE[0]/2, 16))
    UserLauncher.me.addObject(headerText)

    # preview image
    mapPreviewImage = MapPreviewImage()
    userLauncher.addObject(mapPreviewImage)

    # wave thing
    waveThing = WaveThing()
    userLauncher.addObject(waveThing)

    cursor = UserCursor()

    dest, snapshot = userLauncher.runMe(_fps, snapshot, swipeDirection) # run main loop / wait for selection

    if dest == "LOAD":
        goTo = UserLauncher.me.loadData

    elif dest == "_EXIT":
        goTo = "_EXIT"

    userMapsWipe()
    return goTo, snapshot

def userMapsWipe():
    UserLauncher.wipe()
    UserMapScroller.wipe()
    UserCursor.wipe()
    UserMapButton.wipe()
    MapPreviewImage.wipe()
