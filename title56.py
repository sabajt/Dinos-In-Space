
import pygame
import dinosInSpace
import gfx56
import screenWipe
import modeSwitch
import cCursor
import button
import sparkleTrail
import titleDino
import groupMods56
import spriteBasic
import infoGraphic56
import soundFx56

BLACK = (0,0,0)
GREY = (150,150,150)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED = (255,0,0)

WITH_SPARKLE    = True
SPARK_SIZE      = (6,6)
SPARK_COLOR     = WHITE
SPARK_BOUNDS    = (400,600)
SPARK_FREQUENCY = 15 #1)--15
SPARK_FADESPEED = 5 #1)--2
SPARK_CENTER    = (600,300)
SPARK_VELOCITY  = (0,-4)

DINO2_DELAY = 60

BUTTON_FRAMESIZE = (350, 40)
BUTTON_FRAMECOLOR = (GREY, WHITE)
BUTTON_FONTSIZE = 20
BUTTON_FONTCOLOR = BLACK
BUTTON_INDENT = 25
BUTTON_LEFT = BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT

TITLE_HEIGHT = 75
##TITLE_TEXT = "DINOS IN SPACE (PRE-RELEASE)"
TITLE_TEXT = "DINOS IN SPACE"
TITLE_FONTSIZE = 30
TITLE_COLOR = WHITE

BUTTON_POS = [
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 150/3), # new game
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 2*150/3), # load game
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 150 + 150/3), # user maps
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 150 + 2*150/3), # map edit
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 2*150 + 150/3), # was options -- now about
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 2*150 + 2*150/3), # was about -- now quit
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, TITLE_HEIGHT + 3*150 + TITLE_HEIGHT/2 + 2) # was quit -- don't use
]

B_OFFSET = 10
B_BOX_SIZE = (400 - 2*B_OFFSET, 150 - 2*B_OFFSET)
B_BOX_RIM = 2
B_BOX_COLOR = [
    GREEN,
    BLUE,
    YELLOW,
    RED
]
B_BOX_TL = [
    (0 + B_OFFSET, TITLE_HEIGHT + B_OFFSET),
    (0 + B_OFFSET, TITLE_HEIGHT + 150 + B_OFFSET),
    (0 + B_OFFSET, TITLE_HEIGHT + 2*150 + B_OFFSET),
    (0 + B_OFFSET, TITLE_HEIGHT + 3*150 + B_OFFSET)
]

class TitleScreen(object):
    """ running state """
    me = None
    _fps = 60 #### eventually needs to be repalced with setting fpsSwitch

    def __init__(self):
        TitleScreen.me = self

        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))

        # groups
        self.sparkleGroup = pygame.sprite.OrderedUpdates()
        self.dinoGroup = groupMods56.SmallRectGroup()
        self.boxGroup = pygame.sprite.OrderedUpdates()
        self.buttonGroup = pygame.sprite.OrderedUpdates()
        self.cursorGroup = pygame.sprite.RenderUpdates()

        # create sparkle trail #
        ########################
        self.withSparkle = WITH_SPARKLE
        self.sparkleEffect = None
        if self.withSparkle:
            self.sparkleEffect = sparkleTrail.SparkleTrail(SPARK_SIZE, SPARK_COLOR, SPARK_BOUNDS, SPARK_FREQUENCY, SPARK_FADESPEED, self, SPARK_CENTER, SPARK_VELOCITY)
        ########################
        ########################

    @staticmethod
    def wipe():
        TitleScreen.me = None

    def addSpriteToGroup(self, sprite, group):
        if group == "dino":
            self.dinoGroup.add(sprite)
        elif group == "box":
            self.boxGroup.add(sprite)
        elif group == "button":
            self.buttonGroup.add(sprite)
        elif group == "cursor":
            self.cursorGroup.add(sprite)

    def addSpriteListToGroup(self, spriteList, group):
        for s in spriteList:
            self.addSpriteToGroup(s, group)

    def getInput(self):
        dest = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                dest = self.checkButtonPressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dest = "_EXIT"
        return dest

    def checkButtonPressed(self):
        dest = None
        for b in self.buttonGroup:
            dest = b.checkPressed()
            if dest:
                break
        return dest

    def runMe(self, imageFrom):
##        modeSwitch.ModeSwitch.resetModes()

        clock = pygame.time.Clock()
        keepGoing = True
        firstCycle = True
        dest = None

        while keepGoing:

            clock.tick(TitleScreen._fps)
            dest = self.getInput()

            # clear - update - draws
            self.sparkleGroup.clear(self.screen, self.background)
            self.dinoGroup.clear(self.screen, self.background)
            self.boxGroup.clear(self.screen, self.background)
            self.buttonGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)

            self.sparkleGroup.update()
            self.dinoGroup.update()
            self.boxGroup.update()
            self.buttonGroup.update()
            self.cursorGroup.update()

            # sparkle update cycle #
            ########################
            if self.withSparkle:
                newUnit = self.sparkleEffect.update()
                if newUnit:
                    self.sparkleGroup.add(newUnit)
            ########################
            ########################

            self.sparkleGroup.draw(self.screen)
            self.dinoGroup.draw(self.screen)
            self.boxGroup.draw(self.screen)
            self.buttonGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)


            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            if imageFrom:
                screenWipe.wipe(TitleScreen._fps, imageFrom, self.screen.copy(), "right")
                imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            if dest:
                soundFx56.SoundPlayer.requestSound("woosh_b")
                keepGoing = False

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, self.background)

        self.buttonGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        snapshot = pygame.display.get_surface().copy()
        return dest, snapshot

def launch(imageFrom):

    # create objects

    titleScreen = TitleScreen()

    # basic rect: size, color, topLeft=(0,0), rimSize=None, alpha=None, opaqueCenter=False
    titleBox = spriteBasic.BasicRect((800, TITLE_HEIGHT), WHITE, (0,0), B_BOX_RIM, None, True)
    boundingBox = spriteBasic.BasicRect((400,600 - TITLE_HEIGHT), WHITE, (0,TITLE_HEIGHT), B_BOX_RIM)

    # text object: text, size, color, center=None
    titleText = infoGraphic56.TextObject(TITLE_TEXT, TITLE_FONTSIZE, TITLE_COLOR, (400, TITLE_HEIGHT/2))

    buttonBox1 = spriteBasic.BasicRect(B_BOX_SIZE, B_BOX_COLOR[0], B_BOX_TL[0], B_BOX_RIM)
    buttonBox2 = spriteBasic.BasicRect(B_BOX_SIZE, B_BOX_COLOR[1], B_BOX_TL[1], B_BOX_RIM)
    buttonBox3 = spriteBasic.BasicRect(B_BOX_SIZE, B_BOX_COLOR[2], B_BOX_TL[2], B_BOX_RIM)
    buttonBox4 = spriteBasic.BasicRect((B_BOX_SIZE[0], B_BOX_SIZE[1]/2 - 9), B_BOX_COLOR[3], B_BOX_TL[3], B_BOX_RIM)

    # button: dest, framesOrSize, center=None, fillColor=None, text=None, fontSize=None, fontColor=None
    bNewGame = button.Button("dNewGame", BUTTON_FRAMESIZE, BUTTON_POS[0], BUTTON_FRAMECOLOR, "NEW GAME", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bLoadGame = button.Button("dLoadGame", BUTTON_FRAMESIZE, BUTTON_POS[1], BUTTON_FRAMECOLOR, "LOAD GAME", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bUserMap = button.Button("dUserMap", BUTTON_FRAMESIZE, BUTTON_POS[2], BUTTON_FRAMECOLOR, "PLAY USER PUZZLES", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bMapEdit = button.Button("dMapEdit", BUTTON_FRAMESIZE, BUTTON_POS[3], BUTTON_FRAMECOLOR, "PUZZLE EDITOR", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bOptions = button.Button("dOptions", BUTTON_FRAMESIZE, BUTTON_POS[4], BUTTON_FRAMECOLOR, "OPTIONS", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bAbout = button.Button("dAbout", BUTTON_FRAMESIZE, BUTTON_POS[5], BUTTON_FRAMECOLOR, "ABOUT", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bQuit = button.Button("dQuit", BUTTON_FRAMESIZE, BUTTON_POS[6], BUTTON_FRAMECOLOR, "QUIT", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)

    dino1 = titleDino.TitleDino()
    dino2 = titleDino.TitleDino(DINO2_DELAY)
    cursor = cCursor.Cursor()

    # add to titleScreen

    titleScreen.addSpriteListToGroup([boundingBox, buttonBox1, buttonBox2, buttonBox3, buttonBox4, titleBox, titleText], "box") # took out buttonBox4
    titleScreen.addSpriteListToGroup([bNewGame, bLoadGame, bUserMap, bMapEdit, bOptions, bAbout, bQuit], "button") # took out bOptions
    titleScreen.addSpriteListToGroup([dino1, dino2], "dino")
    titleScreen.addSpriteToGroup(cursor, "cursor")

    dest, snapshot = titleScreen.runMe(imageFrom)

    return dest, snapshot, TitleScreen._fps

# button: dest, framesOrSize, center=None, fillColor=None, text=None, fontSize=None, fontColor=None