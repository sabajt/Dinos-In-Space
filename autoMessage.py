"""
    Message.py

    message / menu that appear as hints during game
"""

import random
import pygame

import dinosInSpace
import static56
import infoGraphic56
import tween
import soundFx56
import dataStorage56
import dinostein
import soundFx56

OFFSCREEN                   = (-2000,-2000)
ALPHA                       = 200 # sync with dinostein ALPHA

BLACK = (0,0,0)
YELLOW = (255,255, 0)
GREY = (150,150,150)
WHITE = (255,255,255)

MSG_TWEENSTART              = (1100,300)
MSG_TWEENEND                = (400,300)
MSG_TWEENSPD                = 60 #45
MSG_TWEENMODE               = "EXP"
MSG_TWEENDCLVAL             = 0.80 #0.55
MSG_TWEENDCLLEM             = 4 #3

MSG_TEXT_COLOR              = WHITE
MSG_TEXT_SIZE               = 16
MSG_TEXT_YREL1              = -65
MSG_TEXT_YREL2              = -30
MSG_TEXT_YREL3              = 5

MSG_BUTTON_YREL             = 50
MSG_BUTTON_BACK_TEXT        = "<"
MSG_BUTTON_FORWARD_TEXT     = ">"
MSG_BUTTON_TEXT_SIZE        = 15
MSG_BUTTON_TEXT_COLOR       = BLACK
MSG_BUTTON_BACK_DEST        = "BACK"
MSG_BUTTON_FORWARD_DEST     = "FORWARD"

BTTN_HEIGHT = 50
BTTN_XBUF = 12
BTTN_YBUF = 8
BTTN_MIDJUST = 3

SPIRAL_DIRECTION            = -1
SPIRAL_ROTATESTEP           = 6
SPIRAL_SCALE_STEP           = -10
SPIRAL_TERMINATEAFTER       = 20

# must set message mod to True in level56
MESSAGE_LIB = {

    "tutorial" : [
        ["hi, i'm professor dinostein, welcome to space!",
         "your job is to get all dinos from a launch pad",
         "to a space station."],

        ["the top left shows your tile inventory.",
         "these items help you guide dinos to safety.",
         "here you've got 2 arrows that can bounce dinos"],

        ["click to put an arrow down,",
        "click again to rotate it...",
        "right click or control click to pick it back up."],

        ["when you've made a complete path for the dinos,",
        "click the launch pad or use space bar to launch",
         "them. re-read this message by pressing 'm'."]
    ],

    "tut2" : [
        ["here, some arrows are bolted to the grid.",
         "you can't move or rotate these!",
         ""]
    ],

    "tut3" : [
        ["green arrows only bounce green dinos,",
        "blue arrows only bounce blue dinos ...",
        "red and yellow arrows work the same way!"]
    ],

    "tut4" : [
        ["i put new arrow colors in your inventory.",
        "cycle through tiles with 'z'",
        "or by scrolling the mouse wheel"]
    ],

    "tut5" : [
        ["these stations only take dinos",
        "of a matching color.",
        ""]
    ],

    "tut6" : [
        ["switches change the state of arrows on the grid",
        "once flipped by a dino, the change is permanent",
         ""],

        ["before launching dinos, click and hold",
        "switches to preview how they change things.",
         ""]
    ],

    "tut7" : [
        ["you'll find a set of portals in your inventory.",
        "portals warp dinos one way between locations",
         ""],

        ["place two portals, click one to initiate a link",
         "and click the other to complete the link.",
         ""]
    ],

    "odd color out" : [
        ["click the launch pad or use the space bar again",
        "after launching dinos to reset them.",
        "use control + 'r ' to clear tiles and reset dinos."],

        ["press 'return ' or 'escape ' to bring up the menu.",
        "press any key while i'm talking to ignore me",
         ""]
    ],

    "small detour" : [
        ["feeling savvy?",
        "use 't ' to toggle visibility of your inventory",
        ""]
    ],

    "go for it" : [
        ["omg a box of sugar pufz!",
        "if you get that and all dinos to a station",
        "we'll store it in the interstellar snax ship"],

        ["... for when we get the munchies.",
        "who knows what great things might happen",
        "if we get every snack?"]
    ],

    "go for it_gotSnack" : [
        ["you got the snack here,",
        "check the interstellar snax ship.",
        ""]
    ],

    "switches" : [
        ["if you forget how to do something",
        "review the controls in the pause menu.",
        ""]
    ],

    "cross paths" : [
        ["often, you have to solve puzzles",
        "multiple ways to get all the snax.",
        ""]
    ],

    "island" : [
       ["",
       "hmm...",
        ""]
    ],

    "try the hard way" : [
       ["",
       "clever dinos get snax.",
        ""]
    ],

    "corral" : [
       ["",
       "moo.",
        ""]
    ],

    "asteroid field" : [
       ["",
       "< < < over there < < <",
        ""]
    ],

    "sections" : [
       ["",
       "take things one step at a time.",
        ""]
    ],

    "sardines 2" : [
       ["not a lot of space here.",
       "how ironic.",
        ""]
    ],

    "copy cat" : [
       ["i don't see any cats here...",
       "but who knows?",
       "they could show up when we least expect."]
    ],

    "not so fast" : [
       ["",
       "snack attack!",
       ""]
    ],

    "really crowded crew" : [
       ["",
       "yikes.",
       ""]
    ],

    "rescue" : [
        ["",
        "be brave.",
        ""]
    ],

    "gateway" : [
        ["",
        "you are destined for greatness.",
        ""]
    ]


}

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):

        if not ImgLib.imgDict:

            # basic rect: size, color, topLeft=(0,0), rimSize=None, alpha=None, opaqueCenter=False
            _talkbox = dinosInSpace.loadImage("talkBoxBlack.png", "2X", (0,0), ALPHA)
            _buttonSize = (_talkbox.get_width()/2 - BTTN_XBUF, BTTN_HEIGHT)

            ImgLib.imgDict = {
                "CURSORSTD"     :   dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "TALKBOX" : dinosInSpace.loadImage("talkBoxBlack.png", "2X", (0,0), ALPHA),
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


class StdMessage(tween.TweenMenu):

    """
        message displayed for hints
        - message frame is image with rect
        - should appear at start up, and when requested by user during level
        - endMessage uses the same basic structure
    """
    me = None

    def __init__(self, stateObj, profileName, puzzleName, _fps):
        tween.TweenLeader.__init__(self)
        StdMessage.me           = self

        self.IMG                = ImgLib.getImage # shortcut to img lib

        self.minRatio           = [3,1] # quick fix image ratio must be hardcoded
        self.game               = stateObj
        self.screen             = pygame.display.get_surface()
        self.original           = self.IMG("TALKBOX")
        self.spiralSnap         = None #image to be fed into sprialOut
        self.image              = self.original.copy()
        self.rect               = self.image.get_rect()
        self.rect.center        = OFFSCREEN
        self.centerScreen       = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.profileName        = profileName
        self.puzzleName         = puzzleName

        if self.puzzleName == "go for it":
            if "sugar pufz" in dataStorage56.getSnaxRecord(self.profileName):
                self.puzzleName = "go for it_gotSnack"

        self.FONTSIZE           = 21
        self.currentDinostein   = None
        self.currentSteinFrame  = None
        self._fps = _fps
        self.lastPage = len(MESSAGE_LIB[self.puzzleName])
        self.isGoingOut = False
        self.isGoingOutFrameCount = 0
        self.terminate = False
        self.isActive = False
        self.firstCycle = True

        self.stdMessageGroup = pygame.sprite.OrderedUpdates()
        self.stdMessageGroup.add(self)

    def update(self):
        if self.isActive:
            if not self.firstCycle:
                tween.TweenMenu.update(self)

                if self.isGoingOut:
                    self.isGoingOutFrameCount += 1

                    #spr, directionAsInt, rotateStep, scaleStep, terminateAfter, frameCount, ORIGINAL
            ##        - directionAsInt -> rotate direction: -1 for right, 1 for left
            ##        - rotateStep -> degrees to rotate every frame
            ##        - scaleStep -> degrees to scale every frame (takes positive or negative)
            ##        - terminateAfter -> returns image as None after this many frames
            ##        - frameCount -> expects an iterable count from calling environment: should inc by 1 ever call
            ##        - ORIGINAL -> should be a constant of the image before rotation

                    rotateStep = SPIRAL_ROTATESTEP
                    scaleStep = SPIRAL_SCALE_STEP
                    termAfter = SPIRAL_TERMINATEAFTER
                    if self._fps == 30:
                        rotateStep *= 2
                        scaleStep *= 2
                        termAfter /= 2

                    self.terminate = spiralOut(
                        self,
                        SPIRAL_DIRECTION,
                        rotateStep,
                        scaleStep,
                        termAfter,
                        self.isGoingOutFrameCount,
                        self.minRatio,
                        self.spiralSnap
                    )
            else:
                self.firstCycle = False

    def updateMessage(self):
        """ used for game state to isolate objects to be updated during messaging """
        pass

    def makeMinions(self):
        """ only to be called after message is "requested" (artificial or user) """
        self.currentPage = 1
        self.messageLines = self.makeMessageLines(self.puzzleName)

        self.backButton = StdMessageButton(
#            (-self.rect.width/4, MSG_BUTTON_YREL),
            (-self.rect.width/4 + BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
            ImgLib.getImage("BTTN_0"),
            ImgLib.getImage("BTTN_1"),
            MSG_BUTTON_BACK_TEXT,
            MSG_BUTTON_TEXT_SIZE,
            MSG_BUTTON_TEXT_COLOR,
            MSG_BUTTON_BACK_DEST)

        self.forwardButton = StdMessageButton(
            (self.rect.width/4 - BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
            ImgLib.getImage("BTTN_0"),
            ImgLib.getImage("BTTN_1"),
            MSG_BUTTON_FORWARD_TEXT,
            MSG_BUTTON_TEXT_SIZE,
            MSG_BUTTON_TEXT_COLOR,
            MSG_BUTTON_FORWARD_DEST)

        self.addToGroupAsFollower([
            self.messageLines[0],
            self.messageLines[1],
            self.messageLines[2],
            self.backButton,
            self.forwardButton])

    def blitMinions(self):

        topleft = self.rect.topleft
        bbtopleft = self.backButton.rect.topleft
        fbtopleft = self.forwardButton.rect.topleft
        m1topleft = self.messageLines[0].rect.topleft
        m2topleft = self.messageLines[1].rect.topleft
        m3topleft = self.messageLines[2].rect.topleft

        bbBlitX = bbtopleft[0] - topleft[0]
        bbBlitY = bbtopleft[1] - topleft[1]
        fbBlitX = fbtopleft[0] - topleft[0]
        fbBlitY = fbtopleft[1] - topleft[1]
        m1BlitX = m1topleft[0] - topleft[0]
        m1BlitY = m1topleft[1] - topleft[1]
        m2BlitX = m2topleft[0] - topleft[0]
        m2BlitY = m2topleft[1] - topleft[1]
        m3BlitX = m3topleft[0] - topleft[0]
        m3BlitY = m3topleft[1] - topleft[1]

        self.spiralSnap = self.original.copy()
        self.spiralSnap.blit(self.backButton.image, (bbBlitX, bbBlitY))
        self.spiralSnap.blit(self.forwardButton.image, (fbBlitX, fbBlitY))
        self.spiralSnap.blit(self.messageLines[0].image, (m1BlitX, m1BlitY))
        self.spiralSnap.blit(self.messageLines[1].image, (m2BlitX, m2BlitY))
        self.spiralSnap.blit(self.messageLines[2].image, (m3BlitX, m3BlitY))

        self.hideRealMinions()

    def hideRealMinions(self):
        self.backButton.rect.center = (2000,2000)
        self.forwardButton.rect.center = (2000,2000)
        self.messageLines[0].rect.center = (2000,2000)
        self.messageLines[1].rect.center = (2000,2000)
        self.messageLines[2].rect.center = (2000,2000)

    def makeMessageLines(self, puzzleName):
        line1 = StdMessageTxt((0, MSG_TEXT_YREL1), MESSAGE_LIB[puzzleName][0][0], MSG_TEXT_SIZE, MSG_TEXT_COLOR)
        line2 = StdMessageTxt((0, MSG_TEXT_YREL2), MESSAGE_LIB[puzzleName][0][1], MSG_TEXT_SIZE, MSG_TEXT_COLOR)
        line3 = StdMessageTxt((0, MSG_TEXT_YREL3), MESSAGE_LIB[puzzleName][0][2], MSG_TEXT_SIZE, MSG_TEXT_COLOR)

        return line1, line2, line3

    def makeDinostein(self):
        self.currentDinostein = dinostein.Dinostein(self._fps)
        self.currentSteinFrame = dinostein.Frame(self._fps)
        self.currentDinostein.addFollower(self.currentSteinFrame)
        self.stdMessageGroup.add(self.currentSteinFrame)
        self.stdMessageGroup.add(self.currentDinostein)

    def makeCursor(self):
        cursor = StdMessageCursor(ImgLib.getImage("CURSORSTD"))
        self.stdMessageGroup.add(cursor)

    def addToGroupAsFollower(self, followers):
        """ helper method for adding list of followers """
        for f in followers:
            self.stdMessageGroup.add(f)
            self.addFollower(f)

    @staticmethod
    def reveal():

        soundFx56.SoundPlayer.requestSound("radio")
        speed = MSG_TWEENSPD # 45
        dclval = MSG_TWEENDCLVAL # 0.55
        dcllem = MSG_TWEENDCLLEM # 3

        if StdMessage.me._fps == 30:
            speed *= 2
            dclval = .60
            dcllem = 2

        StdMessage.me.terminate = False

        StdMessage.me.makeMinions()
        StdMessage.me.makeDinostein()
        StdMessage.me.makeCursor()

        StdMessage.me.setTween(MSG_TWEENSTART, MSG_TWEENEND, speed, MSG_TWEENMODE, dclval, dcllem)
        StdMessage.me.startTween()
        StdMessage.me.currentDinostein.setAndStartTween()

    @staticmethod
    def checkButtonPressed():
        """ called upon mouse click """
        dest = None
        for spr in StdMessage.me.stdMessageGroup:
            if spr.__class__ == StdMessageButton:
                dest = spr.requestDest()
                if dest:
                    break

        return dest

    @staticmethod
    def pageBack():
        if StdMessage.me.currentPage > 1:
            # play sound
            StdMessage.me.currentPage -= 1
            lineCount = 0
            for line in StdMessage.me.messageLines:
                line.rerender(MESSAGE_LIB[StdMessage.me.puzzleName][StdMessage.me.currentPage - 1][lineCount])
                lineCount += 1
        else:
            pass # play sound

    @staticmethod
    def pageForward():
        if StdMessage.me.currentPage < StdMessage.me.lastPage:
            # play sound
            StdMessage.me.currentPage += 1
            lineCount = 0
            for line in StdMessage.me.messageLines:
                line.rerender(MESSAGE_LIB[StdMessage.me.puzzleName][StdMessage.me.currentPage - 1][lineCount])
                lineCount += 1
        else:
            # play sound
            return "LAST" # tell game state to exit loop

    @staticmethod
    def setIsGoingOut(isGoingOut):
        if isGoingOut and not StdMessage.me.isGoingOut:
            soundFx56.SoundPlayer.requestSound("woosh_a")
            StdMessage.me.isGoingOutFrameCount = 0
            StdMessage.me.isGoingOut = isGoingOut
            StdMessage.me.blitMinions()

            # dinostein
            if StdMessage.me.currentDinostein:
                StdMessage.me.currentDinostein.kill()
                StdMessage.me.currentSteinFrame.closing = isGoingOut


    @staticmethod
    def resetAll():
        StdMessage.me.image = StdMessage.me.original
        StdMessage.me.rect = StdMessage.me.image.get_rect()
        StdMessage.me.isGoingOutCount = 0
        StdMessage.me.isGoingOut = False

        if StdMessage.me.currentDinostein:
            StdMessage.me.currentDinostein.kill()
        if StdMessage.me.currentSteinFrame:
            StdMessage.me.currentSteinFrame.kill()
        if StdMessageCursor.me:
            StdMessageCursor.me.kill()
        StdMessageCursor.wipe()

        StdMessage.me.reset()
        StdMessage.me.rect.center = OFFSCREEN

    @staticmethod
    def wipe():
        StdMessage.me = None


class StdMessageTxt(tween.TweenFollower):
    """ compound tween follower and text object: child of tween follower, contains a text object
        - follows msg bubble tween and can rerender text
    """

    def __init__(self, relPos, text, fontSize, fontColor):
        tween.TweenFollower.__init__(self, relPos)
        self.textObject = infoGraphic56.TextObject(text, fontSize, fontColor)

        self.image = self.textObject.image
        self.rect = self.image.get_rect()
        self.fontColor = fontColor

    def updateMessage(self):
        """ used for game state to isolate objects to be updated during messaging """
        pass

    def rerender(self, text):
        """ change text, set image, set rect, allign center """
        center = self.rect.center
        self.textObject.rerender(text, self.fontColor)
        self.image = self.textObject.image
        self.rect = self.image.get_rect()
        self.rect.center = center


class StdMessageButton(tween.TweenFollower):
    """
        Button that belongs to StdMessage
        - is a TweenFollower *** don't override moveFollower()
        - returns dest when clicked
        - dest can be restart, quick restart, continue (study solution), back (select screen)
    """

    def __init__(self, relPos, imageOff, imageOver, text, textSize, textColor, dest):
        tween.TweenFollower.__init__(self, relPos)

        self.imageOff       = self.makeButton(imageOff, text, textSize, textColor)
        self.imageOver      = self.makeButton(imageOver, text, textSize, textColor)
        self.image          = self.imageOff
        self.rect           = self.image.get_rect()
        self.dest           = dest
        self.mouseOver      = False
        self.isActive       = False
        self.firstCycle     = True

    def update(self):
        if self.isActive:
            if not self.firstCycle:
                self.checkCursorOver()
            else:
                self.firstCycle = False

    def updateMessage(self):
        """ used for game state to isolate objects to be updated during messaging """
        pass

    def makeButton(self, image, text, textSize, textColor):
        textSurf = infoGraphic56.TextObject(text, textSize, textColor).image
        xBlit = (image.get_width() - textSurf.get_width())/2
        yBlit = (image.get_height() - textSurf.get_height())/2
        image.blit(textSurf, (xBlit, yBlit))

        return image

    def checkCursorOver(self):
        """ if cursor over button set respective image and mouseOver """
        if pygame.sprite.collide_rect(self, StdMessageCursor.me):
            self.image = self.imageOver
            self.mouseOver = True
        else:
            self.image = self.imageOff
            self.mouseOver = False

    def requestDest(self):
        """ returns dest if mouseOver """
        dest = None
        if self.mouseOver:
            dest = self.dest

        return dest

class StdMessageCursor(pygame.sprite.Sprite):
    """ cursor used during end message """
    me = None

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = pygame.rect.Rect((0,0,1,1))
        self.rect.center = (-2000,-2000)
        self.isActive = False
        self.firstCycle = True

        StdMessageCursor.me = self

    def update(self):
        if self.isActive:
            if not self.firstCycle:
                self.rect.center = pygame.mouse.get_pos()
            else:
                self.firstCycle = False

    def updateMessage(self):
        """ used for game state to isolate objects to be updated during messaging """
        pass

    @staticmethod
    def wipe():
        StdMessageCursor.me = None


def quickReset():
    if StdMessage.me:
        StdMessage.resetAll()

# quick fix: copied from gfx56 because of import bug
def spiralOut(spr, directionAsInt, rotateStep, scaleStep, terminateAfter, frameCount, minRatio, ORIGINAL):
    """ update callback for a sprite to 'spiral out' of view in place using a set image
        returns false if spiral hasn't terminated

        - directionAsInt -> rotate direction: -1 for right, 1 for left
        - rotateStep -> degrees to rotate every frame
        - scaleStep -> degrees to scale every frame (takes positive or negative)
        - terminateAfter -> returns image as None after this many frames
        - frameCount -> expects an iterable count from calling environment: should inc by 1 ever call
        - ORIGINAL -> should be a constant of the image before rotation
    """

    terminate = True

    if frameCount <= terminateAfter:
        center = spr.rect.center
        newImg = pygame.transform.scale(
            ORIGINAL,
            (ORIGINAL.get_width() + scaleStep*minRatio[0]*frameCount, ORIGINAL.get_height() + scaleStep*minRatio[1]*frameCount)
        )
        spr.image = pygame.transform.rotate(newImg, directionAsInt*rotateStep*frameCount)
        spr.rect = spr.image.get_rect()
        spr.rect.center = center
        terminate = False

    return terminate



def wipe():
    StdMessage.wipe()
    StdMessageCursor.wipe()



##    def lose(self):
##        soundFx56.SoundPlayer.requestSound("lose")
##
##        line1, line2, line3 = self.generateMessage(False)
##
##        # init features from data and register for access
##        quickReset = EndMessageButton((-170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Quick Reset", SIZE_BTEXT, COL_BTEXT, "QR")
##        reset = EndMessageButton((0,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Clear & Reset", SIZE_BTEXT, COL_BTEXT, "HR")
##        exit = EndMessageButton((170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Leave Area", SIZE_BTEXT, COL_BTEXT, "EXIT")
##        text1 = EndMessageText((0,-50), line1, self.FONTSIZE, (0,0,0))
##        text2 = EndMessageText((0,-25), line2, self.FONTSIZE, (0,0,0))
##        text3 = EndMessageText((0,0), line3, self.FONTSIZE, (0,0,0))
##
##        self.currentDinostein = dinostein.Dinostein(self._fps)
##        self.currentSteinFrame = dinostein.Frame(self._fps)
##        self.currentDinostein.addFollower(self.currentSteinFrame)
##
##        cursor = EndMessageCursor([self.IMG("CURSORSTD")])
##
##        self.bind([quickReset, reset, exit, text1, text2, text3])
##        self.endMessageGroup.add(self.currentDinostein)
##        self.endMessageGroup.add(self.currentSteinFrame)
##        self.endMessageGroup.add(cursor)
##
##        #self.setTween((1000,300), (400,300), 35, "EXP", 0.5, 3) # sp, ep, speed, dclMode, dclVal, dclLim
##        self.setTween(MSG_TWEENSTART, MSG_TWEENEND, 45, "EXP", 0.55, 3)
##        self.currentDinostein.setAndStartTween()
##
##        self.startTween()
##        self.end = True
##        self.game.setIsEnding()
##
##    def win(self):
##        soundFx56.SoundPlayer.requestSound("win")
##
##        snax = BonusDelegate.snax
##
##        if self.profileName != "_user":
##            dataStorage56.modProfile(self.profileName, self.curPuzzle, True, snax) # modify file
##            puzzleData  = dataStorage56.getPuzzleData(self.profileName, self.curPuzzle)
##
##            # add snack collected to snack archive for user viewing
##
##        else:
##            puzzleData = "_user"
##
##        if snax:
##            for s in snax:
##                s.unregister()
##
##        line1, line2, line3 = self.generateMessage(True, puzzleData)
##
##        quickReset  = EndMessageButton((-170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Quick Reset", SIZE_BTEXT, COL_BTEXT, "QR")
##        reset       = EndMessageButton((0,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Clear & Reset", SIZE_BTEXT, COL_BTEXT, "HR")
##        exit        = EndMessageButton((170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Leave Area", SIZE_BTEXT, COL_BTEXT, "EXIT")
##        text1       = EndMessageText((0,-50), line1, self.FONTSIZE, (0,0,0))
##        text2       = EndMessageText((0,-25), line2, self.FONTSIZE, (0,0,0))
##        text3       = EndMessageText((0,0), line3, self.FONTSIZE, (0,0,0))
##        cursor      = EndMessageCursor([self.IMG("CURSORSTD")])
##
##        # dinostein ***
##        self.currentDinostein = dinostein.Dinostein(self._fps)
##        self.currentSteinFrame = dinostein.Frame(self._fps)
##        self.currentDinostein.addFollower(self.currentSteinFrame)
##        # *************
##
##        self.bind([quickReset, reset, exit, text1, text2, text3])
##        self.endMessageGroup.add(self.currentDinostein)
##        self.endMessageGroup.add(self.currentSteinFrame)
##        self.endMessageGroup.add(cursor)
##
##        self.setTween(MSG_TWEENSTART, MSG_TWEENEND, 45, "EXP", 0.55, 3)
##        self.currentDinostein.setAndStartTween()
##        self.startTween()
##        self.end = True
##        self.game.setIsEnding()

##    @staticmethod
##    def quickReset():
##        if EndMessage.me.currentDinostein:
##            EndMessage.me.currentDinostein.kill()
##            EndMessage.me.currentSteinFrame.kill()
##        if EndMessageCursor.me:
##            EndMessageCursor.me.kill()
##        EndMessageCursor.wipe()
##        EndMessage.me.reset()
##        EndMessage.me.rect.center = OFFSCREEN
##        EndMessage.me.end = False

