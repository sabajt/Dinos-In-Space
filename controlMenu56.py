""" controlMenu56.py """

import pygame
import dinosInSpace
import infoGraphic56
import soundFx56
import spriteBasic

WHITE = (255, 255, 255)
GREY = (150, 150, 150)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

TEXT_COLOR = BLACK
HELP_KEYS_COLOR = WHITE
HELP_CONTROLS_COLOR = BLUE

CONTROLS_OFFSET = 110 #85 # 40
KEYS_OFFSET = -155 #-195 # -225
HELP_TEXT_OFFSETY = -35

MENU_SIZE = (600, 300)
ALPHA = 250
BTTN_XBUF = 40
BTTN_HEIGHT = 50
BOTTOM_BUTTON_YOFFSET = 55
BTTN_FONTSIZE = 20
MENU_FONTSIZE = 12

BASIC_BUTTON_OFFSET = (0,0) # intended to make room for puzzle title on pause menu


## temp fix, remove after resaving levels with current data struct
class SwitchesMsg(object):
    pass
class NewColorsMsg(object):
    pass

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):

        if not ImgLib.imgDict:

            # basic rect: size, color, topLeft=(0,0), rimSize=None, alpha=None, opaqueCenter=False
            _menu = spriteBasic.BasicRect(MENU_SIZE, WHITE, (0,0), 2, ALPHA, True).image.copy()
            _buttonSize = (_menu.get_width() - BTTN_XBUF, BTTN_HEIGHT)

            ImgLib.imgDict = {
                "CURSOR" : dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "MENU" : _menu,
                "BTTN_0" : pygame.Surface(_buttonSize),
                "BTTN_1" : pygame.Surface(_buttonSize)
            }

            ImgLib.imgDict["BTTN_0"].fill(GREY)
            ImgLib.imgDict["BTTN_1"].fill(WHITE)

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print("image, " + name + " not found")

def initImgLib():
    ImgLib()


class BasicMenu(pygame.sprite.Sprite):
    """ superclass for a control menu, must use a child class """
    allMenuGroups = pygame.sprite.OrderedUpdates()

    def __init__(self, stateObj): # stateObj is the main obj controlling the current state, ie: game, title etc
        pygame.sprite.Sprite.__init__(self)

        self.stateObj = stateObj
        self.onScreen = False
        self.OFFSCREEN = (-1000,-1000)
        self.CENTER = (stateObj.screen.get_width()/2, stateObj.screen.get_height()/2)

        BasicMenu.allMenuGroups.add(self)

    @staticmethod
    def wipe():
        BasicMenu.allMenuGroups = pygame.sprite.OrderedUpdates()

    def getScreenSize(self):
        return pygame.display.get_surface().get_size()

    def setPosition(self, position):
        self.POSITION = position

    def hideMe(self):
        self.rect.center = self.OFFSCREEN

    def showMe(self):
        self.rect.center = self.POSITION

    def setImage(self, clas, fileName, scaleTo, getAt):
        if not clas.myImage:
            if fileName:
                clas.myImage = dinosInSpace.loadImage(fileName, scaleTo, getAt)
            else:
                clas.myImage = pygame.Surface(scaleTo)
                clas.myImage.set_alpha(0, pygame.RLEACCEL)

        self.image = clas.myImage



class InPlayMenu(BasicMenu):
    """ menu that pauses game / displays in game options"""

    myImage = None
    inPlayGroup = pygame.sprite.OrderedUpdates()
    me = None

    def __init__(self, stateObj):

        BasicMenu.__init__(self, stateObj)

        ## self.setImage(InPlayMenu, "playMenuBlu.png", "2X", (0,0))
        ## self.image.set_alpha(210, pygame.RLEACCEL)

        imgLib = ImgLib()

        self.image = imgLib.getImage("MENU")

        self.rect = self.image.get_rect()
        self.setPosition(self.CENTER)
        InPlayMenu.me = self
        self.showMe() # must be in position to format loc for dependants
        self.currentPage = 1

    def initDependants(self): # broke away from __init__ just so that title label (separate module) could be added to this group first...
        dependants = self.makeDependants()
        InPlayMenu.inPlayGroup.add(self, dependants)
        self.hideMe()

    def update(self):
        if self.onScreen:
            self.showMe()
        else:
            self.hideMe()

    @staticmethod
    def wipe():
        InPlayMenu.inPlayGroup = pygame.sprite.OrderedUpdates()
        InPlayMenu.me = None

    @staticmethod
    def requestToggle(turnOn):
        if not turnOn:
##            print "/ntoggle off/n"
            soundFx56.SoundPlayer.requestSound("pause")
            for s in InPlayMenu.inPlayGroup:
                s.onScreen = False
        else:
##            print "/ntoggle on/n"
            soundFx56.SoundPlayer.requestSound("pause")
            InPlayMenu.me.setPage(1)

            for s in InPlayMenu.inPlayGroup:
                if hasattr(s, "checkCurrentPage"):
                    if s.checkCurrentPage(InPlayMenu):
##                      if s.__class__ == PauseMenuGraphic:
##                      print "hi i'm the problem"
                        s.onScreen = True

    def checkCurrentPage(self, masterMenuClass):
        return True # the master menu is always visible

    def setPage(self, page):
        if self.stateObj.getPause():
            if page == "RESUME":
                InPlayMenu.requestToggle(False)
                self.stateObj.setPause(False)
            elif page == "EXIT":
                self.stateObj.setPause(False)
                self.stateObj.keepGoing = False
                self.stateObj.leaveRequest = True ############## ########################################### leave request added
            elif page == "RETRY":
                self.stateObj.setRetry(True)
                self.stateObj.setPause(False)
                self.stateObj.keepGoing = False
            else:
                self.currentPage = page

                for s in InPlayMenu.inPlayGroup:
                    if hasattr(s, "checkCurrentPage"):
                        if s.checkCurrentPage(InPlayMenu):
                            s.onScreen = True
                        else:
                            s.onScreen = False

    def makeButtons(self, pageData, pageButtons, allButtons):
        onPage = pageData[0]
        totalSetNum = len(pageData[1])

        for myNum in range(totalSetNum):
            text = pageData[1][myNum][1]
            toPage = pageData[1][myNum][0]
            b = BasicButton(self.stateObj, self, totalSetNum, myNum, onPage, text, True) # last tag for offset
            b.setTO_PAGE(toPage)
            pageButtons.append(b)

        allButtons.append(pageButtons)

        return allButtons

    def makeBottomButtons(self, pageData, pageButtons, allButtons):
        """ same as makeButtons but with bottom formatted buttons """

        onPage = pageData[0]
        totalSetNum = len(pageData[1])

        for myNum in range(totalSetNum):

            text = pageData[1][myNum][1]
            toPage = pageData[1][myNum][0]
            b = BottomButton(self.stateObj, self, totalSetNum, myNum, onPage, text) # this is the new line
            b.setTO_PAGE(toPage)
            pageButtons.append(b)

        allButtons.append(pageButtons)

        return allButtons

    def makeImages(self, imageData):
        """ make images for pause menu pages """

        allImages = []
        sObj = self.stateObj

        for dataSet in imageData:

            onPage = dataSet[0]
            fileName = dataSet[1]
            scaleTo = dataSet[2]
            getAt = dataSet[3]
            pos = dataSet[4]
            img = PauseMenuGraphic(sObj, self, fileName, scaleTo, getAt, onPage, pos)
            allImages.append(img)

        return allImages

    def makeTextBlock(self, tBlockData):

        # self, stateObj, master, textBlock, ON_PAGE, position

        allText = []
        sObj = self.stateObj

        for dataSet in tBlockData:

            onPage = dataSet[0]
            surf = dataSet[1]
            pos = dataSet[2]
            tBlock = PauseMenuTextBlock(sObj, self, surf, onPage, pos)
            allText.append(tBlock)

        return allText

    def makeDependants(self):

        dependants = pygame.sprite.OrderedUpdates()
        pageButtons = []
        allButtons = []

        # make pages

        page1Data = [1, [ ("RETRY", "Clear / Reset"), (2, "Controls"), ("RESUME", "Resume Puzzle"), ("EXIT", "Choose Another Puzzle")]] # main
#        page2Data = [2, [ (3, "Controls"), (1, "Back") ]] # help
        page2Data = [2, [ (1, "Back") ]] # controls

        allButtons = self.makeButtons(page1Data, pageButtons, allButtons)
        allButtons = self.makeBottomButtons(page2Data, pageButtons, allButtons)
#        allButtons = self.makeBottomButtons(page3Data, pageButtons, allButtons)

        # make text boxes

        textKeys = [
            "click",
            "right or control click",
            "mouse wheel or z",
            "spacebar or click launchpad",
            "control + r",
            "m",
            "t",
            "return or escape"
        ]

        textControls = [
            "- place / rotate / link tile",
            "- pick up tiles",
            "- cycle through inventory",
            "- launch or reset dinos",
            "- clear tiles and reset puzzle",
            "- show message if avaliable",
            "- toggle inventory / radar display",
            "- pause game"
        ]

        FONTSIZE = MENU_FONTSIZE
        addHeight = 80
        addSpace = 10

        tBlockKeys = infoGraphic56.TextBlock(textKeys, FONTSIZE, HELP_KEYS_COLOR, addHeight, addSpace, False, True)
        tBlockControls = infoGraphic56.TextBlock(textControls, FONTSIZE, HELP_CONTROLS_COLOR, addHeight, addSpace)

        cnt_x = self.rect.centerx
        cnt_y = self.rect.centery + HELP_TEXT_OFFSETY

        textData = [
            (2, tBlockKeys, (cnt_x + KEYS_OFFSET, cnt_y)),
            (2, tBlockControls, (cnt_x + CONTROLS_OFFSET, cnt_y))
        ]

        allText = self.makeTextBlock(textData)

        # make images

##        imageData = [ # [(onPage, fileName, scaleTo, getAt, position), etc]
##            (1, "testCowLit.png", None, None, self.rect.center)
##        ]

##        allImages = self.makeImages(imageData)

        c = ControlMenuCursor(self.stateObj, self, ControlMenuCursor) # game, master, class

        # moved images

        dependants.add(allText)
        dependants.add(allButtons)
##        dependants.add(allImages)
        dependants.add(c)

        return dependants

class MenuDependant(BasicMenu):
    """ an object made avaliable only when its master menu is avaliable """

    def __init__(self, stateObj, master):
        BasicMenu.__init__(self, stateObj)
        self.master = master

    def checkCurrentPage(self, masterMenuClass):
##        if self.__class__ == PauseMenuGraphic: # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
##            print "PauseMenuGraphic checkCurrentPage -- self.ON_PAGE " + str(self.ON_PAGE) # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        if masterMenuClass.me.currentPage == self.ON_PAGE:
##            if self.__class__ == PauseMenuGraphic: # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
##                print "masterMenu" # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            return True
        else:
            return False

class BasicButton(MenuDependant):

    blankFrames = [] # [surface 0, surface 1]
    BasicButtonGroup = pygame.sprite.RenderUpdates() # to check if pressed only
    font = None

    def __init__(self, stateObj, master, totalSetNum, myNum, ON_PAGE, text, offset=False):
        MenuDependant.__init__(self, stateObj, master)

        self.text = text
        self.setBlankFrames("button", 2, (160, 30), (0,0)) # pass in text as well
        self.font = self.getFont(BTTN_FONTSIZE)
        self.color = TEXT_COLOR
        self.myFrames = self.getMyFrames(text, self.color)
        self.image = self.myFrames[0]
        self.rect = self.image.get_rect()
        self.setPosition(totalSetNum, myNum)
        if offset:
            self.POSITION = (self.POSITION[0] + BASIC_BUTTON_OFFSET[0], self.POSITION[1] + BASIC_BUTTON_OFFSET[1])

        self.ready = False
        self.TO_PAGE = None # must call setToPage()
        self.ON_PAGE = ON_PAGE
        self.hideMe()
        BasicButton.BasicButtonGroup.add(self)

    def updateTitle(self):

        self.checkCursorCollide()
        self.showMe()

    def update(self):
        self.checkCursorCollide()

        if not self.checkCurrentPage(InPlayMenu):
            self.hideMe()
        else:
            if self.onScreen:
                self.showMe()
            else:
                self.hideMe()

    @staticmethod
    def wipe():
        BasicButton.BasicButtonGroup = pygame.sprite.RenderUpdates()

    @staticmethod
    def requestPress():
        for b in BasicButton.BasicButtonGroup:
            if b.ready:
                if b.TO_PAGE == "RETRY" or b.TO_PAGE == "EXIT":
                    soundFx56.SoundPlayer.requestSound("woosh_b")
                b.master.setPage(b.TO_PAGE)

    def getFont(self, size):
        if not BasicButton.font:
            BasicButton.font = dinosInSpace.FontBank.getFont(size)

        return BasicButton.font

    def setTO_PAGE(self, TO_PAGE):
        self.TO_PAGE = TO_PAGE

    def checkCursorCollide(self):
        if pygame.sprite.collide_rect(self, ControlMenuCursor.me):
            self.image = self.myFrames[1]
            self.ready = True
        else:
            self.image = self.myFrames[0]
            self.ready = False

#    def setBlankFrames(self, rootName, numBlankFrames, scaleTo, getAt): # add text as param...
#
#        if not BasicButton.blankFrames:
#
#            for i in range(numBlankFrames):
#
#                fileName = rootName + str(i) + ".png"
#                image = dinosInSpace.loadImage(fileName, scaleTo, getAt)
#                BasicButton.blankFrames.append(image)

    def setBlankFrames(self, rootName, numBlankFrames, scaleTo, getAt): # add text as param...

        if not BasicButton.blankFrames:
            imgLib = ImgLib()
            image0 = imgLib.getImage("BTTN_0")
            image1 = imgLib.getImage("BTTN_1")
            BasicButton.blankFrames.append(image0)
            BasicButton.blankFrames.append(image1)

    def getMyFrames(self, text, color):

        textSurface = self.font.render(text, True, color)
        myFrame0 = BasicButton.blankFrames[0].copy()
        myFrame1 = BasicButton.blankFrames[1].copy()

        wHalfText= textSurface.get_width()/2
        hHalfText = textSurface.get_height()/2
        xCenterFrame = myFrame0.get_width()/2
        yCenterFrame = myFrame0.get_height()/2

        xBlit = xCenterFrame - wHalfText
        yBlit = yCenterFrame - hHalfText
        blitCoord0 = (xBlit, yBlit)
        blitCoord1 = (xBlit - 4, yBlit + 2)

        myFrame0.blit(textSurface, blitCoord0)
        myFrame1.blit(textSurface, blitCoord1)
        myFrames = [myFrame0, myFrame1]

        return myFrames

    def setPosition(self, totalSetNum, myNum):

        step = self.master.rect.height / (totalSetNum + 1)
        x = self.master.rect.centerx
        y = self.master.rect.top + ((myNum + 1) * step)
        self.POSITION = (x, y)

class BottomButton(BasicButton):

    def setPosition(self, totalSetNum, myNum):

        step = self.master.rect.width / (totalSetNum + 1)
        x = self.master.rect.left + ((myNum + 1) * step)
        y = self.master.rect.bottom - BOTTOM_BUTTON_YOFFSET
        self.POSITION = (x, y)


class ControlMenuCursor(MenuDependant):
    """ mouse cursor during control menu state """

    myImage = None
    me = None

    def __init__(self, stateObj, master, CLASS):

        MenuDependant.__init__(self, stateObj, master)

        self.setImage(CLASS, "controlCursor.png", (22,22), (21,21))
        self.rect = pygame.Rect(0,0,1,1)
        self.hideMe()
        CLASS.me = self
        self.firstCycle = True

    @staticmethod
    def wipe():

        ControlMenuCursor.me = None

    def updateTitle(self):
        if not self.firstCycle:
            pos = pygame.mouse.get_pos()
            self.rect.center = pos
            self.showMe()
        else:
            self.firstCycle = False

    def update(self):

        if self.onScreen:

            pos = pygame.mouse.get_pos()
            self.rect.center = pos
            self.showMe()

        else:

            self.hideMe()

    def checkCurrentPage(self, masterMenuClass):
        return True # override parent method, cursor is always visible

    def hideMe(self): # override parent method
        self.image.set_alpha(0, pygame.RLEACCEL)
        self.on = False

    def showMe(self): # override parent method
        self.image.set_alpha(255, pygame.RLEACCEL)
        self.on = True

class MessageMenuCursor(ControlMenuCursor):
    myImage = None
    me = None

    def __init__(self, stateObj, master, CLASS):
        ControlMenuCursor.__init__(self, stateObj, master, CLASS)
        CLASS.me = self

    def updateMessage(self):
        self.update()

    @staticmethod
    def wipe():

        MessageMenuCursor.me = None

class MenuGraphic(MenuDependant):
    """ a picture to display on a menu """
    imgDict = {}

    def __init__(self, stateObj, master, fileName, scaleTo, getAt, ON_PAGE, position):
        MenuDependant.__init__(self, stateObj, master)
        self.ON_PAGE = ON_PAGE
        self.setImage(fileName, scaleTo, getAt)
        self.rect = self.image.get_rect()
        self.setPosition(position)
        self.hideMe()
##        print "\ngraphic created\nself.POSITION: " + str(self.POSITION) + "\nself.ON_PAGE: " +str(self.ON_PAGE)

##    def updateMessage(self):
##        if not self.checkCurrentPage(MessageMenu):
##            self.hideMe()
##        else:
##            if self.onScreen:
##                self.showMe()
##            else:
##                self.hideMe()

##    def update(self):
##        if not self.checkCurrentPage(MessageMenu):
##            self.hideMe()
##        else:
##            if self.onScreen:
##                self.showMe()
##            else:
##                self.hideMe()

    def setImage(self, fileName, scaleTo, getAt):
        if fileName not in MenuGraphic.imgDict:
            image = dinosInSpace.loadImage(fileName, scaleTo, getAt)
            MenuGraphic.imgDict[fileName] = image
        self.image = MenuGraphic.imgDict[fileName].copy()

class PauseMenuGraphic(MenuGraphic):
    """ same as MenuGraphic, but for pause menu: has updatePause """

    def updateMessage(self):
        pass

    def update(self):
        if not self.checkCurrentPage(InPlayMenu):
            self.hideMe()
##            print "it's not my current page"
        else:
            if self.onScreen:
##                print "show me"
                self.showMe()
##                print "it's my currnet page and I AM onScreen ****************************"
            else:
## print "it's my current page but i'm not onScreen"
                self.hideMe()

class PauseMenuTextBlock(PauseMenuGraphic):

    def __init__(self, stateObj, master, textBlock, ON_PAGE, position):
        MenuDependant.__init__(self, stateObj, master)

        self.ON_PAGE = ON_PAGE
        self.image = textBlock.image.copy()
        self.rect = self.image.get_rect()
        self.setPosition(position)
        self.hideMe()


def wipe():
    BasicMenu.wipe()
    InPlayMenu.wipe()
    BasicButton.wipe()
    ControlMenuCursor.wipe()
