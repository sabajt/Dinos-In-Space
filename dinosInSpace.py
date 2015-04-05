""" dinosInSpace.py
"""

import pygame
import os

import block56
import interface56
import scroller56
import star56
import radar56
import static56
import soundFx56
import level56
import infoGraphic56
import controlMenu56
import title56
import areaSelect
import gfx56
import editor56
import dino56
import userMaps
import endMessage
import snack
import profileCreate
import profileSelect
import dataStorage56
import screenCap
import snackWorld
import autoMessage
import screenWipe
import modeSwitch
import fpsSwitch
import endingDino
import snackPacket
import simpleLabel
import winningScreen
import options
import about

FRUITCAKE = "UNIVERSALFRUITCAKE.ttf"
DOSFONT = "dos.ttf"

FONT_STD = FRUITCAKE
FONT_EDIT = DOSFONT

MIN_SPEED = 2
PROFILECODE = False

class Game(object):
    """ runs game, get's input from user and updates everything """
    groupList = []  # every sprite group in the game (todo: change to group obj instead of list?)
    clock = None # the fps controller
    minSpeed = MIN_SPEED
    screen = None

    def __init__(self, screen, isTutorial, isLastPuzzle=False):
        """ make screen and background / set minSpeed """

        self.CLASS          = "Game"
        self.screen         = screen
        self.pause          = False
        self.message        = False
        self.retry          = False
        self.hasStarted     = False
        self.isEnding       = False
        self.background     = pygame.Surface(self.screen.get_size());
        self.currentClock   = None
        self.isTutorial     = isTutorial # used in getInput to determine if player can skip messages
        self.isLastPuzzle   = isLastPuzzle # used to stop reset after winning last puzzle (end message)
        self.endDinoImage   = None
        self.endDinoCenter  = None

        ### tutorial vars
        self.wonTutorialStage = False
        self.leaveRequest = False
        #################
        ### ending game vars
        self.wonLastStage = False
        #################

        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))

        Game.screen         = self.screen
        self.setMode("puzzle") # left over from when there was also action mode -- clean up later

    @staticmethod
    def wipe():
        Game.groupList = []
        Game.clock = None
        Game.screen = None

    @staticmethod
    def getMinSpeed():
        """ called by all interactive objects """
        return Game.minSpeed

    def takeScreenshot(self):
        """ save current background as surface """
        return self.screen.copy()

    def getScreen(self):
        return self.screen

    def setRetry(self, isRetry):
        self.retry = isRetry

    def setPause(self, isPause):
        self.pause = isPause

    def setMessage(self, isMessage):
        if isMessage:
            self.message = True
        else:
            self.message = False

    #### clean up later -- not needed without action mode
    def setMode(self, mode):
        self.mode = mode

        if mode == "puzzle":
            self.lock = False
        elif mode == "action":
            self.lock = True
            interface56.Cursor.setLooking(True)
    ######################################################

    def getHasStarted(self):
        return self.hasStarted

    def getPause(self):
        return self.pause

    def getMessage(self):
        return self.message

    def start(self):
        if not self.hasStarted:
            soundFx56.GameSoundManager.registerSound("start")
##        else:
##            soundFx56.GameSoundManager.registerSound("noRecover")

        self.hasStarted = True

        if self.mode == "puzzle":
            self.lock = True
            interface56.Cursor.setLooking(True)
            static56.Switch.resetAll()
            static56.Spawn.activate()

#        elif self.mode == "action":
#            self.lock = False
#            interface56.Cursor.setLooking(False)

    def addGroup(self, g):
        """ called by all objects to be displayed """
        Game.groupList.append(g)

    def insertGroup(self, group, i):
        """ inserts group in groupList before given index """
        Game.groupList.insert(i, group)

    @staticmethod
    def getGroupListLen():
        """ returns last index of groupList"""
        return len(Game.groupList)

    def removeGroup(self, g):
        Game.groupList.remove(g)

    def quickReset(self):
        """ reset level, but keep tiles down (in game) """
        if not gfx56.VanishSeq.getIsRunning():
            if self.mode == "puzzle":

                soundFx56.GameSoundManager.registerSound("qRestart")
                self.hasStarted = False
                self.lock = False

                gfx56.VanishSeq.searchAndCreate(self)
                gfx56.ScreenFlash(self, [(125,97,186)], 2, 40)
                interface56.Cursor.setLooking(False)
                dino56.DinoDelux.quickReset()
                static56.Goal.quickReset()
                static56.Spawn.quickReset()
                ## static56.Switch.quickReset() old location *******
                radar56.Radar.quickReset()
                #level56.EndMessage.quickReset()
                endMessage.EndMessage.quickReset()
                endMessage.BonusDelegate.quickReset() # must be called before snack.quickre
                autoMessage.quickReset()
                snack.Snack.quickReset()
                static56.Switch.quickReset()
                snackPacket.quickReset()

    def getInput(self):
        """ get input from user and send commands """
        stopInput = False # one command per tick (except recover key up)
        mods = pygame.key.get_mods()

        # toggle recover tool

        if mods & pygame.KMOD_CTRL:
            interface56.Cursor.toggleRecover(True)
        else:
            interface56.Cursor.toggleRecover(False)

#        key = pygame.key.get_pressed()  #checking pressed keys
#        if key[pygame.K_x]:
#            interface56.Cursor.toggleRecover(True)
#        else:
#            interface56.Cursor.toggleRecover(False)

        # non locked actions
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.keepGoing = False
            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_r: # quick or hard reset
##                    if mods & pygame.KMOD_CTRL:
##                        self.setRetry(True)
##                        self.keepGoing = False
##                    else:
##                        self.quickReset()
                if event.key == pygame.K_r: # hard reset
                    if mods & pygame.KMOD_CTRL:
                        self.setRetry(True)
                        self.keepGoing = False
                elif event.key == pygame.K_SPACE: # launch or quick reset
                    interface56.Cursor.breakLink()
                    if block56.Warp.readyForLink:
                        block56.Warp.readyForLink.resetAll(False)
                    if self.hasStarted:
                        self.quickReset()
                    else:
                        self.start()
                elif event.key == pygame.K_t: # toggle infoGraphics
                    infoGraphic56.InfoGraphic.toggle()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: # pause / display control menu
                    controlMenu56.InPlayMenu.requestToggle(True)
                    interface56.Cursor.breakRecover()
                    self.setPause(True)
                elif event.key == pygame.K_m: # message / tip menu
                    setMsg = infoGraphic56.MessageStub.requestShowMsg()
                    if setMsg:
                        interface56.Cursor.breakRecover()
                        self.setMessage(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if not stopInput:
                        if self.lock:
                            pass
##                            soundFx56.GameSoundManager.registerSound("noRecover")
                        elif interface56.Cursor.canTestSwitch: # test switch on
                            interface56.Cursor.reqTestSwitch()
                            stopInput = True
                    if interface56.Cursor.overSpawn:
                        if self.hasStarted:
                            self.quickReset()
                        else:
                            self.start()

            if event.type == pygame.MOUSEBUTTONUP:
                static56.Switch.resetAll() # test switches off (all)


            # locked actions
            if not self.lock:

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_z: # cycle through channels (right)
                        if not stopInput:
                            interface56.ItemMenu.changeChannel("R")
                            stopInput = True
##                    elif event.key == pygame.K_s: # display recover cursor
##                        if not stopInput:
##                            interface56.Cursor.toggleRecover()
##                            stopInput = True
                    elif event.key == pygame.K_p: # debug
                        self.talk()
                    if interface56.Cursor.isLinking:
                        interface56.Cursor.breakLink()
                        if block56.Warp.readyForLink:
                            block56.Warp.readyForLink.resetAll(False)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    ######## 2 button + wheel mouse bindings ################
                    if event.button == 5: # mouse wheel down
                        if not stopInput:
                            interface56.ItemMenu.changeChannel("R")
                            stopInput = True
                    if event.button == 4: # mouse wheel up
                        if not stopInput:
                            interface56.ItemMenu.changeChannel("L")
                            stopInput = True

                    if pygame.mouse.get_pressed()[2]:
                        if not stopInput:
                            interface56.Cursor.toggleRecover(True)
                            if not stopInput:
                                for b in block56.Arrow.arrowGroup:
                                    if b.rect.collidepoint(pygame.mouse.get_pos()):
                                        block56.Block.canRecoverThis = b
                                        interface56.ItemMenu.reqRecObj()
                                        interface56.Cursor.toggleRecover(False)
                                        stopInput = True
                                        break
                            if not stopInput:
                                for b in block56.Warp.warpGroup:
                                    if b.rect.collidepoint(pygame.mouse.get_pos()):
                                        ### break link first
                                        if interface56.Cursor.isLinking:
                                            interface56.Cursor.breakLink()
                                            if block56.Warp.readyForLink:
                                                block56.Warp.readyForLink.resetAll(False)
                                        ####################
                                        block56.Block.canRecoverThis = b
                                        interface56.ItemMenu.reqRecObj()
                                        interface56.Cursor.toggleRecover(False)
                                        stopInput = True
                                        break
                    #########################################################

                    if pygame.mouse.get_pressed()[0]:
                        if not stopInput:
                            if interface56.Cursor.isRecover and not stopInput: # recover blocks
                                interface56.ItemMenu.reqRecObj()
                                stopInput = True
                            elif interface56.Cursor.canRotate and not stopInput: # rotate placed arrows (only right)
                                block56.Arrow.reqRotate()
                                stopInput = True
                            elif interface56.Cursor.canLink and not stopInput: # initiate warp link -- 2nd stopInput check right click bugfix
                                block56.Warp.reqInitLink()
                                stopInput = True
                            elif interface56.Cursor.isLinking and not stopInput: # make warp link
                                block56.Warp.reqMakeLink()
                                stopInput = True
                            else: # place block
                                interface56.ItemMenu.reqAddObj()
                                stopInput = True


    def update(self):
        pass

    def getCurrentClock(self):
        return self.currentClock

#    def activateBonusModes(self, modes):
#        """ activate list of modes """
#        assert(type(modes) == list)
#
#        for m in modes:
#            if m == "HATS":
#                print "hats mode enabled"
#            elif m == "NYAN":
#                print "nyan cat mode enabled"
#            elif m == "XTRA":
#                print "xtra puzzles enabled"

    def runGame(self, _fps, isUserMapWithName=None, imageFrom=None, bonusModes=None):
        """ the game (puzzle) loop - runs every tick """

#        # modes
#        if bonusModes:
#            self.activateBonusModes(bonusModes)

        screenCamera = None
        if isUserMapWithName:
            screenCamera = screenCap.ScreenCamera()

        Game.clock = pygame.time.Clock()
        self.currentClock = Game.clock
        self.keepGoing = True

        # main puzzle loop
        while self.keepGoing:
            Game.clock.tick(_fps)
            self.pause = False
            self.getInput()

            dirtyRects = []

            for g in Game.groupList:
                g.clear(self.screen, self.background)
            for g in Game.groupList:
                g.update()
            for g in Game.groupList:
                g.draw(self.screen)

            # check for state breaks
            if not imageFrom:
                if self.pause:
                    self.pauseGame(_fps)
                    self.currentClock = Game.clock
                elif self.message:
                    self.displayMessage(_fps)
                    self.currentClock = Game.clock
                elif self.isEnding:
                    ## make call to hide cursor?
                    interface56.Cursor.hideDuringMessages()
                    for g in Game.groupList:
                        g.clear(self.screen, self.background)
                    for g in Game.groupList:
                        g.update()
                    for g in Game.groupList:
                        g.draw(self.screen)
                    ##------

                    self.endPuzzle(_fps)
                    interface56.Cursor.showAfterMessages()
                    self.currentClock = Game.clock

            radar56.drawBorder(self)
##            radar56.Radar.reqDrawRadarScreen()

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "down")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            if isUserMapWithName:
                dataStorage56.logUserMapsRecord(isUserMapWithName)
                screenCamera.takePicture(self.screen, isUserMapWithName, "PLAY", 0.5)
                isUserMapWithName = None

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
##        self.cursorGroup.clear(self.screen, self.background)
##
##        self.bkgGroup1.draw(self.screen)
##        self.portalGroup.draw(self.screen)
##        self.sectorGroup.draw(self.screen)
##        self.infoGroup.draw(self.screen)
##
##        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        return snapshot

    def eraseGameCursorWithBackground(self, bkg):
        """ hides the game cursor by modifying display when messages appears with given background
            should be called after new background is made at beginning of run state
        """
        for g in Game.groupList:
            for spr in g:
                if spr.__class__ == interface56.Cursor:
                    g.clear(self.screen, bkg)
##                    print "cleared a group"
                    break


    def displayMessage(self, _fps):
        clock = pygame.time.Clock()
        self.currentClock = clock

        # create new background from screen and isolate message items for cycle
        background = self.takeScreenshot()
        msgGroup = pygame.sprite.OrderedUpdates()

        for g in Game.groupList:
            for s in g:
                methods = dir(s)
                if "updateMessage" in methods:
                    if hasattr(s, "isActive"):
                        s.isActive = True
                    msgGroup.add(s)

        while self.message:
            clock.tick(_fps)
            interface56.hideCursorItems()

            mods = pygame.key.get_mods()
            dest = None

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dest = autoMessage.StdMessage.checkButtonPressed()

                if event.type == pygame.KEYDOWN:
                    if not self.isTutorial:
                        autoMessage.StdMessage.setIsGoingOut(True)

            msgGroup.clear(self.screen, background)
            msgGroup.update()
            msgGroup.draw(self.screen)


#            # new update cycle ***
#            for g in Game.groupList:
#                g.clear(self.screen, self.background)
#            for g in Game.groupList:
#                for s in g:
#                    methods = dir(s)
#                    if "updateMessage" in methods:
#                        s.updateMessage()
#            for g in Game.groupList:
#                g.draw(self.screen)
#




            radar56.drawBorder(self)
            pygame.display.update()

            if autoMessage.StdMessage.me.terminate:
                dest = "SPIRALOUT"

            if dest:
                if dest == "BACK":
                    autoMessage.StdMessage.pageBack()
                elif dest == "FORWARD":
                    if autoMessage.StdMessage.pageForward() == "LAST": # internally "resets all" (called manually in key event loop)
                        autoMessage.StdMessage.setIsGoingOut(True)
                elif dest == "SPIRALOUT":
                    autoMessage.StdMessage.me.resetAll()
                    self.setMessage(False)

        for s in msgGroup:
            if hasattr(s, "isActive"):
                s.isActive = False
            if hasattr(s, "firstCycle"):
                s.firstCycle = True


    def pauseGame(self, _fps):
        clock = pygame.time.Clock()
        self.currentClock = clock

        # create new background from screen and isolate pause items for cycle
        background = self.takeScreenshot()
        pauseGroup = pygame.sprite.OrderedUpdates()
        pauseClassList = [
            controlMenu56.InPlayMenu,
            controlMenu56.MenuDependant,
            controlMenu56.BasicButton,
            controlMenu56.BottomButton,
            controlMenu56.ControlMenuCursor,
            controlMenu56.MenuGraphic,
            controlMenu56.PauseMenuTextBlock,
            simpleLabel.Label
        ]
        puzzleLabel = None
        for g in Game.groupList:
            for s in g:
                if s.__class__ in pauseClassList:
                    pauseGroup.add(s)
                    if s.__class__ == simpleLabel.Label:
                        puzzleLabel = s
                        s.visible = True

        while self.pause:
            clock.tick(_fps)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        controlMenu56.InPlayMenu.requestToggle(False)
                        self.setPause(False)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    controlMenu56.BasicButton.requestPress()

            # clear / update / draw pause items
            pauseGroup.clear(self.screen, background)
            pauseGroup.update()
            pauseGroup.draw(self.screen)

##            for g in Game.groupList:
##                g.clear(self.screen, self.background)
##            for g in Game.groupList:
##                for s in g:
##                    methods = dir(s)
##                    if "updatePause" in methods:
##                        s.updatePause() # update classes with updatePause() only
##            for g in Game.groupList:
##                g.draw(self.screen)

            radar56.drawBorder(self)
            pygame.display.update()

        if puzzleLabel:
            puzzleLabel.visible = False

    def setIsEnding(self):
        self.isEnding = True

    def setLastDinoDown(self, endDinoImage, endDinoCenter):
        self.endDinoImage = endDinoImage
        self.endDinoCenter = endDinoCenter

    def endPuzzle(self, _fps):
        clock = pygame.time.Clock()
        self.currentClock = clock

        # create new background from screen and isolate message items for cycle
        background = self.takeScreenshot()
#        self.eraseGameCursorWithBackground(background) #############################################################
        endGroup = pygame.sprite.OrderedUpdates()

        # create trail if winning
        cursorTrail = None
        if endMessage.EndMessageCursor.me.withTrail:
            cursorTrail = endMessage.EndMessageCursor.me.trail

        for g in Game.groupList:
            for s in g:
                methods = dir(s)
                if "updateEnding" in methods:
                    if hasattr(s, "isActive"):
                        s.isActive = True
                    endGroup.add(s)

        if self.endDinoImage:
            endDinoSprite = endingDino.EndingDino(self.endDinoImage, self.endDinoCenter)
            endGroup.add(endDinoSprite)

        while self.isEnding:
            clock.tick(_fps)
            dest = None

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dest = endMessage.EndMessage.checkButtonPressed()

                if event.type == pygame.KEYDOWN:
                    if not self.isTutorial and not self.isLastPuzzle:
                        endMessage.EndMessage.me.setIsGoingOut(True)

##            for event in pygame.event.get():
##                if event.type == pygame.KEYDOWN:
##                    if event.key == pygame.K_r:
##                        if mods & pygame.KMOD_CTRL:
##                            dest = "HR"
##                        else:
##                            dest = "QR"
##                if event.type == pygame.MOUSEBUTTONDOWN:
##                    if pygame.mouse.get_pressed()[0]:
##                        dest = endMessage.EndMessage.checkButtonPressed()

            endGroup.clear(self.screen, background)
            endGroup.update()

            # sparkle update cycle #
            ########################
            if cursorTrail:
                newUnit = cursorTrail.update()
                if newUnit:
                    endGroup.add(newUnit)
            ########################
            ########################

            endGroup.draw(self.screen)

            radar56.drawBorder(self)
            pygame.display.update()

            if endMessage.EndMessage.me.terminate:
                dest = "SPIRALOUT"

            if dest:
                if dest == "QR":
                    endMessage.EndMessage.me.setIsGoingOut(True)
                elif dest == "EXIT":
                    soundFx56.SoundPlayer.requestSound("woosh_b")
                    self.keepGoing = False
                    self.isEnding = False
                elif dest == "NEXT": # tutorial only
                    soundFx56.SoundPlayer.requestSound("woosh_b")
                    self.keepGoing = False
                    self.isEnding = False
                elif dest == "SPIRALOUT":
                    self.quickReset()
                    self.isEnding = False
        for s in endGroup:
            if hasattr(s, "isActive"):
                s.isActive = False
            if hasattr(s, "firstCycle"):
                s.firstCycle = True

        self.setLastDinoDown(None, None)

    def talk(self):
        """ a debugging method, press "p" to print stuff """
        print "message"

def loadImage(fileName, scaleTo=None, getAt=None, alpha=None, cwd=None):
    """ returns image surface - give str '2X' or '4X' or float 0 to 1+ """
    if not cwd:
        filePath = os.path.join("art", fileName)
    else:
        filePath = fileName

    try:
        image = pygame.image.load(filePath)
    except:
        print "error: failed to load image file " + fileName

    image = image.convert()

    if scaleTo:
        if scaleTo == "2X":
            image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
        elif scaleTo == "4X":
            image = pygame.transform.scale(image, (image.get_width()*4,  image.get_height()*4))
        else:
            image = pygame.transform.scale(image, scaleTo)

    if getAt:
        col = image.get_at(getAt)
        image.set_colorkey(col, pygame.RLEACCEL)

    if alpha:
        image.set_alpha(alpha, pygame.RLEACCEL)

    return image

def configMixer():
    """ init mixer with these settings """
    if pygame.mixer:
##        pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=2048)
        pygame.mixer.pre_init(22050, -8, 1, 2048)
    else:
        print "problem loading pygame.mixer"

class FontBank(object):
    """ preloads fonts at all sizes for global access """
    STDFONTS = None
    EDITFONTS = None

    def __init__(self):
        if not FontBank.STDFONTS:
            FontBank.STDFONTS = {
                "FONT10" : pygame.font.Font(FONT_STD, 10),
                "FONT11" : pygame.font.Font(FONT_STD, 11),
                "FONT12" : pygame.font.Font(FONT_STD, 12),
                "FONT13" : pygame.font.Font(FONT_STD, 13),
                "FONT14" : pygame.font.Font(FONT_STD, 14),
                "FONT15" : pygame.font.Font(FONT_STD, 15),
                "FONT16" : pygame.font.Font(FONT_STD, 16),
                "FONT17" : pygame.font.Font(FONT_STD, 17),
                "FONT18" : pygame.font.Font(FONT_STD, 18),
                "FONT19" : pygame.font.Font(FONT_STD, 19),
                "FONT20" : pygame.font.Font(FONT_STD, 20),
                "FONT21" : pygame.font.Font(FONT_STD, 21),
                "FONT22" : pygame.font.Font(FONT_STD, 22),
                "FONT23" : pygame.font.Font(FONT_STD, 23),
                "FONT24" : pygame.font.Font(FONT_STD, 24),
                "FONT25" : pygame.font.Font(FONT_STD, 25),
                "FONT26" : pygame.font.Font(FONT_STD, 26),
                "FONT27" : pygame.font.Font(FONT_STD, 27),
                "FONT28" : pygame.font.Font(FONT_STD, 28),
                "FONT29" : pygame.font.Font(FONT_STD, 29),
                "FONT30" : pygame.font.Font(FONT_STD, 30),
                "FONT50" : pygame.font.Font(FONT_STD, 50),
                "FONT70" : pygame.font.Font(FONT_STD, 70)
            }

            FontBank.EDITFONTS = {
                "FONT10" : pygame.font.Font(FONT_EDIT, 10),
                "FONT11" : pygame.font.Font(FONT_EDIT, 11),
                "FONT12" : pygame.font.Font(FONT_EDIT, 12),
                "FONT13" : pygame.font.Font(FONT_EDIT, 13),
                "FONT14" : pygame.font.Font(FONT_EDIT, 14),
                "FONT15" : pygame.font.Font(FONT_EDIT, 15),
                "FONT16" : pygame.font.Font(FONT_EDIT, 16),
                "FONT17" : pygame.font.Font(FONT_EDIT, 17),
                "FONT18" : pygame.font.Font(FONT_EDIT, 18),
                "FONT19" : pygame.font.Font(FONT_EDIT, 19),
                "FONT20" : pygame.font.Font(FONT_EDIT, 20),
                "FONT21" : pygame.font.Font(FONT_EDIT, 21),
                "FONT22" : pygame.font.Font(FONT_EDIT, 22),
                "FONT23" : pygame.font.Font(FONT_EDIT, 23),
                "FONT24" : pygame.font.Font(FONT_EDIT, 24),
                "FONT25" : pygame.font.Font(FONT_EDIT, 25),
                "FONT26" : pygame.font.Font(FONT_EDIT, 26),
                "FONT27" : pygame.font.Font(FONT_EDIT, 27),
                "FONT28" : pygame.font.Font(FONT_EDIT, 28),
                "FONT29" : pygame.font.Font(FONT_EDIT, 29),
                "FONT30" : pygame.font.Font(FONT_EDIT, 30),
                "FONT50" : pygame.font.Font(FONT_EDIT, 50),
                "FONT70" : pygame.font.Font(FONT_EDIT, 70)
            }

    @staticmethod
    def getFont(size, editorFont=False):
        if FontBank.STDFONTS and FontBank.EDITFONTS:
            key = "FONT" + str(size)
            if not editorFont:
                return FontBank.STDFONTS[key]
            else:
                return FontBank.EDITFONTS[key]
        print "ERROR: font bank not initiated"

##pygame.init()
##FontBank()
configMixer()   # custom sound settings for this game
pygame.init()
FontBank()
# start here
def main():
    """ control game states """


#    pygame.init()
    R_640 = (640, 480)
    R_800 = (800, 600)
    FS = pygame.FULLSCREEN

    screen = pygame.display.set_mode(R_800, FS) # resolution / fullscreen tag <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FULLSCREEN
    soundFx56.SoundPlayer()
    modeSwitch.ModeSwitch() # keeps track of bonus modes
    fpsSwitch.FPSSwitch() # controls frames per second

    pygame.mouse.set_visible(False)


#    FontBank()

    goTo = None
    _fps = None # set fps in title screen

    snapshot = None # holds "from" transition image (copy of screen surface)
    swipeDirection = None # holds the 'up' 'down' 'left' right' for screen transition directions for transition variable states
    wonLastStage = False

    while goTo != "dQuit":

        # show credits if just completed last stage
        if wonLastStage:
            winningScreen.launch()
            wonLastStage = False
            snapshot = None

        # titleScreen = title56.TitleScreen()
        goTo, snapshot, _fps = title56.launch(snapshot)  # title state


        # --------------------------------- music -------------------
#        if pygame.mixer.music:
#            musicFile = os.path.join("sound", "beatz1.ogg")
#            try:
#                beatz = pygame.mixer.music.load(musicFile)
#            except:
#                print "couldn't load beatz1!"
#            pygame.mixer.music.play(-1)
#        else:
#            print "pygame.mixer.music failed to init"
        # -----------------------------------------------------------


        if goTo == "dQuit":
            pass
        elif goTo == "dOptions":
            snapshot = options.launch(snapshot) # only one destination, back
        elif goTo == "dAbout":
            snapshot = about.launch(snapshot) # only one destination, back
        # new or load game
        elif goTo == "dNewGame" or goTo == "dLoadGame":
            isUserMap = False
            mapName = None
            profileName = None

            if goTo == "dNewGame":
                newGame = True
                profileName, snapshot = profileCreate.launchProfileCreate(_fps, snapshot)
            else:
                newGame = False
                profileName, snapshot = profileSelect.launchProfileSelect(_fps, snapshot)

            swipeDirection = "left" # screen transitions

            if profileName != "_EXIT":
                while mapName != "_EXIT" and wonLastStage == False:

                    mapName, puzzleName, snapshot = areaSelect.launch(profileName, newGame, _fps, snapshot, swipeDirection)
                    newGame = False
                    retry = True
                    wonLastStage = False

                    if mapName != "_EXIT" and mapName != "_SNAX" and mapName[:5] != "1_TUT":
                        while retry:
                            retry, snapshot, wonLastStage = level56.buildLevel(screen, mapName, isUserMap, profileName, puzzleName, _fps, snapshot)

                    elif mapName[:5] == "1_TUT":
                        leaveRequest = False
                        while (mapName[:5] == "1_TUT") and not leaveRequest:
                            snapshot, mapName, puzzleName, leaveRequest = level56.buildLevel(screen, mapName, isUserMap, profileName, puzzleName, _fps, snapshot, )

                    elif mapName == "_SNAX":
                        snapshot = snackWorld.launch(profileName, _fps, snapshot)

                    swipeDirection = "up" # screen transitions

#                snackWorld.BonusSwitch.clearStates() # reset bonus switch states to off

        # select user map
        elif goTo == "dUserMap":
            isUserMap = True
            mapName = None

            swipeDirection = "left" # screen transitions

            while mapName != "_EXIT":
                mapName, snapshot = userMaps.launchUserMaps(_fps, snapshot, swipeDirection)
                retry = True
                if mapName != "_EXIT":
                    while retry:
                        retry, snapshot, wonLastStage = level56.buildLevel(screen, mapName, isUserMap, None, None, _fps, snapshot)
                        wonLastStage = False # should always be, but just to make sure...

                swipeDirection = "up" # screen transitions

        # map editor
        elif goTo == "dMapEdit":

            swipeDirection = "left" # screen transitions

            while goTo != "_EXIT":
                goTo, snapshot = editor56.launchSetup(_fps, snapshot, swipeDirection)

                swipeDirection = "up" # screen transitions

    pygame.mouse.set_visible(True)
    pygame.quit()

if __name__ == "__main__":
    if PROFILECODE:
        cProfile.run('main()')  # start program from here
    else:
        main()

## from Game displayMessage
##                    if event.key == pygame.K_r:
##                        if mods & pygame.KMOD_CTRL:
##                            dest = "HR"
##                        else:
##                            dest = "QR"
##
##                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
##                        autoMessage.StdMessage.resetAll()
##                        self.setMessage(False)
##                        autoMessage.StdMessage.setIsGoingOut(True)

##                    elif event.key == pygame.K_LEFT:
##                        if not autoMessage.StdMessage.me.isGoingOut:
##                            dest = "BACK"
##
##                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_RETURN:
##                        if not isGoingOut:
##                            dest = "FORWARD"

