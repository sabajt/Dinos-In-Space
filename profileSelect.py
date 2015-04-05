"""
        profileSelect.py
        - player selects new profile from saved files
"""

import pygame
import dinosInSpace
import dataStorage56
import infoGraphic56
import spriteBasic
import tween
import gfx56
import screenWipe
import soundFx56

BLACK               = (0,0,0)
RED                 = (255,0,0)
DGREEN              = (0,180,0)
WHITE               = (255,255,255)
OFFSCREEN           = (-1000,-1000)
STD_FSIZE           = 20
SNAX_ARCHIVE        = "_snaxArchive"
SNAX_MILESTONE      = "_snaxMilestone"
NON_PUZZLE_PORTAL   = [SNAX_ARCHIVE, SNAX_MILESTONE, "quit to title", "interstellar snax ship", "tut2", "tut3", "tut4", "tut5", "tut6", "tut7"]
TOPBUFF = 10

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:

            ImgLib.imgDict = {
                "CURSORSTD"     :   dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "SCROLLUP"      :   dinosInSpace.loadImage("scrollUpGreen.png", "2X", None),
                "SCROLLDOWN"    :   dinosInSpace.loadImage("scrollDownGreen.png", "2X", None),
                "SCROLLUP1"     :   dinosInSpace.loadImage("scrollUpGreen1.png", "2X"),
                "SCROLLDOWN1"   :   dinosInSpace.loadImage("scrollDownGreen1.png", "2X"),
                "LOADPREV"     :   dinosInSpace.loadImage("rocketMask.png", "2X", (200,300)),
                "LOADPIC"       :   dinosInSpace.loadImage("rocketFillNew.png", "2X")
            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image, " + name + " not found"


class LoadProfileScreen(object):
    """ running state """
    me = None

    def __init__(self):
        LoadProfileScreen.me = self

        self.keepGoing      = True
        self.shiftDown      = False
        self.displayPrev    = False

        #self.bkgGroup       = pygame.sprite.OrderedUpdates()    # bottom level gfx
        self.previewGroup   = pygame.sprite.OrderedUpdates()    # right hand side profile progress preview
        self.fileBoxGroup   = pygame.sprite.RenderUpdates()             # box behind file buttons
        self.buttonGroup    = pygame.sprite.OrderedUpdates()    # buttons that return a dest
        self.maskGroup      = pygame.sprite.OrderedUpdates()    # surface that masks buttons
        self.exitGroup      = pygame.sprite.RenderUpdates()       # exit button
        self.scrollGroup    = pygame.sprite.RenderUpdates()             # scroller buttons
        self.cursorGroup    = pygame.sprite.RenderUpdates()       # mouse cursor

        self.ynGroup        = pygame.sprite.RenderUpdates()       # y/n tween message only

        self.screen         = pygame.display.get_surface()
        self.background     = pygame.Surface(self.screen.get_size())

        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))

    @staticmethod
    def wipe():
        LoadProfileScreen.me = None

    def runMe(self, _fps, imageFrom):
        clock = pygame.time.Clock()
        self.keepGoing = True
        dest = None
        firstCycle = True

        while self.keepGoing:

            clock.tick(_fps)
            dest = self.getInput(_fps)

            # ******* % preview ********
            if pygame.sprite.spritecollideany(MouseCursor.me, self.buttonGroup):
                self.displayPrev = True
            else:
                self.displayPrev = False
            if firstCycle:
                self.displayPrev = False
                firstCycle = False
            # **************************

            #            self.bkgGroup.clear(screen, background)
            self.previewGroup.clear(self.screen, self.background)

            self.buttonGroup.clear(self.screen, self.background)
            self.maskGroup.clear(self.screen, self.background)
            self.exitGroup.clear(self.screen, self.background)
            self.scrollGroup.clear(self.screen, self.background)
            self.fileBoxGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)

            #            self.bkgGroup.update()
            self.previewGroup.update()

            self.buttonGroup.update()
            self.maskGroup.update()
            self.exitGroup.update()
            self.scrollGroup.update()
            self.fileBoxGroup.update()
            self.cursorGroup.update()

            #            self.bkgGroup.draw(screen)
            self.previewGroup.draw(self.screen)

            self.buttonGroup.draw(self.screen)
            self.maskGroup.draw(self.screen)
            self.exitGroup.draw(self.screen)
            self.scrollGroup.draw(self.screen)
            self.fileBoxGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "left")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            if dest:
                soundFx56.SoundPlayer.requestSound("woosh_b")
                self.keepGoing = False

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, self.background)

        self.previewGroup.draw(self.screen)
        self.buttonGroup.draw(self.screen)
        self.maskGroup.draw(self.screen)
        self.exitGroup.draw(self.screen)
        self.fileBoxGroup.draw(self.screen)
        self.scrollGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

# snapshot = pygame.display.get_surface().copy()
        return dest, snapshot

    def runYN(self, _fps):
        """ create tween YN message / wait for user input """
#        for s in self.ynGroup:
#            s.setTween
#            break

        clock = pygame.time.Clock()
        yesOrNo = None
        while not yesOrNo:
            clock.tick(_fps)

            # get input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        yesOrNo = "y"
                    elif event.key == pygame.K_n:
                        yesOrNo = "n"

            # clear / update / draw cycle
            self.previewGroup.clear(self.screen, self.background)
            self.buttonGroup.clear(self.screen, self.background)
            self.maskGroup.clear(self.screen, self.background)
            self.exitGroup.clear(self.screen, self.background)
            self.scrollGroup.clear(self.screen, self.background)
            self.fileBoxGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)
            self.ynGroup.clear(self.screen, self.background)

            self.ynGroup.update()

            self.previewGroup.draw(self.screen)
            self.buttonGroup.draw(self.screen)
            self.maskGroup.draw(self.screen)
            self.exitGroup.draw(self.screen)
            self.scrollGroup.draw(self.screen)
            self.fileBoxGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)
            self.ynGroup.draw(self.screen)

            gfx56.drawBorder(self)
            pygame.display.flip()

        for spr in self.ynGroup:
            spr.kill()
        return yesOrNo

    def getInput(self, _fps):
        dest = None

        for event in pygame.event.get():

            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL:
                self.shiftDown = True
            else:
                self.shiftDown = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                dest = self.checkButtonPressed(_fps)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dest = "_EXIT"

        return dest

    def checkButtonPressed(self, _fps):
        dest = None
        for b in self.exitGroup:
            dest = b.requestDest(_fps)
        if not dest:
            for b in self.buttonGroup:
                if b.__class__ == ProfileButton:
                    dest = b.requestDest(_fps)
                    if dest:
                        break

        return dest

    def addSpriteToGroup(self, sprite, group):
        if group == "BKG":
            self.bkgGroup.add(sprite)
        elif group == "PREVIEW":
            self.previewGroup.add(sprite)
        elif group == "FILEBOX":
            self.fileBoxGroup.add(sprite)
        elif group == "BUTTON":
            self.buttonGroup.add(sprite)
        elif group == "MASK":
            self.maskGroup.add(sprite)
        elif group == "EXIT":
            self.exitGroup.add(sprite)
        elif group == "SCROLL":
            self.scrollGroup.add(sprite)
        elif group == "CURSOR":
            self.cursorGroup.add(sprite)
        elif group == "YN":
            self.ynGroup.add(sprite)

    def addSpriteListToGroup(self, spriteList, group):
        for s in spriteList:
            self.addSpriteToGroup(s, group)


class ProfileScroller(object):
    """ generates and keeps track of saved profile buttons """
    me = None

    def __init__(self, fileBox):
        ProfileScroller.me = self
        self.buttonList = []

        self.BUTTON_W   = fileBox.rect.width
        self.BUTTON_H   = 40
        self.BUTTON_X   = fileBox.rect.left
        self.TOP        = fileBox.rect.top
        self.BOTTOM     = fileBox.rect.bottom

        self.head       = None # scroller bounds
        self.tail       = None

    @staticmethod
    def wipe():
        ProfileScroller.me = None

    def scroll(self, direction):

        if self.buttonList:
            if direction == "DOWN":
                if self.head.rect.top < self.TOP:
                    for b in self.buttonList:
                        b.move(direction)
            else:
                if self.tail.rect.bottom > self.BOTTOM:
                    for b in self.buttonList:
                        b.move(direction)

    def makeButtons(self, frameColorOff, frameColorOn, fontSize, fontColor):

        size        = (self.BUTTON_W, self.BUTTON_H)
        colorDel    = (255,0,0)
        x           = self.BUTTON_X
        y           = self.TOP

        profDataList, profNames = dataStorage56.getSortedProfiles(True)
        assert len(profDataList) == len(profNames)

        nCount = 0
        if profDataList:
            for pData in profDataList:
                topLeft = (x,y)
                b = ProfileButton(size,
                                  frameColorOff,
                                  frameColorOn,
                                  colorDel,
                                  fontSize,
                                  fontColor,
                                  topLeft,
                                  profNames[nCount][:-4],
                                  pData)
                self.buttonList.append(b)
                y += self.BUTTON_H
                nCount += 1

        if self.buttonList:
            self.head = self.buttonList[0]
            self.tail = self.buttonList[-1]

        return self.buttonList

    def getIndex(self, button):
        assert self.buttonList
        return self.buttonList.index(button)

    def closeGap(self, index):
        assert self.buttonList
        for b in self.buttonList[index:]:
            b.swish()

class ProfileScrollerButton(pygame.sprite.Sprite):
    """ button that controlls the user map buttons (links to user maps) """

    def __init__(self, imgOff, imgOn, topLeft, direction):
        pygame.sprite.Sprite.__init__(self)
        assert (direction == "UP" or direction == "DOWN")

        self.direction      = direction
        self.imgOff         = imgOff
        self.imgOn          = imgOn
        self.image          = self.imgOff
        self.rect           = self.image.get_rect()
        self.rect.topleft   = topLeft
        self.mouseOver      = False

    def update(self):

        if pygame.sprite.collide_rect(self, MouseCursor.me):
            self.mouseOver = True
            self.image = self.imgOn
        else:
            self.mouseOver = False
            self.image = self.imgOff

        if self.mouseOver:
            ProfileScroller.me.scroll(self.direction)

class ProfileButton(pygame.sprite.Sprite):
    """ each is a link to a saved profile """

    def __init__(self, size, color0, color1, colorDel, fontSize, fontColor, topLeft, text, pData=None):
        pygame.sprite.Sprite.__init__(self)

        self.STEP           = 8
        self.imageOff       = self.makeButton(size, color0, text, fontSize, fontColor)
        self.imageOver      = self.makeButton(size, color1, text, fontSize, fontColor)
        self.image          = self.imageOff
        self.rect           = self.image.get_rect()
        self.rect.topleft   = topLeft
        self.dest           = text
        self.firstCycle     = True
        self.mouseOver      = False

        if self.__class__ == ProfileButton:
            self.imageDel       = self.makeButton(size, colorDel, text, fontSize, fontColor)
            self.SWISHSTEP      = 4
            self.swishTick      = 0
            self.swishing       = False
            self.totalUnits     = 0
            self.completedUnits = 0

            self.calculatePreview(pData)
            assert self.rect.height % self.SWISHSTEP == 0

    def update(self):
        if self.firstCycle:
            self.firstCycle = False
        else:
            self.checkCursorOver()
            if self.__class__ == ProfileButton and self.swishing:
                if self.swishTick == self.rect.height:
                    self.swishing = False
                    self.swishTick = 0
                else:
                    self.rect.top -= self.SWISHSTEP
                    self.swishTick += self.SWISHSTEP


    def calculatePreview(self, pData):
        """ calculate % of game complete for display -- profile buttons only """
        for puz in pData:
            if puz not in NON_PUZZLE_PORTAL:

                self.totalUnits += 1
                if pData[puz][2]:
                    self.completedUnits += 1
                if pData[puz][4]:
                    for snax in pData[puz][4]:
                        self.totalUnits += 1
                        if snax:
                            self.completedUnits += 1

    def makeButton(self, size, frameColor, text, fontSize, fontColor):
        textSurf = infoGraphic56.TextObject(text, fontSize, fontColor).image
        frame = spriteBasic.BasicRect(size, frameColor)
        xBlit = (frame.rect.width - textSurf.get_width())/2
        yBlit = (frame.rect.height - textSurf.get_height())/2
        frame.image.blit(textSurf, (xBlit, yBlit))

        return frame.image

    def checkCursorOver(self):
        """ if cursor over button set respective image and mouseOver """

        if self.isInBounds() and pygame.sprite.collide_rect(self, MouseCursor.me):
            self.image = self.imageOver
            self.mouseOver = True
            if self.__class__ == ProfileButton:
                # send display preview info ***************************************************************
                PrevPercent.me.refresh((self.completedUnits, self.totalUnits))
                PrevBar.me.refresh((self.completedUnits, self.totalUnits))
                if LoadProfileScreen.me.shiftDown:
                    self.image = self.imageDel
        else:
            self.image = self.imageOff
            self.mouseOver = False

    def isInBounds(self):
        inBounds = True

        if self.__class__ == ProfileButton:
            if self.rect.top <  ProfileScroller.me.TOP or self.rect.bottom > ProfileScroller.me.BOTTOM:
                inBounds = False

        return inBounds

    def requestDest(self, _fps):
        """ returns dest if mouseOver, or deletes if shift is down """
        dest = None
        if self.mouseOver:
            if LoadProfileScreen.me.shiftDown and self.__class__ == ProfileButton:
                if not self.swishing:
                    makeYN()
                    if LoadProfileScreen.me.runYN(_fps) == "y":
                        dataStorage56.deleteProfile(self.dest)
                        self.erase()
            else:
                dest = self.dest

        return dest

    def move(self, direction):
        if direction == "UP":
            self.rect.centery -= self.STEP

        elif direction == "DOWN":
            self.rect.centery += self.STEP

    def erase(self):
        assert self.__class__ == ProfileButton

        i = ProfileScroller.me.getIndex(self)
        self.kill()
        ProfileScroller.me.closeGap(i)

    def swish(self):
        self.swishing = True


class PrevPercent(infoGraphic56.TextObject):
    """ displays percentage of game complete for a profile """
    me = None

    def __init__(self):
        screen      = pygame.display.get_surface()
        self.size   = 30
        self.color  = (255,255,255)
        self.center = (3*screen.get_width()/4, screen.get_height()/2)
        self.firstCycle     = True

        text = "text"

        infoGraphic56.TextObject.__init__(self, text, self.size, self.color, OFFSCREEN)
        PrevPercent.me = self

    def update(self):
        if self.firstCycle:
            self.rect.center = OFFSCREEN
            self.firstCycle = False
        elif not LoadProfileScreen.me.displayPrev:
            self.rect.center = OFFSCREEN

    def refresh(self, fraction):
        rep = float(fraction[0])/fraction[1]
        rep *= 100
        text = str(int(rep)) + " %"
        self.rerender(text, None, self.center)

    @staticmethod
    def wipe():
        PrevPercent.me = None

class PrevBar(pygame.sprite.Sprite):
    me = None

    def __init__(self, image, bottomleft):
        pygame.sprite.Sprite.__init__(self)

        screen = pygame.display.get_surface()
        self.picture = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.BOTTOMLEFT = bottomleft
        self.firstCycle = True
        PrevBar.me = self

    def update(self):
        if self.firstCycle:
            self.rect.center = (2000,2000)
            self.firstCycle = False
        elif not LoadProfileScreen.me.displayPrev:
            self.rect.center = OFFSCREEN

    def refresh(self, fraction):
        frac = float(fraction[0])/fraction[1]
        height = self.picture.get_height() - self.picture.get_height() * frac
        img = self.picture.copy()
        if height > 0:
            msk = pygame.Surface((self.picture.get_width(), height))
            msk.fill((0,0,0))
            img.blit(msk, (0,0))
        self.image = img
        self.rect.bottomleft = self.BOTTOMLEFT

    @staticmethod
    def wipe():
        PrevBar.me = None

#class PrevBar(spriteBasic.BasicRect):
#    me = None
#
#    def __init__(self, width, maxheight, bottomleft):
#        screen          = pygame.display.get_surface()
#        self.WIDTH      = width
#        self.MAXHEIGHT  = maxheight
#        self.BOTTOMLEFT = bottomleft
#        self.size       = (self.WIDTH, 100)
#        self.color      = (255,0,100)
#        self.firstCycle     = True
#
#        spriteBasic.BasicRect.__init__(self, self.size, self.color)
#        self.rect.bottomleft = self.BOTTOMLEFT
#        PrevBar.me = self
#
#    def update(self):
#        if self.firstCycle:
#            self.rect.center = (2000,2000)
#            self.firstCycle = False
#        elif not LoadProfileScreen.me.displayPrev:
#            self.rect.center = OFFSCREEN
#
#    def refresh(self, fraction):
#        frac    = float(fraction[0])/fraction[1]
#        height  = int(self.MAXHEIGHT * frac)
#
#        self.resize((self.WIDTH, height))
#        self.rect.bottomleft = self.BOTTOMLEFT
#
#    @staticmethod
#    def wipe():
#        PrevBar.me = None

class PrevMask(pygame.sprite.Sprite):
    me = None

    def __init__(self, imageOff, imageOn, center):
        pygame.sprite.Sprite.__init__(self)

        self.imageOff       = imageOff
        self.imageOn        = imageOn
        self.image          = imageOff
        self.rect           = self.image.get_rect()
        self.rect.center    = center
        self.firstCycle     = True

    def update(self):
        if LoadProfileScreen.me.displayPrev:
            self.image = self.imageOn
            if self.firstCycle:
                self.image = self.imageOff
                self.firstCycle = False
        else:
            self.image = self.imageOff


    @staticmethod
    def wipe():
        PrevMask.me = None

class ExitButton(ProfileButton):

    def __init__(self, size, color0, color1, fontSize, fontColor, topLeft, text):
        ProfileButton.__init__(self, size, color0, color1, None, fontSize, fontColor, topLeft, text)

        self.dest = "_EXIT"

class MouseCursor(pygame.sprite.Sprite):
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        MouseCursor.me = self

        self.firstCycle = True
        self.image  = ImgLib.getImage("CURSORSTD")
        self.rect   = pygame.rect.Rect((0,0,1,1))

    def update(self):
        if self.firstCycle:
            self.firstCycle = False
            self.rect.center = OFFSCREEN
        else:
            self.rect.center = pygame.mouse.get_pos()

    @staticmethod
    def wipe():
        MouseCursor.me = None

def launchProfileSelect(_fps, snapshot):

    ImgLib()
    img                 = ImgLib.getImage
    screen              = pygame.display.get_surface()
    loadProfileScreen   = LoadProfileScreen()

    # helper values

    labFontSize = 20 # top text
    labBuffer = TOPBUFF # top text buffer
    yBoxOffset = labFontSize + labBuffer
    exitBttnHeight  = 40
    delInfoHeight   = 150
    scrollBttnWidth = img("SCROLLUP").get_width()
    rimSize = 2

    # fileBox and other asthetic stuff

    spaceBuffer     = 5
    fbSize          = (screen.get_width()/2 - scrollBttnWidth - 2*spaceBuffer, screen.get_height() - exitBttnHeight - delInfoHeight - yBoxOffset)
    fbCol           = (255,255,255)
    fbTL            = (0,yBoxOffset)
    fileBox         = spriteBasic.BasicRect(fbSize, fbCol, fbTL, rimSize)
    #overBox         = spriteBasic.BasicRect((fbSize[0], screen.get_height()), fbCol, fbTL, rimSize)
    lhsBox          = spriteBasic.BasicRect((screen.get_width()/2, screen.get_height()), fbCol, (0,0), rimSize)
    #  backBox
    topMask = spriteBasic.BasicRect((fbSize[0], yBoxOffset), (0,0,0),(0,0))

    profileText = infoGraphic56.TextObject("Select Profile:", STD_FSIZE, DGREEN, (fbSize[0]/2, 16))

    loadProfileScreen.addSpriteListToGroup((fileBox, lhsBox, profileText), "FILEBOX")
    loadProfileScreen.addSpriteToGroup(topMask, "MASK")

    # profile scroller (automatically makes profile buttons)

    frameColorOff   = (0,0,0)
    frameColorOn    = DGREEN
    bttnFontSize    = 16
    bttnFontColor   = (255,255,255)

    profileScroller = ProfileScroller(fileBox)
    profileButtons = profileScroller.makeButtons(frameColorOff, frameColorOn, bttnFontSize, bttnFontColor)

    loadProfileScreen.addSpriteListToGroup(profileButtons, "BUTTON")

    # profile scroller button

    scrollBttn1TL   = (fbSize[0] + spaceBuffer, yBoxOffset)

    scrollBttnUp    = ProfileScrollerButton(img("SCROLLUP"), img("SCROLLUP1"), scrollBttn1TL, "DOWN")

    scrollBttn2TL = (scrollBttnUp.rect.left, scrollBttnUp.rect.bottom + 8)
    scrollBttnDown  = ProfileScrollerButton(img("SCROLLDOWN"), img("SCROLLDOWN1"), scrollBttn2TL, "UP")

    loadProfileScreen.addSpriteToGroup(scrollBttnUp, "SCROLL")
    loadProfileScreen.addSpriteToGroup(scrollBttnDown, "SCROLL")

    # delInfo mask

    delMaskSize     = (fbSize[0], delInfoHeight)
    delMaskColor    = (0,0,0)
    delMaskTL       = (0, fbSize[1] + yBoxOffset)
    delMask         = spriteBasic.BasicRect(delMaskSize, delMaskColor, delMaskTL)

    loadProfileScreen.addSpriteToGroup(delMask, "MASK")

    delBox = spriteBasic.BasicRect((screen.get_width()/2, delMaskSize[1]), fbCol, (0, delMaskTL[1] - 2), rimSize)
    loadProfileScreen.addSpriteToGroup(delBox, "FILEBOX")


    # del text

    delInfoSize     = STD_FSIZE
    delInfoColor    = (255,0,0)
    m1text          = "Delete Profile: Hold"
    m2text          = "'CTRL' while selecting"
    m1Center        = (delMaskSize[0]/2, delMaskTL[1] + delMaskSize[1]/3)
    m2Center        = (delMaskSize[0]/2, delMaskTL[1] + 2*delMaskSize[1]/3)

    delInfo1        = infoGraphic56.TextObject(m1text, delInfoSize, delInfoColor, m1Center)
    delInfo2        = infoGraphic56.TextObject(m2text, delInfoSize, delInfoColor, m2Center)

    loadProfileScreen.addSpriteListToGroup([delInfo1, delInfo2], "MASK")

    # exit button

    exitSize        = (screen.get_width()/2, exitBttnHeight) # height defined above
    exitColOff      = (150,150,150)
    exitColOn       = DGREEN
    exitFontSize    = 20
    exitFontColor   = (0,0,0)
    exitTopLeft     = (0, screen.get_height() - exitSize[1])
    exitButton      = ExitButton(exitSize, exitColOff, exitColOn, exitFontSize, exitFontColor, exitTopLeft, "BACK")

    loadProfileScreen.addSpriteToGroup(exitButton, "EXIT")

    # prev bar and mask

    prevMask        = PrevMask(img("LOADPREV"), img("LOADPREV"), (3*screen.get_width()/4, screen.get_height()/2))
    prevBar         = PrevBar(img("LOADPIC"), prevMask.rect.bottomleft)
#    prevBar         = PrevBar(prevMask.rect.width, prevMask.rect.height, prevMask.rect.bottomleft)
    loadProfileScreen.addSpriteToGroup(prevBar, "PREVIEW")
    loadProfileScreen.addSpriteToGroup(prevMask, "PREVIEW")

    # prev percent

    prevPercent     = PrevPercent()
    loadProfileScreen.addSpriteToGroup(prevPercent, "PREVIEW")

    # cursor

    cursor = MouseCursor()
    loadProfileScreen.addSpriteToGroup(cursor, "CURSOR")

    # run

    dest, snapShot = loadProfileScreen.runMe(_fps, snapshot)
    wipe()
    return dest, snapShot

def makeYN():

    ynSize      = (400,200)
    ynColor     = (255,0,0)
    ynFontSize  = 30
    ynFontColor = (255,255,255)
    alpha       = 180
    ynMenu      = tween.TweenYN(ynSize, ynColor, ynFontSize, ynFontColor, alpha)

    LoadProfileScreen.me.addSpriteToGroup(ynMenu, "YN")

def wipe():
    LoadProfileScreen.wipe()
    ProfileScroller.wipe()
    MouseCursor.wipe()
    PrevPercent.wipe()
    PrevBar.wipe()


