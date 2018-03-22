""" infoGraphic56.py """

import pygame
import soundFx56
import dinosInSpace
import interface56
import controlMenu56
import os
import autoMessage

WHITE = (255,255,255)
BLACK = (0,0,0)

SPAWN_INFO_FONTSIZE = 15
MSG_SUB_FONTSIZE = 10

class TextObject(pygame.sprite.Sprite):
    """ superclass for a text sprite """

    def __init__(self, text, size, color, center=None, antialias=True, editorFont=False, bkgColor=None):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.bkgColor = bkgColor

#        try:
#            self.font = pygame.font.Font("dos.ttf", size)
#        except:
#            print "could not load font dos.ttf"

        self.font = dinosInSpace.FontBank.getFont(size, editorFont)

        self.text = text
        if self.bkgColor:
            self.image = self.font.render(text, True, color, self.bkgColor) #anti
        else:
            self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()

        if center:
            self.rect.center = center

    def rerender(self, text=None, color=None, center=None):
        if text:
            self.text = text
        else:
            self.text = ""
        if color:
            self.color = color

        if self.bkgColor:
            self.image = self.font.render(self.text, True, self.color, self.bkgColor) #false
        else:
            self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if center:
            self.rect.center = center


class TextBlock(pygame.sprite.Sprite):
    """ takes a list of strings and puts into a text block """

    def __init__(self, textList, fontSize, fontColor, addHeight=0, addSpace=0, editorFont=False, rightJustify=False):
        pygame.sprite.Sprite.__init__(self)

        self.font = dinosInSpace.FontBank.getFont(fontSize, editorFont)
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.addHeight = addHeight
        self.addSpace = addSpace
        self.editorFont = editorFont
        self.rightJustify = rightJustify
        self.image = self.formatText(textList)
        self.rect = self.image.get_rect()

    def formatText(self, textList):
        """ return textblock surface """
        rTextList = [] # rendered text objects
        widthList = [] # to get longest line for box

        for line in textList:
            rLine = TextObject(line, self.fontSize, self.fontColor, None, True, self.editorFont)
            w = rLine.image.get_width()
            widthList.append(w)
            rTextList.append(rLine)

        largestWidth = 0

        for w in widthList:
            if w > largestWidth:
                largestWidth = w

        boxWidth = largestWidth
        boxHeight = len(rTextList) * self.fontSize

        textSurface = pygame.Surface((boxWidth, boxHeight + self.addHeight))

#        if self.fontColor != WHITE:
#            textSurface.fill(WHITE)
#            textSurface.set_colorkey(WHITE, pygame.RLEACCEL)
#        else:
#            textSurface.fill(BLACK)
#            textSurface.set_colorkey(BLACK, pygame.RLEACCEL)

        if self.fontColor != BLACK:
            textSurface.fill(BLACK)
            textSurface.set_colorkey(BLACK, pygame.RLEACCEL)
        else:
            textSurface.fill(WHITE)
            textSurface.set_colorkey(WHITE, pygame.RLEACCEL)

        y = 0

        for rT in rTextList:
            if not self.rightJustify:
                textSurface.blit(rT.image, (0, y))
            else:
                textSurface.blit(rT.image, (textSurface.get_width() - rT.image.get_width(), y))
            y += self.fontSize + self.addSpace

        return textSurface

class InfoGraphic(pygame.sprite.Sprite):
    """ superclass for game-info that can be set visible or not visible """
    IG_List = []
    visible = True

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        InfoGraphic.IG_List.append(self)

    @staticmethod
    def wipe():
        InfoGraphic.IG_List = []
        InfoGraphic.visible = True

    @staticmethod
    def toggle():
        soundFx56.GameSoundManager.registerSound("toggle")

        if InfoGraphic.visible:
            InfoGraphic.hideAll()
            InfoGraphic.visible = False
        else:
            InfoGraphic.showAll()
            InfoGraphic.visible = True

    @staticmethod
    def showAll():
        for i in InfoGraphic.IG_List:
            i.showMe()

    @staticmethod
    def hideAll():
        for i in InfoGraphic.IG_List:
            i.hideMe()

    def hideMe(self):
        self.image.set_alpha(0, pygame.RLEACCEL)

    def showMe(self):
        self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)

class FPS(InfoGraphic):
    """ displays frames per second """

    def __init__(self, game):
        InfoGraphic.__init__(self)

        self.game = game
        self.ALPHA = 255
        self.font = dinosInSpace.FontBank.getFont(25)
        w = pygame.display.get_surface().get_width()
        self.TR = (w, 20)

        if self.game:
            if game.__class__ == dinosInSpace.Game:
                fpsGroup = pygame.sprite.RenderUpdates(self)
                game.addGroup(fpsGroup)

    def update(self, moveLeft=None):
        f = str(int(self.game.getCurrentClock().get_fps()))
        text = f + " fps "

        if InfoGraphic.visible:

            self.image = self.font.render(text, True, (255,255,255))
            self.rect = self.image.get_rect()
            self.rect.topright = self.TR

        if moveLeft:
            self.rect.left -= moveLeft

    def updateMessage(self):
        self.update()

    def updateEnding(self):
        self.update(100)

    def updatePause(self):
        self.update()

class SpawnInfoBox(pygame.sprite.Sprite):
    """ displays num, direction & color of dinos that come out of a spawn """
    counter = 0 # tracks every box created, use to sync with spawn
    allBoxGroup = pygame.sprite.RenderUpdates()
    imgGreen = None
    imgRed = None
    imgBlue = None
    imgYellow = None
    imgDirection = None

    def __init__(self, game, dinoData):
        pygame.sprite.Sprite.__init__(self)
        SpawnInfoBox.counter += 1
        self.FONTSIZE = SPAWN_INFO_FONTSIZE
        self.ALPHA = 200
        self.FL_DELAY = 10
        self.visible = False
        self.flickerDelay = self.FL_DELAY
        self.game = game
        self.font = dinosInSpace.FontBank.getFont(self.FONTSIZE)
        self.textColor = (0,0,0)
        self.iconSize = (26,26)
        self.loadImages()
        imageKey = self.getImageKey(dinoData)
        self.image = self.getBoxImage(imageKey)
        self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        SpawnInfoBox.allBoxGroup.add(self)

    def update(self):
        if self.visible:
            self.flicker()

    def flicker(self):
        self.flickerDelay -= 1

        if self.flickerDelay < 1:
            self.image.set_alpha(40, pygame.RLEACCEL)
            self.flickerDelay = self.FL_DELAY
        else:
            self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)

    @staticmethod
    def wipe():
        SpawnInfoBox.counter = 0
        SpawnInfoBox.allBoxGroup = pygame.sprite.RenderUpdates()

    @staticmethod
    def setLoc():
        h = interface56.ItemMenu.getHeight()
        for s in SpawnInfoBox.allBoxGroup:
            s.rect.topleft = (0, h)

    @staticmethod
    def addToGame(game):
        game.addGroup(SpawnInfoBox.allBoxGroup)

    def showMe(self):
        self.visible = True
        self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)

    def hideMe(self):
        self.visible = False
        self.image.set_alpha(0, pygame.RLEACCEL)

##    def getBoxImage(self, imageKey):
##        """ return box surface with all images drawn together """
##
##        OFFSET = 4
##        sqSide = self.iconSize[0]
##        boxWidth = len(imageKey) * sqSide + ((len(imageKey) + 1) * OFFSET)
##        boxHeight = sqSide * 2 + (2 * OFFSET)
##        box = pygame.Surface((boxWidth, boxHeight))
##        box.fill((103,99,103))
##        r = box.get_rect()
##        pygame.draw.rect(box, (255,255,255), r, 2)
##
##        imageSeq = []
##        x = OFFSET + self.iconSize[0]/2
##
##        for keySet in imageKey:
##
##            y = OFFSET + self.iconSize[0]/2
##
##            for key in keySet:
##
##                image = self.getImage(key)
##                imgW = image.get_width()
##                imgH = image.get_height()
##                blitX = x - imgW/2
##                blitY = y - imgH/2
##                box.blit(image, (blitX, blitY))
##                y += sqSide #
##
##            x += sqSide + OFFSET #
##
##        return box

    def getBoxImage(self, imageKey):
        """ return box surface with all images drawn together """

        OFFSET = 4
        sqSide = self.iconSize[0]
        boxWidth = len(imageKey) * sqSide + ((len(imageKey) + 1) * OFFSET)
        boxHeight = sqSide * 2 + (2 * OFFSET)
        box = pygame.Surface((boxWidth, boxHeight))
        box.fill((103,99,103))
        r = box.get_rect()
        pygame.draw.rect(box, (255,255,255), r, 2)

        imageSeq = []
        x = OFFSET + self.iconSize[0]/2

        for keySet in imageKey:
            y = OFFSET + self.iconSize[0]/2

            for key in keySet:
                image = self.getImage(key)
                if image:
                    imgW = image.get_width()
                    imgH = image.get_height()
                    blitX = x - imgW/2
                    blitY = y - imgH/2
                    box.blit(image, (blitX, blitY))
                y += sqSide
            x += sqSide + OFFSET

        return box

    def getImage(self, key):
        """ return image """
        if key == "green" or key == "red" or key == "blue" or key == "yellow":
            if key == "green":
                image = SpawnInfoBox.imgGreen.copy()
            elif key == "red":
                image = SpawnInfoBox.imgRed.copy()
            elif key == "blue":
                image = SpawnInfoBox.imgBlue.copy()
            elif key == "yellow":
                image = SpawnInfoBox.imgYellow.copy()
        elif type(key) == int:
            image = self.font.render(str(key), True, self.textColor)
        else:
            image = None

        return image

    def loadImages(self):
        if not SpawnInfoBox.imgGreen:
            s = self.iconSize
            SpawnInfoBox.imgGreen = dinosInSpace.loadImage("miniDinoG.png", s, (0,0))
            SpawnInfoBox.imgBlue = dinosInSpace.loadImage("miniDinoB.png", s, (0,0))
            SpawnInfoBox.imgRed = dinosInSpace.loadImage("miniDinoR.png", s, (0,0))
            SpawnInfoBox.imgYellow = dinosInSpace.loadImage("miniDinoY.png", s, (0,0))
            SpawnInfoBox.imgDirection = dinosInSpace.loadImage("spawnDir.png", s, (0,0))

    def getImageKey(self, dinoData):
        """ returns imageKey that is used to order images on the box """
        imageKey = [] # [ (2, "green"), ... ]
        num = 0
        DSTEP = 25

        # collect data sets from dinoData that match this spawn
        myData = [] # extracted whole dino data sets for this spawn
        slotList = [] # just the slot number, from this spawn

        for dataSet in dinoData:
            if dataSet[4] == SpawnInfoBox.counter:
                myData.append(dataSet)
                slotList.append(dataSet[-2]/DSTEP)


        # get number of slots (full + empty) to be displayed on box / create key
        dinoCount = 0

        slotRange = range(int(slotList[-1]))
        for slot in list(slotRange):
            if (slot + 1) in slotList: # if slot has a dino match
                color = myData[dinoCount][2]
                dinoCount += 1
            else:
                color = None
            imageKey.append((slot + 1, color))
        return imageKey

class MessageStub(InfoGraphic):
    """ shows user if message / tip is waiting """
    font = None
    txtNoneGrey = None # text "no message"
    txtNoneRed = None # "no message" in red
    txtWaiting1 = None # text "message waiting:"
    txtWaiting2 = None # text "press f"
    box = None # surface bkg
    noMsg = None # text + box
    noMsgRed = None # text + box
    msgWaiting = None # text + box
    flashing = False # for noMsgRed timer if request denied
    myGroup = pygame.sprite.RenderUpdates()
    me = None

    def __init__(self, game, hasMessage):
        InfoGraphic.__init__(self)

        self.ALPHA = 180
        self.game = game
        self.flashTimer = 3
        self.hasMessage = hasMessage
        self.fontSize = MSG_SUB_FONTSIZE
        self.fontColor = (255,255,255)
        self.setBoxSize(100)
        self.boxColor = (0,0,0)
        self.setFont()
        self.setText()
        self.setBox()
        self.setCombinedImg()

        if hasMessage:
            self.setImage(MessageStub.msgWaiting)
            self.startUp = True
        else:
            self.setImage(MessageStub.noMsg)
            self.startUp = False

        self.rect = self.image.get_rect()
        self.setPos()
        MessageStub.me = self
        MessageStub.myGroup.add(self)

    def update(self):
        if self.startUp:
            MessageStub.requestShowMsg()
            self.game.setMessage(True)
            self.startUp = False
        if self.flashing:
            self.flashText()

    @staticmethod
    def wipe():
        MessageStub.myGroup = pygame.sprite.RenderUpdates()
        MessageStub.me = None
        MessageStub.flashing = False

    @staticmethod
    def requestShowMsg():
        if MessageStub.me.hasMessage:
            ##interface56.Cursor.hideDuringMessages() # hides cursor stuff so won't be on background screenshot
            autoMessage.StdMessage.reveal()
            return True
        else:
            soundFx56.GameSoundManager.registerSound("noRecover")
            if MessageStub.me.visible:
                MessageStub.flashing = True
            return False

##    @staticmethod
##    def requestShowMsg():
##        if MessageStub.me.hasMessage:
##            controlMenu56.MessageMenu.toggle(True)
##            return True
##        else:
##            soundFx56.GameSoundManager.registerSound("noRecover")
##            if MessageStub.me.visible:
##                MessageStub.flashing = True
##            return False

    def flashText(self):
        if self.flashTimer > 0:
            self.setImage(MessageStub.noMsgRed)
            self.flashTimer -= 1
        else:
            self.setImage(MessageStub.noMsg)
            self.flashTimer = 5
            MessageStub.flashing = False


    def setBoxSize(self, width):
        w = width
        h = interface56.ItemMenu.getHeight()
        self.boxSize = (w, h)

    def setFont(self):
        if not MessageStub.font:
            MessageStub.font = self.font = dinosInSpace.FontBank.getFont(self.fontSize)

    def setText(self):
        if not MessageStub.msgWaiting:
            MessageStub.txtWaiting1 = MessageStub.font.render("see message", True, self.fontColor)
            MessageStub.txtWaiting2 = MessageStub.font.render("press m", True, self.fontColor)
            MessageStub.txtNoneGrey = MessageStub.font.render("no message", True, self.fontColor)
            MessageStub.txtNoneRed = MessageStub.font.render("no message", True, (255,0,0))

    def setBox(self):
        if not MessageStub.box:
            MessageStub.box = pygame.Surface(self.boxSize)
            MessageStub.box.fill(self.boxColor)
            MessageStub.box.set_alpha(self.ALPHA, pygame.RLEACCEL)
            r = MessageStub.box.get_rect()
            pygame.draw.rect(MessageStub.box, (255,255,255), r, 2)

    def setCombinedImg(self):
        if not MessageStub.noMsg:
            bW = MessageStub.box.get_width()
            bH = MessageStub.box.get_height()
            txtNoneW = MessageStub.txtNoneGrey.get_width()
            txtNoneH = MessageStub.txtNoneGrey.get_height()
            txtWait1W = MessageStub.txtWaiting1.get_width()
            txtWait1H = MessageStub.txtWaiting1.get_height()
            txtWait2W = MessageStub.txtWaiting2.get_width()
            txtWait2H = MessageStub.txtWaiting2.get_height()

            MessageStub.noMsg = MessageStub.box.copy()
            MessageStub.noMsgRed = MessageStub.box.copy()
            MessageStub.msgWaiting = MessageStub.box.copy()

            center = ( (bW/2 - txtNoneW/2), (bH/2 - txtNoneH/2) )
            MessageStub.noMsg.blit(MessageStub.txtNoneGrey, center)
            MessageStub.noMsgRed.blit(MessageStub.txtNoneRed, center)

            topCenter = ( (bW/2 - txtWait1W/2), (bH/3 - txtWait1H/2) )
            bottomCenter = ( (bW/2 - txtWait2W/2), ( (2 * bH/3) - txtWait2H/2) )
            MessageStub.msgWaiting.blit(MessageStub.txtWaiting1, topCenter)
            MessageStub.msgWaiting.blit(MessageStub.txtWaiting2, bottomCenter)

    def setImage(self, image):
        self.image = image.copy()

    def setPos(self):
        self.rect.topleft = (interface56.ItemMenu.getWidth(),0)


def wipe():
    InfoGraphic.wipe()
    SpawnInfoBox.wipe()
    MessageStub.wipe()