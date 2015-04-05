"""
    EndMessage.py

    message / menu that appears upon completion or failure of puzzle
    EndMessage.win is where puzzle profile data is modified after completion
"""

import pygame
import dinosInSpace
import static56
import infoGraphic56
import tween
import soundFx56
import dino56
import dataStorage56
import snack
import random
import dinostein
import sparkleTrail
import spriteBasic

OFFSCREEN       = (-1000,-1000)
ALPHA           = 200

BLACK = (0,0,0)
YELLOW = (255,255, 0)
BLUE = (0,0,255)
GREY = (150,150,150)
WHITE = (255,255,255)

COL_BTEXT       = BLACK
COL_MTEXT       = WHITE
SIZE_BTEXT      = 15
SIZE_MTEXT      = 15

BTTN_HEIGHT = 50
BTTN_XBUF = 12
BTTN_YBUF = 8
BTTN_MIDJUST = 3

MSG_TEXT_YREL1              = -65
MSG_TEXT_YREL2              = -30
MSG_TEXT_YREL3              = 5

MSG_TWEENSTART              = (1100,300)
MSG_TWEENEND                = (400,300)
MSG_TWEENSPD                = 60 #45
MSG_TWEENMODE               = "EXP"
MSG_TWEENDCLVAL             = 0.80 #0.55
MSG_TWEENDCLLEM             = 4 #3

SPIRAL_DIRECTION            = -1
SPIRAL_ROTATESTEP           = 6
SPIRAL_SCALE_STEP           = -10
SPIRAL_TERMINATEAFTER       = 20

SPARK_SIZE      = (6,6)
SPARK_COLOR     = BLUE
SPARK_BOUNDS    = (20,20)
SPARK_FREQUENCY = 1
SPARK_FADESPEED = 10

LAST_TUTORIAL = "tut7" # used in win to check if last %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LAST_TUTORIAL %%%%%%%%%%%%%%%%%%%%%%%%%%

def getExlaim():
    wordList = [
        "Yowza!",
        "Check it yo!",
        "Wowzies!",
        "Yowzies!",
        "Look!",
        "Jeepers!",
        "OoOoOoOo!",
    ]
    return wordList[random.randint(0, len(wordList) - 1)]

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:

            _talkbox = dinosInSpace.loadImage("talkBoxBlack.png", "2X", (0,0), ALPHA)
            _buttonSize = (_talkbox.get_width()/2 - BTTN_XBUF, BTTN_HEIGHT)

            ImgLib.imgDict = {
                "CURSORSTD"     :   dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
#                "BTTN_0"        :   dinosInSpace.loadImage("button0.png", "2X", (0,0)),
#                "BTTN_1"        :   dinosInSpace.loadImage("button1.png", "2X", (0,0)),
                ##"TALKBOX" : dinosInSpace.loadImage("talkBoxBlack.png", "2X", None, ALPHA),
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
            print "image, " + name + " not found"

def initImgLib():
    ImgLib()

class BonusDelegate(object):
    """
        a simple object to hold snax collected or alt exits taken during puzzle
        - data stored here and retrieved by EndMessage if player wins
    """
    snax        = []

    @staticmethod
    def wipe():
        BonusDelegate.snax      = []

    @staticmethod
    def quickReset():
        BonusDelegate.wipe()

class EndMessage(tween.TweenMenu):
    """
        message displayed upon failing or completing puzzle
        - message is subclass of tween sprite and message frame is image with rect
        - creates and controlls features determined by puzzle outcome
    """
    me = None

    def __init__(self, stateObj, mustSave, profileName, curPuzzle, _fps):
        tween.TweenLeader.__init__(self)

        EndMessage.me           = self
        self.IMG                = ImgLib.getImage # shortcut to img lib
        self.minRatio           = [3,1] # quick fix image ratio must be hardcoded
        self.game               = stateObj
        self.screen             = self.game.getScreen()
        self.image              = self.IMG("TALKBOX")
        self.original           = self.image.copy()
        self.spiralSnap         = None #image to be fed into sprialOut
        self.rect               = self.image.get_rect()
        self.rect.center        = OFFSCREEN
        self.centerScreen       = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.mustSave           = mustSave
        self.end                = False
        self.endMessageGroup    = pygame.sprite.OrderedUpdates()
        self.profileName        = profileName
        self.curPuzzle          = curPuzzle
        self.currentDinostein   = None
        self.currentSteinFrame  = None
        self._fps =             _fps
        self.isGoingOut         = False
        self.isGoingOutFrameCount = 0
        self.terminate          = False
        self.isActive           = False # activate after screenshot for state change
        self.firstCycle         = True # state change bug

        self.speed = MSG_TWEENSPD # 45
        self.dclval = MSG_TWEENDCLVAL # 0.55
        self.dcllim = MSG_TWEENDCLLEM # 3
        if self._fps == 30:
            self.speed *= 2
            self.dclval = .60
            self.dcllim = 2

        self.endMessageGroup.add(self)

    def update(self):
        self.checkEndCondition()
        if self.isActive:
            if not self.firstCycle:
                tween.TweenMenu.update(self)

                if self.isGoingOut:
                    self.isGoingOutFrameCount += 1

                    rotateStep = SPIRAL_ROTATESTEP
                    scaleStep = SPIRAL_SCALE_STEP
                    termAfter = SPIRAL_TERMINATEAFTER
                    if self._fps == 30:
                        rotateStep *= 2
                        scaleStep *= 2
                        termAfter /= 2

                    #spr, directionAsInt, rotateStep, scaleStep, terminateAfter, frameCount, minRatio, ORIGINAL
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

    def updateEnding(self):
        """ for state change identification purpose """
        pass

    @staticmethod
    def wipe():
        EndMessage.me = None

    def checkEndCondition(self):
        if not self.end:
            if static56.Goal.getSaved() >= self.mustSave:
                self.win()
            if dino56.Dino.getLost() > 0:  ## instead return coord and pic?
                self.lose()

    def generateMessage(self, didWin, data=None, newSnax=None):
        line1 = ""
        line2 = ""
        line3 = ""

        if not didWin:
            line1 = ""
            line2 = "Dino Down, try again!"
            line3 = ""

        elif data == "_user":
            line1 = ""
            line2 = "Good work, you got all dinos to a station"

        elif data == "TUTORIAL":
            line1 = "Good job"

        else:
            assert(data)
            if not newSnax:
                line1 = "Good work, you got all dinos to a Station."
            else:
                line1 = "you got all dinos to a station and " + str(len(newSnax)) + " new snax!"

            snax                = data[4]
            snaxLeft            = 0
            itLooks_theyLook    = "it looks"
            theres_thereAre     = "there's"

            if snax:
                for s in snax:
                    if s == 0:
                        snaxComp = False
                        snaxLeft += 1

            if snaxLeft > 1:
                theres_thereAre = "there are"
                itLooks_theyLook = "they look"

            if snaxLeft:
                line2 = "It appears " + theres_thereAre + " " + str(snaxLeft) + " snax still in the area..."
                line3 = "and " +  itLooks_theyLook + " REALLY tasty!"

            else:
                line2 = ""

        return line1, line2, line3
#    # puzzle name   :   [file name, locked, complete, difficulty, snacks collected, secret exit found]
#    #
#    #   -0 (string) _file name_     : passed as 'dest' to map selector (level)
#    #   -1 (bool)   _locked_        : controlls player access / preview
#    #   -2 (bool)   _complete_      : displays if complete, adds to global profile completed count
#    #   -3 (int)    _difficulty_    : displays difficulty level
#    #   -4 (list)   _snacks_        : displays how many snacks collected as fraction, pass 'None' if n/a

    @staticmethod
    def checkButtonPressed():
        dest = None
        for s in EndMessage.me.endMessageGroup:
            if s.__class__ == EndMessageButton:
                dest = s.requestDest()
                if dest:
                    break

        return dest

    def bind(self, followers):
        for f in followers:
            self.endMessageGroup.add(f)
            self.addFollower(f)

    def lose(self):
        endDinoImage, endDinoCenter = dino56.Dino.getLastDinoImageAndCenter()

##        soundFx56.SoundPlayer.requestSound("lose")

        line1, line2, line3 = self.generateMessage(False)

        # init features from data and register for access

        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            self.retryButton = EndMessageButton(
                (-self.rect.width/4 + BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                "Retry (any key)",
                SIZE_BTEXT,
                COL_BTEXT,
                "QR"
            )
            self.exitButton = EndMessageButton(
                (self.rect.width/4 - BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                "choose another puzzle",
                SIZE_BTEXT,
                COL_BTEXT,
                "EXIT"
            )
        else:
            self.retryButton = EndMessageButton(
                (0, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                "Retry",
                SIZE_BTEXT,
                COL_BTEXT,
                "QR"
            )
        ##(170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Leave Area", SIZE_BTEXT, COL_BTEXT, "EXIT")

        self.text1 = EndMessageText((0, MSG_TEXT_YREL1), line1, SIZE_MTEXT, COL_MTEXT)
        self.text2 = EndMessageText((0, MSG_TEXT_YREL2), line2, SIZE_MTEXT, COL_MTEXT)
        self.text3 = EndMessageText((0, MSG_TEXT_YREL3), line3, SIZE_MTEXT, COL_MTEXT)

        # dinostein ***
        self.currentDinostein = dinostein.Dinostein(self._fps)
        self.currentSteinFrame = dinostein.Frame(self._fps)
        self.currentDinostein.addFollower(self.currentSteinFrame)
        # *************

        cursor = EndMessageCursor([self.IMG("CURSORSTD")]) # true for withTrail - winning condition only

        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            self.bind([self.retryButton, self.exitButton, self.text1, self.text2, self.text3])
        else:
            self.bind([self.retryButton, self.text1, self.text2, self.text3])
        self.endMessageGroup.add(self.currentSteinFrame)
        self.endMessageGroup.add(self.currentDinostein)
        self.endMessageGroup.add(cursor)

        #self.setTween((1000,300), (400,300), 35, "EXP", 0.5, 3) # sp, ep, speed, dclMode, dclVal, dclLim
        self.setTween(MSG_TWEENSTART, MSG_TWEENEND, self.speed, MSG_TWEENMODE, self.dclval, self.dcllim)
        self.currentDinostein.setAndStartTween()
        self.startTween()
        self.end = True
        self.game.setLastDinoDown(endDinoImage, endDinoCenter)
        self.game.setIsEnding()

    def win(self):
        soundFx56.SoundPlayer.requestSound("win")

        snax = BonusDelegate.snax

        if self.profileName != "_user":

            ### case for tuts
            if self.curPuzzle[:3] == "tut":
                self.game.wonTutorialStage = True # tell game instance so level56 can access for returning next stage
                if self.curPuzzle == LAST_TUTORIAL:
                    dataStorage56.modProfile(self.profileName, "tutorial", True)
                puzzleData = "TUTORIAL"

            else:
                dataStorage56.modProfile(self.profileName, self.curPuzzle, True, snax) # modify file & and add snack to archive
                puzzleData  = dataStorage56.getPuzzleData(self.profileName, self.curPuzzle)

                if self.curPuzzle == "gateway":
                    self.game.wonLastStage = True # tell game instance so level56 can access for returning flag for ending scene
        else:
            puzzleData = "_user"
            dataStorage56.logUserMapsComplete(self.curPuzzle)

        if snax:
            for s in snax:
                s.unregister()

        line1, line2, line3 = self.generateMessage(True, puzzleData, snax)

        if self.curPuzzle[:3] == "tut" and self.profileName != "_user":
#            self.retryButton = EndMessageButton((-170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "next", SIZE_BTEXT, COL_BTEXT, "NEXT")
            self.retryButton = EndMessageButton(
                (0, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                ">",
                SIZE_BTEXT,
                COL_BTEXT,
                "NEXT"
            )
            line1 = ""; line2 = "Good work, lets move on"; line3 = ""
            if self.curPuzzle == LAST_TUTORIAL:
                line1 = "Alright, that's it for the training,"
                line2 = "you're ready for the real puzzles!"
        elif self.curPuzzle == "gateway" and self.profileName != "_user":
            self.exitButton = EndMessageButton(
                (0, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                "!",
                SIZE_BTEXT,
                COL_BTEXT,
                "EXIT"
            )
            line1 = "i'm so happy i could cry..."
            line2 = "excellent work, you got "
            line3 = "all dinos to a station!"
        else:
            self.retryButton = EndMessageButton(
                (-self.rect.width/4 + BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
                self.IMG("BTTN_0"),
                self.IMG("BTTN_1"),
                "Retry (any key)",
                SIZE_BTEXT,
                COL_BTEXT,
                "QR"
            )

            self.exitButton = EndMessageButton(
               (self.rect.width/4 - BTTN_MIDJUST, self.rect.height/2 - self.IMG("BTTN_0").get_height()/2 - BTTN_YBUF),
               self.IMG("BTTN_0"),
               self.IMG("BTTN_1"),
               "choose another puzzle",
               SIZE_BTEXT,
               COL_BTEXT,
               "EXIT"
            )

#            self.retryButton = EndMessageButton((-170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Quick Reset", SIZE_BTEXT, COL_BTEXT, "QR")
#            self.exitButton = EndMessageButton((170,30), self.IMG("BTTN_0"), self.IMG("BTTN_1"), "Leave Area", SIZE_BTEXT, COL_BTEXT, "EXIT")


        self.text1 = EndMessageText((0, MSG_TEXT_YREL1), line1, SIZE_MTEXT, COL_MTEXT)
        self.text2 = EndMessageText((0, MSG_TEXT_YREL2), line2, SIZE_MTEXT, COL_MTEXT)
        self.text3 = EndMessageText((0, MSG_TEXT_YREL3), line3, SIZE_MTEXT, COL_MTEXT)
        cursor = EndMessageCursor([self.IMG("CURSORSTD")], True)

        # dinostein ***
        self.currentDinostein = dinostein.Dinostein(self._fps)
        self.currentSteinFrame = dinostein.Frame(self._fps)
        self.currentDinostein.addFollower(self.currentSteinFrame)
        # *************

        if self.curPuzzle[:3] == "tut" and self.profileName != "_user":
            self.bind([self.retryButton, self.text1, self.text2, self.text3])
        elif self.curPuzzle == "gateway" and self.profileName != "_user":
            self.bind([self.exitButton, self.text1, self.text2, self.text3])
        else:
            self.bind([self.retryButton, self.exitButton, self.text1, self.text2, self.text3])

        self.endMessageGroup.add(self.currentSteinFrame)
        self.endMessageGroup.add(self.currentDinostein)
        self.endMessageGroup.add(cursor)

        self.setTween(MSG_TWEENSTART, MSG_TWEENEND, self.speed, MSG_TWEENMODE, self.dclval, self.dcllim)
        self.currentDinostein.setAndStartTween()
        self.startTween()
        self.end = True
        self.game.setIsEnding()

    def blitMinions(self):

        topleft = self.rect.topleft

        bbtopleft = self.retryButton.rect.topleft
        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            fbtopleft = self.exitButton.rect.topleft
        m1topleft = self.text1.rect.topleft
        m2topleft = self.text2.rect.topleft
        m3topleft = self.text3.rect.topleft

        bbBlitX = bbtopleft[0] - topleft[0]
        bbBlitY = bbtopleft[1] - topleft[1]
        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            fbBlitX = fbtopleft[0] - topleft[0]
            fbBlitY = fbtopleft[1] - topleft[1]
        m1BlitX = m1topleft[0] - topleft[0]
        m1BlitY = m1topleft[1] - topleft[1]
        m2BlitX = m2topleft[0] - topleft[0]
        m2BlitY = m2topleft[1] - topleft[1]
        m3BlitX = m3topleft[0] - topleft[0]
        m3BlitY = m3topleft[1] - topleft[1]

        self.spiralSnap = self.original.copy()
        self.spiralSnap.blit(self.retryButton.image, (bbBlitX, bbBlitY))
        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            self.spiralSnap.blit(self.exitButton.image, (fbBlitX, fbBlitY))
        self.spiralSnap.blit(self.text1.image, (m1BlitX, m1BlitY))
        self.spiralSnap.blit(self.text2.image, (m2BlitX, m2BlitY))
        self.spiralSnap.blit(self.text3.image, (m3BlitX, m3BlitY))

        self.hideRealMinions()

    def hideRealMinions(self):
        self.retryButton.rect.center = (2000,2000)
        if self.curPuzzle[:3] != "tut" or self.profileName == "_user":
            self.exitButton.rect.center = (2000,2000)
        self.text1.rect.center = (2000,2000)
        self.text2.rect.center = (2000,2000)
        self.text3.rect.center = (2000,2000)

    @staticmethod
    def setIsGoingOut(isGoingOut):
        if isGoingOut and not EndMessage.me.isGoingOut:
            soundFx56.SoundPlayer.requestSound("woosh_a")
            EndMessage.me.isGoingOutFrameCount = 0
            EndMessage.me.isGoingOut = isGoingOut
            EndMessage.me.blitMinions()

            # dinostein
            if EndMessage.me.currentDinostein:
                EndMessage.me.currentDinostein.kill()
                EndMessage.me.currentSteinFrame.closing = isGoingOut

    @staticmethod
    def quickReset():
        if EndMessage.me.currentDinostein:
            EndMessage.me.currentDinostein.kill()
        if EndMessage.me.currentSteinFrame:
            EndMessage.me.currentSteinFrame.kill()
        if EndMessageCursor.me:
            EndMessageCursor.me.kill()
        EndMessageCursor.wipe()
        EndMessage.me.reset()
        EndMessage.me.image = EndMessage.me.original
        EndMessage.me.rect = EndMessage.me.image.get_rect()
        EndMessage.me.rect.center = OFFSCREEN
        EndMessage.me.end = False
        EndMessage.me.isGoingOut = False
        EndMessage.me.isGoingOutFrameCount = 0
        EndMessage.me.terminate = False


class EndMessageText(tween.TweenFollower):

    def __init__(self, relPos, text, fontSize, fontColor):
        tween.TweenFollower.__init__(self, relPos)

        self.image = infoGraphic56.TextObject(text, fontSize, fontColor).image
        self.rect = self.image.get_rect()

    def updateEnding(self):
        pass

class EndMessageButton(tween.TweenFollower):
    """
        Button that belongs to EndMessage
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

    def update(self):
        tween.TweenFollower.update(self)
        self.checkCursorOver()

    def updateEnding(self):
        pass

    def makeButton(self, image, text, textSize, textColor):

        textSurf = infoGraphic56.TextObject(text, textSize, textColor).image
        xBlit = (image.get_width() - textSurf.get_width())/2
        yBlit = (image.get_height() - textSurf.get_height())/2
        image.blit(textSurf, (xBlit, yBlit))

        return image

    def checkCursorOver(self):
        """ if cursor over button set respective image and mouseOver """
        if pygame.sprite.collide_rect(self, EndMessageCursor.me):
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

class EndMessageCursor(pygame.sprite.Sprite):
    """ cursor used during end message """
    me = None

    def __init__(self, frames, withTrail=False):
        pygame.sprite.Sprite.__init__(self)

        if len(frames) > 1:
            self.hasFrames = True
            self.setFrames(frames)
            self.currentFrame = 0
        else:
            self.hasFrames = False
            self.image = frames[0]
            self.currentFrame = None

        self.rect = pygame.rect.Rect((0,0,1,1))
        self.rect.center = (-2000,2000)
        self.isActive = False
        self.firstCycle = True

        # create sparkle trail #
        ########################
        self.withTrail = withTrail
        self.trail = None
        if self.withTrail:
            self.image.set_alpha(0, pygame.RLEACCEL)
            self.trail = sparkleTrail.SparkleTrail(SPARK_SIZE, SPARK_COLOR, SPARK_BOUNDS, SPARK_FREQUENCY, SPARK_FADESPEED, self)
        ########################
        ########################

        EndMessageCursor.me = self

    def update(self):
        if self.isActive:
            if not self.firstCycle:
                self.rect.center = pygame.mouse.get_pos()
                if self.hasFrames:
                    self.stepFrames()
            else:
                self.firstCycle = False

    def updateEnding(self):
        pass

    def getTrailGroup(self):
        return self.trail.myGroup

    def stepFrames():
        self.image = self.frames[self.currentFrame]
        self.currentFrame += 1

        if self.currentFrame >= len(self.frames):
            self.currentFrame = 0

    def setFrames(self, frames):
        self.frames = frames

    @staticmethod
    def wipe():
        EndMessageCursor.me = None


# quick fix: copied from gfx56 because of circular import
def spiralOut(spr, directionAsInt, rotateStep, scaleStep, terminateAfter, frameCount, minRatio, ORIGINAL):
    """ update callback for a sprite to 'spiral out' of view in place using a set image
        returns false if spiral hasn't terminated

        - directionAsInt -> rotate direction: -1 for right, 1 for left
        - rotateStep -> degrees to rotate every frame
        - scaleStep -> degrees to scale every frame (takes positive or negative)
        - terminateAfter -> returns image as None after this many frames
        - frameCount -> expects an iterable count from calling environment: should inc by 1 ever call
        - ORIGINAL -> should be a constant of the pre-rotated image
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
    EndMessage.wipe()
    EndMessageCursor.wipe()
    BonusDelegate.wipe()


















