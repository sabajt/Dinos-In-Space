""" snackWorld.py

    the screen that keeps track of snax collected and bonus things unlocked
"""
import pygame
import dinosInSpace
import gfx56
import dataStorage56
import screenWipe
import button
import infoGraphic56
import modeSwitch
import spriteBasic
import soundFx56

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREY = (100,100,100)
SUB_SHADOW = (27,47,50)
SUB_STANDARD = (48,86,91)
SUB_LIGHT = (79,140,149)

SNAX_ARCHIVE = "_snaxArchive"
COL_BACKGROUND = SUB_SHADOW
PLATE_TXTSIZE = 30
BONUS_DESTS = ["HATS", "NYAN", "XTRA"]

SNAX_TEXT_BKG_HEIGHT = 40

GRID_SIZE = (6,4)
GRID_STEP = 75
GRID_COLOR = GREY

PILL_COLOR = SUB_SHADOW
PILL_EDGE_WIDTH = 0 # 0 filled

TNAME_TEXT = "?   ?   ?" # default text
TNAME_SIZE = 20
TNAME_COLOR = BLACK
TNAME_CENTER = (400,30)

SNAX_FEATURE_BKG_COLOR = BLACK
SNAX_TEXT_BKG_COLOR = WHITE

GRID_OFFSET_Y = 50
##TROPHY_IMAGE4X_DEFAULT_TEXTSIZE = 70
##TROPHY_IMAGE4X_DEFAULT_TEXTCOLOR = WHITE
TROPHYCASE_SIZE = (160,160)
TROPHYCASE_COLOR = SUB_SHADOW
TROPHYCASE_WIDTH = None

TROPHY_FEATURES_XOFFSET = 40
TROPHY_FEATURES_YOFFSET = 0

TROPHY_GRIDPOINT = {
# keys are identical to image keys

    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| add snax ||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    "barbequarks" : (0,0),
    "broccolibanana" : (1,0),
    "candydough" : (2,0),
    "cheese zees" : (3,0),
    "fizzy beerwafers" : (4,0),
    "funtarts" : (5,0),
    "grade a milk" : (0,1),
    "hexberries" : (1,1),
    "joybacon" : (2,1),
    "lazercut fries" : (3,1),
    "lucky coffee" : (4,1),
    "marshmelons" : (5,1),
    "monster biscuits" : (0,2),
    "munchzilla" : (1,2),
    "nanocorn" : (2,2),
    "penutbutter cubes" : (3,2),
    "picklesicle" : (4,2),
    "pizzaballoon" : (5,2),
    "shrimp nuggets" : (0,3),
    "sugar pufz" : (1,3),
    "sushi yumyum cone" : (2,3),
    "xtremophile gummies" : (3,3),
    "yumzingers" : (4,3),
    "chocobeanz" : (5,3)
}

class ImgLib(object):
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:
            ImgLib.imgDict = {

                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
                # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| add snax ||||||||||||||||||||||||||||||||||||||||
                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

##                "TESTSNACK" : dinosInSpace.loadImage("blueSquare.png", (50,50)),
##                "BLUESNAX" : dinosInSpace.loadImage("blueSquare.png", (50,50)),
##                "GREENSNAX" : dinosInSpace.loadImage("greenSquare.png", (50,50)),
##                "PINKSNAX" : dinosInSpace.loadImage("pinkSquare.png", (50,50)),
##                "REDSNAX" : dinosInSpace.loadImage("redSquare.png", (50,50)),
##                "PURPLESNAX" : dinosInSpace.loadImage("purpleSquare.png", (50,50)),


                "CURSOR" : dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "SWITCH_OFF0" : dinosInSpace.loadImage("bonusSwitchOff0.png", "2X", (0,0)),
                "SWITCH_OFF1" : dinosInSpace.loadImage("bonusSwitchOff1.png", "2X", (0,0)),
                "SWITCH_ON0" : dinosInSpace.loadImage("bonusSwitchOn0.png", "2X", (0,0)),
                "SWITCH_ON1" : dinosInSpace.loadImage("bonusSwitchOn1.png", "2X", (0,0)),
                "MODE_LOCKED" : dinosInSpace.loadImage("modeLocked.png", "2X", (0,0)),
#                "MODE_HATS"
                "barbequarks" : dinosInSpace.loadImage("s_barbequarks.png", "2X", (0,0)),
                "broccolibanana" : dinosInSpace.loadImage("s_broccolibanana.png", "2X", (0,0)),
                "candydough" : dinosInSpace.loadImage("s_candydough.png", "2X", (0,0)),
                "cheese zees" : dinosInSpace.loadImage("s_cheese_zees.png", "2X", (0,0)),
                "chocobeanz" : dinosInSpace.loadImage("s_chocobeanz.png", "2X", (0,0)),
                "fizzy beerwafers" : dinosInSpace.loadImage("s_fizzy_beerwafers.png", "2X", (0,0)),
                "funtarts" : dinosInSpace.loadImage("s_funtarts.png", "2X", (0,0)),
                "grade a milk" : dinosInSpace.loadImage("s_grade_a_milk.png", "2X", (0,0)),
                "hexberries" : dinosInSpace.loadImage("s_hexberries.png", "2X", (0,0)),
                "joybacon" : dinosInSpace.loadImage("s_joybacon.png", "2X", (0,0)),
                "lazercut fries" : dinosInSpace.loadImage("s_lazercut_fries.png", "2X", (0,0)),
                "lucky coffee" : dinosInSpace.loadImage("s_lucky_coffee.png", "2X", (0,0)),
                "marshmelons" : dinosInSpace.loadImage("s_marshmelons.png", "2X", (0,0)),
                "monster biscuits" : dinosInSpace.loadImage("s_monster_biscuits.png", "2X", (0,0)),
                "munchzilla" : dinosInSpace.loadImage("s_munchzilla.png", "2X", (0,0)),
                "nanocorn" : dinosInSpace.loadImage("s_nanocorn.png", "2X", (0,0)),
                "penutbutter cubes" : dinosInSpace.loadImage("s_penutbutter_cubes.png", "2X", (0,0)),
                "picklesicle" : dinosInSpace.loadImage("s_picklesicle.png", "2X", (0,0)),
                "pizzaballoon" : dinosInSpace.loadImage("s_pizzaballoon.png", "2X", (0,0)),
                "shrimp nuggets" : dinosInSpace.loadImage("s_shrimp_nuggets.png", "2X", (0,0)),
                "sugar pufz" : dinosInSpace.loadImage("s_sugar_pufz.png", "2X", (0,0)),
                "sushi yumyum cone" : dinosInSpace.loadImage("s_sushi_yumyum_cone.png", "2X", (0,0)),
                "xtremophile gummies" : dinosInSpace.loadImage("s_xtremophile_gummies.png", "2X", (0,0)),
                "yumzingers" : dinosInSpace.loadImage("s_yumzingers.png", "2X", (0,0)),

#                "S_PIZZA" : dinosInSpace.loadImage("s_pizza.png", "2X", (0,0)),
#                "S_SALAMI" : dinosInSpace.loadImage("s_salami.png", "2X", (0,0)),
#                "S_SHRIMP" : dinosInSpace.loadImage("s_shrimp.png", "2X", (0,0)),
#                "S_BROCCOLI" : dinosInSpace.loadImage("s_broc.png", "2X", (0,0)),
#                "S_MAC_N'_CHEESE" : dinosInSpace.loadImage("s_mac.png", "2X", (0,0)),
#                "S_CORN_CRUNCHIES" : dinosInSpace.loadImage("s_corn_crunchies.png", "2X", (0,0)),
#                "S_SUGAR_PUFZ" : dinosInSpace.loadImage("s_sugar_pufz.png", "2X", (0,0)),
#                "S_PB_CUBES" : dinosInSpace.loadImage("s_pb_cubes.png", "2X", (0,0)),
#                "S_BBQ_TWISTS" : dinosInSpace.loadImage("s_bbq_twists.png", "2X", (0,0)),

                "barbequarks_4x" : dinosInSpace.loadImage("s_barbequarks.png", "4X", (0,0)),
                "broccolibanana_4x" : dinosInSpace.loadImage("s_broccolibanana.png", "4X", (0,0)),
                "candydough_4x" : dinosInSpace.loadImage("s_candydough.png", "4X", (0,0)),
                "cheese zees_4x" : dinosInSpace.loadImage("s_cheese_zees.png", "4X", (0,0)),
                "chocobeanz_4x" : dinosInSpace.loadImage("s_chocobeanz.png", "4X", (0,0)),
                "fizzy beerwafers_4x" : dinosInSpace.loadImage("s_fizzy_beerwafers.png", "4X", (0,0)),
                "funtarts_4x" : dinosInSpace.loadImage("s_funtarts.png", "4X", (0,0)),
                "grade a milk_4x" : dinosInSpace.loadImage("s_grade_a_milk.png", "4X", (0,0)),
                "hexberries_4x" : dinosInSpace.loadImage("s_hexberries.png", "4X", (0,0)),
                "joybacon_4x" : dinosInSpace.loadImage("s_joybacon.png", "4X", (0,0)),
                "lazercut fries_4x" : dinosInSpace.loadImage("s_lazercut_fries.png", "4X", (0,0)),
                "lucky coffee_4x" : dinosInSpace.loadImage("s_lucky_coffee.png", "4X", (0,0)),
                "marshmelons_4x" : dinosInSpace.loadImage("s_marshmelons.png", "4X", (0,0)),
                "monster biscuits_4x" : dinosInSpace.loadImage("s_monster_biscuits.png", "4X", (0,0)),
                "munchzilla_4x" : dinosInSpace.loadImage("s_munchzilla.png", "4X", (0,0)),
                "nanocorn_4x" : dinosInSpace.loadImage("s_nanocorn.png", "4X", (0,0)),
                "penutbutter cubes_4x" : dinosInSpace.loadImage("s_penutbutter_cubes.png", "4X", (0,0)),
                "picklesicle_4x" : dinosInSpace.loadImage("s_picklesicle.png", "4X", (0,0)),
                "pizzaballoon_4x" : dinosInSpace.loadImage("s_pizzaballoon.png", "4X", (0,0)),
                "shrimp nuggets_4x" : dinosInSpace.loadImage("s_shrimp_nuggets.png", "4X", (0,0)),
                "sugar pufz_4x" : dinosInSpace.loadImage("s_sugar_pufz.png", "4X", (0,0)),
                "sushi yumyum cone_4x" : dinosInSpace.loadImage("s_sushi_yumyum_cone.png", "4X", (0,0)),
                "xtremophile gummies_4x" : dinosInSpace.loadImage("s_xtremophile_gummies.png", "4X", (0,0)),
                "yumzingers_4x" : dinosInSpace.loadImage("s_yumzingers.png", "4X", (0,0)),

#                "S_PIZZA_4X" : dinosInSpace.loadImage("s_pizza.png", "4X", (0,0)),
#                "S_SALAMI_4X" : dinosInSpace.loadImage("s_salami.png", "4X", (0,0)),
#                "S_SHRIMP_4X" : dinosInSpace.loadImage("s_shrimp.png", "4X", (0,0)),
#                "S_BROCCOLI_4X" : dinosInSpace.loadImage("s_broc.png", "4X", (0,0)),
#                "S_MAC_N'_CHEESE_4X" : dinosInSpace.loadImage("s_mac.png", "4X", (0,0)),
#                "S_CORN_CRUNCHIES_4X" : dinosInSpace.loadImage("s_corn_crunchies.png", "4X", (0,0)),
#                "S_SUGAR_PUFZ_4X" : dinosInSpace.loadImage("s_sugar_pufz.png", "4X", (0,0)),
#                "S_PB_CUBES_4X" : dinosInSpace.loadImage("s_pb_cubes.png", "4X", (0,0)),
#                "S_BBQ_TWISTS_4X" : dinosInSpace.loadImage("s_bbq_twists.png", "4X", (0,0)),

##                "TROPHY_IMAGE4X_DEFAULT" : infoGraphic56.TextObject("?", TROPHY_IMAGE4X_DEFAULT_TEXTSIZE, TROPHY_IMAGE4X_DEFAULT_TEXTCOLOR).image,
                "TROPHY_IMAGE4X_DEFAULT" : dinosInSpace.loadImage("snackTrophy.png", "2X", (0,0)),
##                "TROPHY_IMAGE4X_DEFAULT" : spriteBasic.BasicRect(TROPHYCASE_SIZE, TROPHYCASE_COLOR, (0,0), TROPHYCASE_WIDTH).image.copy(),
                "BACKDROP" : dinosInSpace.loadImage("snaxWorldBkg.png", "4X"),
                "TROPHY_TEXT_FRAME" : dinosInSpace.loadImage("snackTrophyTextFrame.png", "2X", (0,0))
            ##"" : dinosInSpace.loadImage()
            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image " + str(name) + " not found"

class SnaxWorld(object):
    """ state that runs the snax screen """
    me = None

    def __init__(self, background=None):

        self.screen = pygame.display.get_surface()
        if background:
            self.bkg = background
        else:
            self.bkg = pygame.Surface(self.screen.get_size())
            self.bkg.fill(COL_BACKGROUND)
        self.screen.blit(self.bkg, (0,0))

        self.bkgGroup = pygame.sprite.Group()
        self.gridGroup = pygame.sprite.RenderUpdates()
        self.snaxGroup = pygame.sprite.RenderUpdates()
        self.buttonGroup = pygame.sprite.RenderUpdates()
        self.basicGroup = pygame.sprite.RenderUpdates()
        self.cursorGroup = pygame.sprite.RenderUpdates()

        SnaxWorld.me = self

    @staticmethod
    def addSpriteToGroup(spr, group):
        if group == "BKG":
            SnaxWorld.me.bkgGroup.add(spr)
        elif group == "GRID":
            SnaxWorld.me.gridGroup.add(spr)
        elif group == "SNAX":
            SnaxWorld.me.snaxGroup.add(spr)
        elif group == "BUTTON":
            SnaxWorld.me.buttonGroup.add(spr)
        elif group == "BASIC":
            SnaxWorld.me.basicGroup.add(spr)
        elif group == "CURSOR":
            SnaxWorld.me.cursorGroup.add(spr)
        else:
            print group + " is an unrecognized group, spr not added"

    @staticmethod
    def addSpriteListToGroup(sprList, group):
        for spr in sprList:
            SnaxWorld.addSpriteToGroup(spr, group)

    def runMe(self, _fps, imageFrom):
        clock = pygame.time.Clock()
        dest = None

        while not dest:
            clock.tick(_fps)
            dest = self.getInput()

            self.bkgGroup.clear(self.screen, self.bkg)
            self.gridGroup.clear(self.screen, self.bkg)
            self.snaxGroup.clear(self.screen, self.bkg)
            self.buttonGroup.clear(self.screen, self.bkg)
            self.basicGroup.clear(self.screen, self.bkg)
            self.cursorGroup.clear(self.screen, self.bkg)

            self.bkgGroup.update()
            self.gridGroup.update()
            self.snaxGroup.update()
            self.buttonGroup.update()
            self.basicGroup.update()
            self.cursorGroup.update()

            self.bkgGroup.draw(self.screen)
            self.gridGroup.draw(self.screen)
            self.snaxGroup.draw(self.screen)
            self.buttonGroup.draw(self.screen)
            self.basicGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "down")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            # if dest is from a bonus button, handle then clear dest
            if dest in BONUS_DESTS:

                dest = None


        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, self.bkg)

        self.gridGroup.draw(self.screen)
        self.snaxGroup.draw(self.screen)
        self.buttonGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #
        soundFx56.SoundPlayer.requestSound("woosh_b")

        return snapshot

    def getInput(self):
        dest = None

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dest = "EXIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    dest = self.checkButtonPressed()

        return dest

    def checkButtonPressed(self):
        dest = None

        for spr in self.buttonGroup:
            dest = spr.checkPressed()
            if dest:
                break

        return dest

    @staticmethod
    def wipe():
        SnaxWorld.me = None


class SnaxTrophy(pygame.sprite.Sprite):
    """ an image of the snack that appears in the archive
        - checking for collected snax happens outside of this class (will not be created if not collected)
    """

    def __init__(self, imageKey):
        pygame.sprite.Sprite.__init__(self)

        self.image = ImgLib.getImage(imageKey)
        self.rect = self.image.get_rect()
        self.name = imageKey # used for trophy name when mouse over

    def centerAt(self, center):
        self.rect.center = center

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            TrophyName.setName(self.name)
            TrophyImage4X.setImage(self.name)

class TrophyName(infoGraphic56.TextObject):
    """
        dislayed text of trophy name when mouse over
    """
    me = None

    def __init__(self, center):
        infoGraphic56.TextObject.__init__(self, TNAME_TEXT, TNAME_SIZE, TNAME_COLOR, None )
        self.image = gfx56.centerBlit(ImgLib.getImage("TROPHY_TEXT_FRAME"), self.image.copy())
        self.rect = self.image.get_rect()
        TrophyName.me = self
        self.center = center
        self.rect.center = center

    @staticmethod
    def setNameToDefault():
        TrophyName.setName(TNAME_TEXT)

    @staticmethod
    def setName(name):
        TrophyName.me.rerender(name, TNAME_COLOR)
        TrophyName.me.image = gfx56.centerBlit(ImgLib.getImage("TROPHY_TEXT_FRAME"), TrophyName.me.image.copy())
        TrophyName.me.rect = TrophyName.me.image.get_rect()
        TrophyName.me.rect.center = TrophyName.me.center

    @staticmethod
    def wipe():
        TrophyName.me = None


class TrophyImage4X(pygame.sprite.Sprite):
    me = None

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)

        self.defaultImage = ImgLib.getImage("TROPHY_IMAGE4X_DEFAULT")
        self.image = self.defaultImage
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.center = center

        TrophyImage4X.me = self

    @staticmethod
    def setImage(name):
        imageName = name + "_4x"
        TrophyImage4X.me.image = gfx56.centerBlit(TrophyImage4X.me.image.copy(), ImgLib.getImage(imageName))
##        TrophyImage4X.me.image = ImgLib.getImage(imageName) # -- old way to get (just) image
        TrophyImage4X.me.rect = TrophyImage4X.me.image.get_rect()
        TrophyImage4X.me.rect.center = TrophyImage4X.me.center

    @staticmethod
    def setImageToDefault():
        TrophyImage4X.me.image = TrophyImage4X.me.defaultImage
        TrophyImage4X.me.rect = TrophyImage4X.me.image.get_rect()
        TrophyImage4X.me.rect.center = TrophyImage4X.me.center

    @staticmethod
    def wipe():
        TrophyImage4X.me = None

class SnaxGrid(object):
    """ abstract grid which holds snax trophies """

    def __init__(self, gridSize, lineStep, origin=(0,0), color=(255,255,255), lineWidth=2):

        self.gridSize = gridSize
        self.lineStep = lineStep
        self.origin = origin

        self.totalWidth = gridSize[0] * lineStep
        self.totalHeight = gridSize[1] * lineStep

        self.xLines = []
        self.yLines = []

        count = 0
        for l in range(gridSize[0] + 1):
            self.xLines.append(SnaxGridLine((lineWidth, self.totalHeight), color, (origin[0] + count*lineStep, origin[1])))
            count += 1

        count = 0
        for l in range(gridSize[1] + 1):
            self.yLines.append(SnaxGridLine((self.totalWidth, lineWidth), color, (origin[0], origin[1] + count*lineStep)))
            count += 1

        SnaxWorld.addSpriteListToGroup(self.xLines, "GRID")
        SnaxWorld.addSpriteListToGroup(self.yLines, "GRID")

    def addTrophy(self, trophyKey):
        """ create and add trophy to grid """
        position = self.absolutePosForPoint(TROPHY_GRIDPOINT[trophyKey])
        t = SnaxTrophy(trophyKey)
        t.centerAt((position[0] + self.lineStep/2, position[1] + self.lineStep/2))
        SnaxWorld.addSpriteToGroup(t, "SNAX")

    def absolutePosForPoint(self, gridPoint):
        x = self.origin[0] + (gridPoint[0] * self.lineStep)
        y = self.origin[1] + (gridPoint[1] * self.lineStep)

        return (x, y)


class SnaxGridLine(pygame.sprite.Sprite):
    """ grid line generated by snax grid """

    def __init__(self, size, color, topLeft):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft


class Cursor(pygame.sprite.Sprite):
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = ImgLib.getImage("CURSOR")
        self.rect = pygame.Rect((0,0,1,1))
        Cursor.me = self
        self.firstCycle = True

        SnaxWorld.addSpriteToGroup(self, "CURSOR")

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()
            if not pygame.sprite.spritecollideany(self, SnaxWorld.me.snaxGroup):
                TrophyName.setNameToDefault()
                TrophyImage4X.setImageToDefault()
        else:
            self.rect.topleft = (2000,2000)
            self.firstCycle = False

    @staticmethod
    def wipe():
        Cursor.me = None


def makePillBackground(gridOrigin, gridWidth, gridHeight, customBackdrop=None):
#    pygame.draw.ellipse(Surface, color, Rect, width=0): return Rect
#    pygame.draw.rect(Surface, color, Rect, width=0): return Rect

    background = pygame.Surface((800,600))
    background.fill(COL_BACKGROUND)
    if customBackdrop:
        background = customBackdrop
    ellipseWidth = 2 * gridOrigin[0]
    ellipseRect1 = (0, gridOrigin[1], ellipseWidth, gridHeight)
    ellipseRect2 = (800 - ellipseWidth, gridOrigin[1], ellipseWidth, gridHeight)
    bodyRect = (gridOrigin[0], gridOrigin[1], gridWidth, gridHeight)

    pygame.draw.ellipse(background, PILL_COLOR, ellipseRect1, PILL_EDGE_WIDTH)
    pygame.draw.ellipse(background, PILL_COLOR, ellipseRect2, PILL_EDGE_WIDTH)
    pygame.draw.rect(background, PILL_COLOR, bodyRect, PILL_EDGE_WIDTH)

    return background

def launch(profileName, _fps, snapshot):
    assert(dataStorage56.checkForProfile(profileName))
    ImgLib()
    snaxWidth = ImgLib.getImage("barbequarks").get_width()

    gridWidth       = GRID_STEP * GRID_SIZE[0]
    gridHeight      = GRID_STEP * GRID_SIZE[1]
    gridOrigin      = (400 - gridWidth/2, 300 - gridHeight/2 + GRID_OFFSET_Y)
    gridColor       = GRID_COLOR

    exitSize        = (800, 50)
    exitColor0      = (100,100,100)
    exitColor1      = SUB_LIGHT
    exitText        = "BACK"
    exitFontSize    = 20
    exitFontColor   = BLACK
    exitCenter      = (400, 575)
    exitDest        = "EXIT"

    backdropImage = ImgLib.getImage("BACKDROP")
    backgroundImage = makePillBackground(gridOrigin, gridWidth, gridHeight, backdropImage)

    img = ImgLib.getImage
    snaxWorld = SnaxWorld(backgroundImage)
    snaxRecord = dataStorage56.getSnaxRecord(profileName)
    snaxGrid = SnaxGrid(GRID_SIZE, GRID_STEP, gridOrigin, GRID_COLOR)

    featureFrame = spriteBasic.BasicRect((GRID_STEP*2, GRID_STEP*2), SNAX_FEATURE_BKG_COLOR)
    snaxTextFrame = spriteBasic.BasicRect((gridWidth - GRID_STEP*2, SNAX_TEXT_BKG_HEIGHT), SNAX_TEXT_BKG_COLOR)
    featureFrame.rect.bottomleft = gridOrigin
    snaxTextFrame.rect.bottomright = (gridOrigin[0] + gridWidth, gridOrigin[1])

    exitButton = button.Button(exitDest, exitSize, exitCenter, (exitColor0, exitColor1), exitText, exitFontSize, exitFontColor)

    snaxWorld.addSpriteToGroup(exitButton, "BUTTON")
#    snaxWorld.addSpriteListToGroup([featureFrame, snaxTextFrame], "BKG")

    snaxCursor = Cursor()

    for s in snaxRecord:
        snaxGrid.addTrophy(s)

    trophyFeatureX = gridOrigin[0] + GRID_STEP
    trophyFeatureY = gridOrigin[1]/2
    trophyFeatureCenter = (trophyFeatureX - TROPHY_FEATURES_XOFFSET, trophyFeatureY - TROPHY_FEATURES_YOFFSET)
    trophyNameCenter = (gridOrigin[0] + 2*GRID_STEP + (gridWidth - 2*GRID_STEP)/2 + TROPHY_FEATURES_XOFFSET, gridOrigin[1]/2 - TROPHY_FEATURES_YOFFSET)
    TrophyName(trophyNameCenter)
    TrophyImage4X(trophyFeatureCenter)
    snaxWorld.addSpriteListToGroup([TrophyName.me, TrophyImage4X.me], "BASIC")

    snapshot = snaxWorld.runMe(_fps, snapshot) # there's no dest here because the only option is to go back
    wipe()
    return snapshot

def wipe():
    # DONT wipe Bonus switch here - only when player ends profile session
    SnaxWorld.wipe()
    Cursor.wipe()
    TrophyName.wipe()
    TrophyImage4X.wipe()



#    if snaxMilestone[0]:
#        switch0 = button.Button(None, (img("SWITCH_OFF0"), img("SWITCH_OFF1")), switch0_center)
#        plate0 = BonusPlate(img("MODE_LOCKED"), (switch0.rect.topright[0] + 10, switch0.rect.topright[1]))
#    else:
#        switch0 = BonusSwitch("HATS", ((img("SWITCH_OFF0"), img("SWITCH_OFF1")), (img("SWITCH_ON0"), img("SWITCH_ON1"))), switch0_center, 0)
#        plate0 = BonusPlate(img("MODE_LOCKED"), (switch0.rect.topright[0] + 10, switch0.rect.topright[1]))
#
#    if snaxMilestone[1]:
#        switch1 = button.Button(None, (img("SWITCH_OFF0"), img("SWITCH_OFF1")), switch1_center)
#    else:
#        switch1 = BonusSwitch("NYAN", ((img("SWITCH_OFF0"), img("SWITCH_OFF1")), (img("SWITCH_ON0"), img("SWITCH_ON1"))), switch1_center, 1)
#
#    if snaxMilestone[2]:
#        switch2 = button.Button(None, (img("SWITCH_OFF0"), img("SWITCH_OFF1")), switch2_center)
#    else:
#        switch2 = BonusSwitch("XTRA", ((img("SWITCH_OFF0"), img("SWITCH_OFF1")), (img("SWITCH_ON0"), img("SWITCH_ON1"))), switch2_center, 2)
#
#testToggle = button.ImageToggler("TESTDEST", ((img("BLUESNAX"), img("GREENSNAX")), (img("PINKSNAX"), img("REDSNAX"))))
#    snaxWorld.addSpriteListToGroup([switch0, switch1, switch2], "BUTTON")
#    SnaxWorld.addSpriteListToGroup([plate0], "BASIC")

    #snaxMilestone = dataStorage56.getMilestone(profileName)



#    switch0_center  = (100,180)
#    switch1_center  = (100,300)
#    switch2_center  = (100,420)


#class BonusSwitch(button.ImageToggler):
#    """
#        adds state tracking to ImageToggler for persistence throughout profile session
#        - bonus switch only created if bonus milestone is reached - different object created if not
#    """
#    states = [0, 0, 0] # 0 or 1
#
#    def __init__(self, dest, frameSet, center, switchNum):
#        button.ImageToggler.__init__(self, dest, frameSet, center)
#
#        self.switchNum = switchNum
#        self.mode = dest
#
#        if BonusSwitch.states[self.switchNum]:
#            self.toggle()
#
#    @staticmethod
#    def clearStates():
#        """ should be called only when user quits profile session """
#        BonusSwitch.states = [0, 0, 0]
#
#    def checkPressed(self):
#        """ called upon mouse click - override to set state"""
#        if self.mouseOver:
#            modeSwitch.ModeSwitch.toggleMode(self.mode)
#            self.toggle()
#            if BonusSwitch.states[self.switchNum]:
#                BonusSwitch.states[self.switchNum] = 0
#            else:
#                BonusSwitch.states[self.switchNum] = 1
#            return self.dest
#
#class BonusPlate(pygame.sprite.Sprite):
#    """ image with or without centered text: determined in launch """
#
#    def __init__(self, image, topleft, text=None, textColor=None):
#        pygame.sprite.Sprite.__init__(self)
#
#        self.image = image
#        self.rect = self.image.get_rect()
#        self.rect.topleft = topleft
#
#        if text:
#            textSurf = infoGraphic56.TextObject(text, PLATE_TXTSIZE, textColor).image
#            self.image = gfx56.centerBlit(self.image, textSurf)

##class SimpleButton(
##
##    def __init__(self, size, color0, color1, text, fontSize, fontColor, center, myDest):
##        pygame.sprite.Sprite.__init__(self)
##        self.mouseOver = False
##        self.makeButtons(size, color0, color1, text, fontSize, fontColor)
##        self.image = self.imgOff
##        self.rect = self.image.get_rect()
##        self.rect.center = center
##        self.myDest = myDest
##
##        SnaxWorld.addSpriteToGroup(self, "BUTTON")
##
##    def update(self):
##        if pygame.sprite.collide_rect(self, Cursor.me):
##            self.image = self.imgOn
##            self.mouseOver = True
##        else:
##            self.image = self.imgOff
##            self.mouseOver = False
##
##    def makeButtons(self, size, color0, color1, text, fontSize, fontColor):
##        self.imgOff = pygame.Surface(size)
##        self.imgOff.fill(color0)
##        self.imgOn = pygame.Surface(size)
##        self.imgOn.fill(color1)
##        font = dinosInSpace.FontBank.getFont(fontSize)
##        text = font.render(text, False, fontColor)
##        textBlitX = ( size[0] - text.get_width() ) / 2
##        textBlitY = ( size[1] - text.get_height() ) / 2
##        self.imgOff.blit(text, (textBlitX, textBlitY))
##        self.imgOn.blit(text, (textBlitX, textBlitY))
##
##    def getDest(self):
##        return self.myDest


