""" areaSelect.py"""

import pygame
import dinosInSpace
import scroller56
import os
import dataStorage56
import spriteBasic
import infoGraphic56
import sector
import groupMods56
import gfx56
import screenWipe
import fpsSwitch
import soundFx56
import sparkleTrail

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ADD PORTAL |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| LOOK FOR THIS ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
BLACK = (0,0,0)
WHITE = (255,255,255)
LTGREY2 = (200,200,200)
LTGREY = (150,150,150)
GREY = (100,100,100)
DGREY = (60,60,60)
ORANGE = (255,125,0)
GREEN = (0,255,0)
RED = (255,0,0)
DARK_RED = (150,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
TEAL = (0,50,50)

FIELDSIZE           = (8,8) # 12
XGRIDSTEP           = 100
YGRIDSTEP           = 100

MAX_SNAX = 24 # last puzzle unlocks at...

# info bar
INFOBAR_WIDTH = 200
INFOBAR_YSTEP = 25
INFOBAR_BOX_UNIT_SIZE = (INFOBAR_WIDTH, 2*INFOBAR_YSTEP)
LOCKED_FONTSIZE = 20
LOCKED_BKGCOLOR = WHITE
DEFAULT_FONTSIZE = 20
TITLE_FONTSIZE = 18
SMALL_FONTSIZE = 16
XTRA_SMALL_FONTSIZE = 12
IB_ALPHA = None
SNAX_COLLECTED_TEXT_COLOR = ORANGE
SNAX_GFX_SPACING = 30
SNAX_GFX_ALPHA = 100
SNAX_BOX_COLOR = ORANGE

PORTAL_NUMSIZE              = 14
PORTAL_NUMCOLOR             = (255,255,255)
PORTAL_NUMBLIT              = (5,5)
PORTAL_SCALEBY              = 20
PORTAL_LABEL_OFFSET         = (0,-80)
PORTAL_LABEL_ALPHA_STD      = 250
PORTAL_LABEL_ALPHA_BLINK    = 150
PORTAL_LABEL_BLINK_DELAY    = 5 # *2 for 60 fps

PORTAL_SGLYPH_SIZE = 16
PORTAL_SGLYPH_COLOR = DARK_RED
PORTAL_SGLYPH_BLIT = (5,25)
PORTAL_SGLYPH_TEXT = "s!"

SECTORS = [0, # 1
           1, # 2 - 3 - 4
           4, # 5 - 6 - 7 - 8 - 9 - 10
           8, # 11 - 12 - 13 - 14 - 15 - 16
           14,# 17 - 18 - 19 - 20 - 21 - 22
           19,# 23 - 24 - 25 - 26 - 27 - 28
           24,# 29 - 30 - 31 - 32 - 33 - 34
           30,# 35 - 36 - 37 - 38 - 39 - 40
           40]# 41
SNAX_ARCHIVE        = "_snaxArchive"
SNAX_MILESTONE      = "_snaxMilestone"
NON_PUZZLE_ENTRY    = [SNAX_ARCHIVE, SNAX_MILESTONE, "quit to title", "interstellar snax ship"]
TUTORIAL_LENGTH = 7 # for totals reference, plz sync with actual number of TUT portals / puzzles %%%%%%%%%%%%%%%%%%%%%%%% TUTORIAL_LENGTH %%%%%%%%

##WITH_SPARKLE    = True
##SPARK_SIZE      = (6,6)
##SPARK_COLOR     = WHITE
##SPARK_BOUNDS    = (800,600)
##SPARK_FREQUENCY = 15 #1)--15
##SPARK_FADESPEED = 5 #1)--2
##SPARK_CENTER    = (400,300)
##SPARK_VELOCITY  = (0,0)

NEW_PROFILE = {
    # puzzle name   :   [file name, locked, complete, difficulty, snacks collected, unlocked after...]
    #
    #   -0 (string) _file name_     : passed as 'dest' to map selector (level)
    #   -1 (bool)   _locked_        : controlls player access / preview
    #   -2 (bool)   _complete_      : displays if complete, adds to global profile completed count
    #   -3 (int)    _difficulty_    : displays difficulty level
    #   -4 (list)   _snacks_        : displays how many snacks collected as list (0 or 1), pass 'None' if n/a
    #   -5 (int)    _lock number_   : portal is unlocked after this number of total completed puzzles
    #
    #
    #   example:
    #
    #       "roundabout" : ["2_ROUNDABOUT", True, False, 0, [0,0], SECTORS[1]],
    #
    # ********************
    # _snaxArchive   :   [snackName1, snackName2, snackName3...]
    # ********************

    # misc data
    "_snaxArchive"  :   [], # list of snax collected for snax screen to access
    "_snaxMilestone" : [1,3,20],  # num of snax required to unlock stuff, changes to 0 when achieved

    # non-puzzle portals
    "quit to title"          :   ["_EXIT", False, False, 0, None, SECTORS[0]],
    "interstellar snax ship"     :   ["_SNAX", False, False, 0, None, SECTORS[0]],

    #puzzle portals -- don't forget to sync tutorial length constant
    "tutorial" : ["1_TUT1", False, False, 0, None, SECTORS[0]],
    "tut2" : ["1_TUT2", False, False, 0, None, SECTORS[0]],
    "tut3" : ["1_TUT3", False, False, 0, None, SECTORS[0]],
    "tut4" : ["1_TUT4", False, False, 0, None, SECTORS[0]],
    "tut5" : ["1_TUT5", False, False, 0, None, SECTORS[0]],
    "tut6" : ["1_TUT6", False, False, 0, None, SECTORS[0]],
    "tut7" : ["1_TUT7", False, False, 0, None, SECTORS[0]],

    "odd color out" : ["2_ODD_COLOR_OUT", True, False, 0, None, SECTORS[1]], # 1
    "small detour" : ["3_SMALL_DETOUR", True, False, 0, None, SECTORS[1]],
    "go for it" : ["4_GO_FOR_IT", True, False, 0, [0], SECTORS[1]],
    "switches" : ["5_SWITCHES", True, False, 0, None, SECTORS[2]], # 2
    "space walk" : ["6_SPACE_WALK", True, False, 0, None, SECTORS[2]],
    "wait for me" : ["7_WAIT_FOR_ME", True, False, 0, None, SECTORS[2]],
    "crowded crew 1" : ["8_CROWDED_CREW_1", True, False, 0, None, SECTORS[2]],
    "cross paths"   :   ["9_CROSS_PATHS", True, False, 0, [0,0], SECTORS[2]],
    "loop" : ["10_LOOP", True, False, 0, [0,0], SECTORS[2]],
    "island" : ["11_ISLAND", True, False, 0, None, SECTORS[3]], # 3
    "sardines 1" : ["12_SARDINES_1", True, False, 0, [0], SECTORS[3]],
    "current" : ["13_CURRENT", True, False, 0, None, SECTORS[3]],
    "try the hard way" : ["14_TRY_THE_HARD_WAY", True, False, 0, [0], SECTORS[3]],
    "double back" : ["15_DOUBLE_BACK", True, False, 0, None, SECTORS[3]],
    "teamwork" : ["16_TEAMWORK", True, False, 0, None, SECTORS[3]],
    "over and out" : ["17_OVER_AND_OUT", True, False, 0, None, SECTORS[4]], # 4
    "symmetry 1" : ["18_SYMMETRY_1", True, False, 0, None, SECTORS[4]],
    "corral" : ["19_CORRAL", True, False, 0, [0,0], SECTORS[4]],
    "crowded crew 2" : ["20_CROWDED_CREW_2", True, False, 0, None, SECTORS[4]],
    "split up" : ["21_SPLIT_UP", True, False, 0, [0,0], SECTORS[4]],
    "asteroid field" : ["22_ASTEROID_FIELD", True, False, 0, None, SECTORS[4]],
    "jump the fence" : ["23_JUMP_THE_FENCE", True, False, 0, None, SECTORS[5]], # 5
    "symmetry 2" : ["24_SYMMETRY_2", True, False, 0, None, SECTORS[5]],
    "separate" : ["25_SEPARATE", True, False, 0, None, SECTORS[5]],
    "under your nose" : ["26_UNDER_YOUR_NOSE", True, False, 0, [0,0], SECTORS[5]],
    "so close yet so far" : ["27_SO_CLOSE_YET_SO_FAR", True, False, 0, None, SECTORS[5]],
    "sections" : ["28_SECTIONS", True, False, 0, None, SECTORS[5]],
    "sardines 2" : ["29_SARDINES_2", True, False, 0, None, SECTORS[6]], # 6
    "tasty trove" : ["30_TASTY_TROVE", True, False, 0, [0,0], SECTORS[6]],
    "sandbar" : ["31_SANDBAR", True, False, 0, [0,0], SECTORS[6]],
    "hopscotch" : ["32_HOPSCOTCH", True, False, 0, [0], SECTORS[6]],
    "corners" : ["33_CORNERS", True, False, 0, [0], SECTORS[6]],
    "copy cat" : ["34_COPY_CAT", True, False, 0, [0], SECTORS[6]],
    "small loop" : ["35_SMALL_LOOP", True, False, 0, None, SECTORS[7]], # 7
    "outpost" : ["36_OUTPOST", True, False, 0, None, SECTORS[7]],
    "take a hike" : ["37_TAKE_A_HIKE", True, False, 0, None, SECTORS[7]],
    "not so fast" : ["38_NOT_SO_FAST", True, False, 0, [0,0,0], SECTORS[7]],
    "really crowded crew" : ["39_REALLY_CROWDED_CREW", True, False, 0, None, SECTORS[7]],
    "rescue" : ["40_RESCUE", True, False, 0, [0], SECTORS[7]],
    "gateway" : ["41_GATEWAY", True, False, 0, None, SECTORS[8]] # 8


} # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ADD PORTAL |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| add snax ||||||||||||||||||||||||||||||||||||||||
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ^^^^^^^^^

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:

            ImgLib.imgDict = {
                "CURSOR"            :   dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "PUZZLE_PREVIEW"    :   dinosInSpace.loadImage("portalPrevDefault.png", "2X"),
##                "TEST1"             :   dinosInSpace.loadImage("rock2.png", "2X", (0,0)),
##                "TEST2"             :   dinosInSpace.loadImage("rock3.png", "2X", (0,0)),
##                "TESTPREV"          :   dinosInSpace.loadImage("testPreview.png", (200,150), None),
##                "TESTPREV_E"        :   dinosInSpace.loadImage("testPreviewEmpty.png", (200,150), None),
                "LOCKED"            :   infoGraphic56.TextObject("locked", LOCKED_FONTSIZE, DARK_RED, None, True, False, LOCKED_BKGCOLOR).image.copy(),
                "SNAX"              :   dinosInSpace.loadImage("hamburger.png", "2X", (0,0)),
                "SNAX_LOCKED"       :   dinosInSpace.loadImage("hamburgerLocked.png", "2X", (0,0)),
                "PORT_LOCK"         :   dinosInSpace.loadImage("portalLocked.png", "2X", (0,0)),
                "PORT_OPEN"         :   dinosInSpace.loadImage("portalOpen.png", "2X", (0,0)),
                "PORT_COMP"         :   dinosInSpace.loadImage("portalComplete.png", "2X", (0,0)),
                "PORT_FLAG"         :   dinosInSpace.loadImage("flagBasic.png", "2X", (0,0)),
                "PORT_FLAGPLUS"     :   dinosInSpace.loadImage("flagComplete.png", "2X", (0,0)),
                "BACK_ARROW"        :   dinosInSpace.loadImage("backArrow.png", "2X", (0,0)),
                "SNAX_BOX"          :   pygame.Surface(INFOBAR_BOX_UNIT_SIZE),
                "SNAX_SUB"         :   dinosInSpace.loadImage("snaxSub.png", "2X", (0,0)),
                "SNAX_SUB_PARTY"         :   dinosInSpace.loadImage("snaxSubParty.png", "2X", (0,0)),
                "PORTAL_LABEL"      : dinosInSpace.loadImage("portalLabel.png", "2X", (0,75)),

                # map previews - requested by portals during init
                "quit to title"              :   dinosInSpace.loadImage("pp_title.png"),
                "interstellar snax ship"        :   dinosInSpace.loadImage("pp_snax.png"),
                "tutorial"              :   dinosInSpace.loadImage("pp_tutorial.png"),
                "go for it"             :   dinosInSpace.loadImage("pp_go_for_it.png"),
                "odd color out"     :   dinosInSpace.loadImage("pp_odd_color_out.png"),
                "small detour"      :   dinosInSpace.loadImage("pp_small_detour.png"),
                "crowded crew 1"      :   dinosInSpace.loadImage("pp_crowded_crew_1.png"),
                "switches"          :   dinosInSpace.loadImage("pp_switches.png"),
                "loop"              :   dinosInSpace.loadImage("pp_loop.png"),
                "sardines 1"            :   dinosInSpace.loadImage("pp_sardines_1.png"),
                "corral"            :   dinosInSpace.loadImage("pp_corral.png"),
                "cross paths"       :   dinosInSpace.loadImage("pp_cross_paths.png"),
                "current"           :   dinosInSpace.loadImage("pp_current.png"),
                "over and out"      :   dinosInSpace.loadImage("pp_over_and_out.png"),
                "hopscotch"            :   dinosInSpace.loadImage("pp_hopscotch.png"),
                "outpost"           :   dinosInSpace.loadImage("pp_outpost.png"),
                "island"            :   dinosInSpace.loadImage("pp_island.png"),
                "symmetry 1"          :   dinosInSpace.loadImage("pp_symmetry_1.png"),
                "double back"       :   dinosInSpace.loadImage("pp_double_back.png"),
                "try the hard way"       :   dinosInSpace.loadImage("pp_try_the_hard_way.png"),
                "crowded crew 2"    :   dinosInSpace.loadImage("pp_crowded_crew_2.png"),
                "small loop"        :   dinosInSpace.loadImage("pp_small_loop.png"),
                "wait for me"       :   dinosInSpace.loadImage("pp_wait_for_me.png"),
                "separate"       : dinosInSpace.loadImage("pp_separate.png"),
                "symmetry 2"       : dinosInSpace.loadImage("pp_symmetry_2.png"),
                "teamwork"       : dinosInSpace.loadImage("pp_teamwork.png"),
                "rescue"       : dinosInSpace.loadImage("pp_rescue.png"),
                "copy cat"       : dinosInSpace.loadImage("pp_copy_cat.png"),
                "jump the fence"       : dinosInSpace.loadImage("pp_jump_the_fence.png"),
                "space walk"       : dinosInSpace.loadImage("pp_space_walk.png"),
                "so close yet so far"       : dinosInSpace.loadImage("pp_so_close_yet_so_far.png"),
                "under your nose"       : dinosInSpace.loadImage("pp_under_your_nose.png"),
                "corners"       : dinosInSpace.loadImage("pp_corners.png"),
                "tasty trove"       : dinosInSpace.loadImage("pp_tasty_trove.png"),
                "sections"       : dinosInSpace.loadImage("pp_sections.png"),
                "sardines 2"       : dinosInSpace.loadImage("pp_sardines_2.png"),
                "really crowded crew" : dinosInSpace.loadImage("pp_really_crowded_crew.png"),
                "sandbar" : dinosInSpace.loadImage("pp_sandbar.png"),
                "asteroid field" : dinosInSpace.loadImage("pp_asteroid_field.png"),
                "take a hike" : dinosInSpace.loadImage("pp_take_a_hike.png"),
                "split up" : dinosInSpace.loadImage("pp_split_up.png"),
                "not so fast" : dinosInSpace.loadImage("pp_not_so_fast.png"),
                "gateway" : dinosInSpace.loadImage("pp_gateway.png"),

                "quit to title_L" : dinosInSpace.loadImage("pp_title_L.png"),
                "interstellar snax ship_L"        :   dinosInSpace.loadImage("pp_snax_L.png"),
                "tutorial_L"              :   dinosInSpace.loadImage("pp_tutorial_L.png"),
                "go for it_L"             :   dinosInSpace.loadImage("pp_go_for_it_L.png"),
                "odd color out_L"     :   dinosInSpace.loadImage("pp_odd_color_out_L.png"),
                "small detour_L"      :   dinosInSpace.loadImage("pp_small_detour_L.png"),
                "crowded crew 1_L"      :   dinosInSpace.loadImage("pp_crowded_crew_1_L.png"),
                "switches_L"          :   dinosInSpace.loadImage("pp_switches_L.png"),
                "loop_L"              :   dinosInSpace.loadImage("pp_loop_L.png"),
                "sardines 1_L"            :   dinosInSpace.loadImage("pp_sardines_1_L.png"),
                "corral_L"            :   dinosInSpace.loadImage("pp_corral_L.png"),
                "cross paths_L"       :   dinosInSpace.loadImage("pp_cross_paths_L.png"),
                "current_L"           :   dinosInSpace.loadImage("pp_current_L.png"),
                "over and out_L"      :   dinosInSpace.loadImage("pp_over_and_out_L.png"),
                "hopscotch_L"            :   dinosInSpace.loadImage("pp_hopscotch_L.png"),
                "outpost_L"           :   dinosInSpace.loadImage("pp_outpost_L.png"),
                "island_L"            :   dinosInSpace.loadImage("pp_island_L.png"),
                "symmetry 1_L"          :   dinosInSpace.loadImage("pp_symmetry_1_L.png"),
                "double back_L"       :   dinosInSpace.loadImage("pp_double_back_L.png"),
                "try the hard way_L"       :   dinosInSpace.loadImage("pp_try_the_hard_way_L.png"),
                "crowded crew 2_L"    :   dinosInSpace.loadImage("pp_crowded_crew_2_L.png"),
                "small loop_L"        :   dinosInSpace.loadImage("pp_small_loop_L.png"),
                "wait for me_L"       :   dinosInSpace.loadImage("pp_wait_for_me_L.png"),
                "separate_L"       : dinosInSpace.loadImage("pp_separate_L.png"),
                "symmetry 2_L"       : dinosInSpace.loadImage("pp_symmetry_2_L.png"),
                "teamwork_L"       : dinosInSpace.loadImage("pp_teamwork_L.png"),
                "rescue_L"       : dinosInSpace.loadImage("pp_rescue_L.png"),
                "copy cat_L"       : dinosInSpace.loadImage("pp_copy_cat_L.png"),
                "jump the fence_L"       : dinosInSpace.loadImage("pp_jump_the_fence_L.png"),
                "space walk_L"       : dinosInSpace.loadImage("pp_space_walk_L.png"),
                "so close yet so far_L"       : dinosInSpace.loadImage("pp_so_close_yet_so_far_L.png"),
                "under your nose_L"       : dinosInSpace.loadImage("pp_under_your_nose_L.png"),
                "corners_L"       : dinosInSpace.loadImage("pp_corners_L.png"),
                "tasty trove_L"       : dinosInSpace.loadImage("pp_tasty_trove_L.png"),
                "sections_L"       : dinosInSpace.loadImage("pp_sections_L.png"),
                "sardines 2_L"       : dinosInSpace.loadImage("pp_sardines_2_L.png"),
                "really crowded crew_L" : dinosInSpace.loadImage("pp_really_crowded_crew_L.png"),
                "sandbar_L" : dinosInSpace.loadImage("pp_sandbar_L.png"),
                "asteroid field_L" : dinosInSpace.loadImage("pp_asteroid_field_L.png"),
                "take a hike_L" : dinosInSpace.loadImage("pp_take_a_hike_L.png"),
                "split up_L" : dinosInSpace.loadImage("pp_split_up_L.png"),
                "not so fast_L" : dinosInSpace.loadImage("pp_not_so_fast_L.png"),
                "gateway_L" : dinosInSpace.loadImage("pp_gateway_L.png"),

            } # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ADD PORTAL |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            ImgLib.imgDict["SNAX_BOX"].fill(SNAX_BOX_COLOR)

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print("image, " + name + " not found")

class SelectScreen(object):
    """ screen to select stages in story mode """
    me = None

    def __init__(self):
        SelectScreen.me = self

        self.scrollerGroup  = pygame.sprite.GroupSingle()       # scroller updates first
        self.bkgGroup1      = pygame.sprite.RenderUpdates()             # bottom level gfx
##        self.sparkleGroup   = pygame.sprite.OrderedUpdates()
        self.portalGroup    = pygame.sprite.OrderedUpdates()    # level portals
        self.sectorGroup    = groupMods56.SR_OrderedUpdates()   # sectors and sector counters
        self.infoGroup      = pygame.sprite.OrderedUpdates()    # portal info right side of screen
        self.portLabelGroup = pygame.sprite.Group()             # labels over portals as prompts
        self.cursorGroup    = pygame.sprite.RenderUpdates()       # cursor

        self.currentProfile = None
        self.keepGoing      = None
        self.dest           = None
        self.puzzleSelected = None
        self.minSpeed       = dinosInSpace.Game.getMinSpeed()
        self.screen         = pygame.display.get_surface()
        self.background     = pygame.Surface(self.screen.get_size())

        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
##        gfx56.drawBorder(self)
##        pygame.display.update()

##        # create sparkle trail #
##        ########################
##        self.withSparkle = WITH_SPARKLE
##        self.sparkleEffect = None
##        if self.withSparkle:
##            self.sparkleEffect = sparkleTrail.SparkleTrail(SPARK_SIZE, SPARK_COLOR, SPARK_BOUNDS, SPARK_FREQUENCY, SPARK_FADESPEED, self, SPARK_CENTER, SPARK_VELOCITY)
##        ########################
##        ########################


    @staticmethod
    def wipe():
        SelectScreen.me = None

    def setCurrentProfile(self, currentProfile):
        self.currentProfile = currentProfile

    def getMinSpeed(self):
        return self.minSpeed

    def getPortalGroup(self):
        return self.portalGroup

    def addSpriteToGroup(self, sprite, group):
        if group == "SCROLLER":
            self.scrollerGroup.add(sprite)
        elif group == "BKG1":
            self.bkgGroup1.add(sprite)
        elif group == "PORTAL":
            self.portalGroup.add(sprite)
        elif group == "SECTOR":
            self.sectorGroup.add(sprite)
        elif group == "INFO":
            self.infoGroup.add(sprite)
        elif group == "LABEL":
            self.portLabelGroup.add(sprite)
        elif group == "CURSOR":
            self.cursorGroup.add(sprite)

    def addSpriteListToGroup(self, spriteList, group):
        for s in spriteList:
            self.addSpriteToGroup(s, group)

    def getInput(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dest = "_EXIT"

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dest, self.puzzleSelected = AreaCursor.cursor.click()

            if self.dest:
                self.keepGoing = False

    def runMe(self, _fps, imageFrom, swipeDirection):
        clock = pygame.time.Clock()
        self.clock = clock # bugfix for fps [infographic] access (rest of code uses local variable 'clock'
        self.keepGoing = True
        self.dest = None

        while self.keepGoing:
            clock.tick(_fps)
            self.getInput()

            self.bkgGroup1.clear(self.screen, self.background)
##            self.sparkleGroup.clear(self.screen, self.background)
            self.portalGroup.clear(self.screen, self.background)
            self.sectorGroup.clear(self.screen, self.background)
            self.infoGroup.clear(self.screen, self.background)
            self.portLabelGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)

            if not imageFrom:
                self.scrollerGroup.update()

            self.bkgGroup1.update()
##            self.sparkleGroup.update()
            self.portalGroup.update()
            if not imageFrom:
                self.sectorGroup.update()
            self.infoGroup.update()
            self.portLabelGroup.update()
            self.cursorGroup.update()

##            # sparkle update cycle #
##            ########################
##            if self.withSparkle:
##                newUnit = self.sparkleEffect.update()
##                if newUnit:
##                    self.sparkleGroup.add(newUnit)
##            print self.sparkleGroup
##            ########################
##            ########################

            self.bkgGroup1.draw(self.screen)
##            self.sparkleGroup.draw(self.screen)
            self.portalGroup.draw(self.screen)
            self.sectorGroup.draw(self.screen)
            self.infoGroup.draw(self.screen)
            self.portLabelGroup.draw(self.screen)
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
        self.cursorGroup.clear(self.screen, self.background)

        self.bkgGroup1.draw(self.screen)
        self.portalGroup.draw(self.screen)
        self.sectorGroup.draw(self.screen)
        self.infoGroup.draw(self.screen)
        self.portLabelGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #
        if self.dest == "_SNAX":
            soundFx56.SoundPlayer.requestSound("snaxScreen")
        else:
            soundFx56.SoundPlayer.requestSound("woosh_b")

        return self.dest, self.puzzleSelected, snapshot

class ProfileDelegate(object):
    """ container for players saved data
        - holds access and scroll over data
        - portal gets data by request
        - only one instance exists avaliable thru class attribute 'curProfile'
        - fetches data from saved file (via dataStorage module) when initialized

    """
    curProfile = None

    def __init__(self, profileName):
        ProfileDelegate.curProfile = self
        self.dataDict = dataStorage56.getProfile(profileName)
        self.profileName = profileName

    @staticmethod
    def wipe():
        ProfileDelegate.curProfile = None

    def checkForUnlockedAndSyncData(self):
        m = None
        for milestone in self.dataDict[SNAX_MILESTONE]:
            if milestone:
                m = milestone
                break
        if m:
            if len(self.dataDict[SNAX_ARCHIVE]) >= m:
                dataStorage56.logNextMilestone(self.profileName)

    def getPortalData(self, portal):
        """ returns portal data from profile data - called by portals during init """
        return self.dataDict[portal]

    def getTotalsData(self):
        """ returns totals data from current profile - called by InfoBar during init"""
        mapsComplete = 0
        totalMaps = len(self.dataDict) - len(NON_PUZZLE_ENTRY) - (TUTORIAL_LENGTH - 1)
        snaxConsumed = 0
        totalSnax = 0

        for portal in self.dataDict:
            if portal not in NON_PUZZLE_ENTRY:

                if self.dataDict[portal][2]:
                    mapsComplete += 1

                if self.dataDict[portal][4]:
                    for s in self.dataDict[portal][4]:
                        totalSnax += 1
                        if s:
                            snaxConsumed += 1

        mapsRep = "PUZZLES SOLVED : " + str(mapsComplete) + " / " + str(totalMaps)
        snaxRep = "TOTAL SNAX : " + str(snaxConsumed) + " / " + str(totalSnax)

        return mapsRep, snaxRep

    def getNumberSnaxCollected(self):
        """ return the number of snax consumed and the total number of snax """
        totalSnax = 0
        snaxConsumed = 0
        for portal in self.dataDict:
            if portal not in NON_PUZZLE_ENTRY:
                if self.dataDict[portal][4]:
                    for s in self.dataDict[portal][4]:
                        totalSnax += 1
                        if s:
                            snaxConsumed += 1
        return snaxConsumed, totalSnax

    def getMapsComplete(self):
        mapsComplete = 0

        for portal in self.dataDict:
            if portal not in NON_PUZZLE_ENTRY:

                if self.dataDict[portal][2]:
                    mapsComplete += 1

        return mapsComplete

#    def getNumTilUnlock(self, toUnlock):
#        num = toUnlock - self.getMapsComplete()
#        if num < 0:
#            num = 0
#
#        return num

    def getNumTilUnlock(self):

        allComplete = True
        num = 0
        for s in SECTORS:
            if s > self.getMapsComplete():
                num = s - self.getMapsComplete()
                allComplete = False
                break
        return num

    def getProfilePackage(self):
        """ returns profileData in one piece - requested at launch to pass to level """
        return self.dataDict


class Portal(pygame.sprite.Sprite):
    """
        portal to puzzle
        - responds to Scroller
        - unique data accessed by request thru ProfileData
        - scrolling over gives information
        - instance var 'locked' controlls user access
    """
    #   profile data reference (see top)
    #
    #   -0 (string) _file name_     : passed as 'dest' to map selector (level)
    #   -1 (bool)   _locked_        : controlls player access / preview
    #   -2 (bool)   _complete_      : displays if complete, adds to global profile completed count
    #   -3 (int)    _difficulty_    : displays difficulty level
    #   -4 (list)   _snacks_        : displays how many snacks collected as fraction, pass 'None' if n/a
    #   -5 (int)    _lock number_   : portal is unlocked after this number of total completed puzzles

    def __init__(self, name, imgLocked, imgUnlocked, imgComplete, location):
        pygame.sprite.Sprite.__init__(self)

##        self.SCALEFRAC = PORTAL_SCALEFRAC
##        self.SCALE = imgLocked.get_width()/self.SCALEFRAC
        self.SCALE = PORTAL_SCALEBY
        self.name = name

        # fetch stored profile data
        (self.dest,
        self.locked,
        self.complete,
        self.difficulty,
        self.snax,
        self.lockNum)   = ProfileDelegate.curProfile.getPortalData(self.name)

##        self.puzzleNumber = None
##        if self.dest[0] != "_": # exclude _EXIT and _SNAX
##            self.puzzleNumber = self.dest[:self.dest.index("_")]


        if self.locked:
            self.checkLock()

        if self.locked:
            self.original = imgLocked
        elif self.complete:
            self.original = imgComplete
        else:
            self.original = imgUnlocked

        # if snax ship, check for all snax collected
        if self.name == "interstellar snax ship":
            snaxConsumed, totalSnax = ProfileDelegate.curProfile.getNumberSnaxCollected()
            if snaxConsumed == totalSnax: #  total snax should be 24
                self.original = ImgLib.getImage("SNAX_SUB_PARTY")

        # add puzzle number
        if self.dest[0] != "_": # exclude _EXIT and _SNAX
            numSurf = infoGraphic56.TextObject(self.dest[:self.dest.index("_")], PORTAL_NUMSIZE, PORTAL_NUMCOLOR).image
            self.original.blit(numSurf, (PORTAL_NUMBLIT))

        # add s glyph if snax left
        if self.snax:
            for s in self.snax:
                if not s:
                    sGlyph = infoGraphic56.TextObject(PORTAL_SGLYPH_TEXT, PORTAL_SGLYPH_SIZE, PORTAL_SGLYPH_COLOR).image
                    self.original.blit(sGlyph, (PORTAL_SGLYPH_BLIT))
                    break

        self.imgOver    = pygame.transform.scale(self.original, (self.original.get_width() + self.SCALE, self.original.get_height() + self.SCALE))
        self.image      = self.original
        self.rect       = self.image.get_rect()
        self.ready      = False
        self.minSpeed   = SelectScreen.me.getMinSpeed()
        self.previewImg = ImgLib.getImage(self.name)

        self.rect.center = location
        SelectScreen.me.addSpriteToGroup(self, "PORTAL")

        # flag
        self.flag = PortalFlag(self) if self.complete else None
        if self.flag:
            SelectScreen.me.addSpriteToGroup(self.flag, "PORTAL")

        # label
        self.label = None
        if self.name == "tutorial" and not self.complete:
            self.label = PortalLabel(self, ImgLib.getImage("PORTAL_LABEL"), "start here")
            SelectScreen.me.addSpriteToGroup(self.label, "LABEL")

        self.firstCycle = True

    def update(self):
        if not self.firstCycle:
            self.checkCollision()
            self.setSpeed()
        else:
            self.firstCycle = False

    def checkLock(self):
        mapsComplete = ProfileDelegate.curProfile.getMapsComplete()
        if mapsComplete >= self.lockNum:
            # handle last puzzle
            if self.name == "gateway":
                collectedSnax, totalSnax = ProfileDelegate.curProfile.getNumberSnaxCollected()
                    #if collectedSnax == totalSnax:
                if collectedSnax == MAX_SNAX:
                    self.locked = False
            # normal case
            else:
                self.locked = False

    def getPuzzleName(self):
        return self.name

    def setSpeed(self):
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy
        if self.flag:
            self.flag.mimic(dx, dy)
        if self.label:
            self.label.mimic(dx, dy)

    def checkCollision(self):
        if pygame.sprite.collide_rect(self, AreaCursor.cursor):
            if not self.ready:
                self.setReady(True)
        elif self.ready:
            self.setReady(False)

    def setReady(self, ready):
        self.ready = ready
        curCenter = self.rect.center

        if self.ready:
            self.image          = self.imgOver
            self.rect           = self.image.get_rect()
            self.rect.center    = curCenter
            if self.flag:
                self.flag.mimic(-self.SCALE/2, -self.SCALE/2)
                self.flag.scaleUp()
        else:
            self.image          = self.original
            self.rect           = self.image.get_rect()
            self.rect.center    = curCenter
            if self.flag:
                self.flag.mimic(self.SCALE/2, self.SCALE/2)
                self.flag.scaleDown()

        AreaCursor.cursor.addReadyPortal(self) if self.ready else AreaCursor.cursor.removeReadyPortal(self)
        InfoBar.me.display(self) if self.ready else InfoBar.me.clearDisplay(self)

    def isLocked(self):
        return self.locked

    def getDest(self):
        return self.dest

#    def difToString(self):
#        if self.difficulty == 0:
#            rep = "easy"
#        elif self.difficulty == 1:
#            rep = "medium"
#        elif self.difficulty == 2:
#            rep = "hard"
#        elif self.difficulty == 3:
#            rep = "xtra hard"
#        else:
#            rep = "not recognized"
#
#        return rep

    def solvedToString(self):
        if self.name == "quit to title" or self.name == "interstellar snax ship":
            rep = "- - -"
        else:
            if self.complete:
                rep = "Solved"
            else:
                rep = "Unsolved"
        return rep

    def snaxToString(self):
        if self.snax:
            total = len(self.snax)
            consumed = 0

            for s in self.snax:
                if s:
                    consumed += 1

            rep = str(consumed) + " / " + str(total)
        else:
            rep = "N/A"

        return rep


class PortalFlag(pygame.sprite.Sprite):
    """ flag that indicates full or partial completion """

    def __init__(self, portal):
        assert(portal.complete)
        pygame.sprite.Sprite.__init__(self)

        self.portal         = portal
        self.original       = self.chooseFlag()
##        self.SCALE          = self.original.get_width()/portal.SCALEFRAC
        self.SCALE          = PORTAL_SCALEBY
        self.imgOver        = pygame.transform.scale(self.original,
                                                    (self.original.get_width() + self.SCALE,
                                                    self.original.get_height() + self.SCALE))
        self.image          = self.original

        self.rect           = self.image.get_rect()
        self.rect.center    = self.portal.rect.center
##        self.rect.top       = self.portal.rect.top - 45
##        self.rect.left      = self.portal.rect.left

    def chooseFlag(self):
        image = ImgLib.getImage("PORT_FLAGPLUS")

        if self.portal.snax:
            for s in self.portal.snax:
                if not s:
                    image = ImgLib.getImage("PORT_FLAG")

        return image

    def mimic(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def scaleUp(self):
        self.image = self.imgOver

    def scaleDown(self):
        self.image = self.original

class PortalLabel(pygame.sprite.Sprite):

    def __init__(self, portal, image, text, textSize=XTRA_SMALL_FONTSIZE, textColor=BLACK, centerRelativeToPortal=PORTAL_LABEL_OFFSET):
        pygame.sprite.Sprite.__init__(self)

        textSurface = infoGraphic56.TextObject(text, textSize, textColor).image
        self.masterPortal = portal
        self.image = gfx56.centerBlit(image, textSurface)
        self.rect = self.image.get_rect()
        self.rect.center = (self.masterPortal.rect.center[0] + centerRelativeToPortal[0], self.masterPortal.rect.center[1] + centerRelativeToPortal[1])

        self.alphaStandard = PORTAL_LABEL_ALPHA_STD
        self.alphaBlink = PORTAL_LABEL_ALPHA_BLINK
        self.blinkDelay = PORTAL_LABEL_BLINK_DELAY
        if fpsSwitch.FPSSwitch._fps == 60:
            self.blinkDelay *= 2
        self.blinkTick = self.blinkDelay
        self.image.set_alpha(self.alphaStandard, pygame.RLEACCEL)

    def mimic(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy
        self.blink()

    def blink(self):
        self.blinkTick -= 1
        if self.blinkTick < 1:
            self.blinkTick = self.blinkDelay
            if self.image.get_alpha() == self.alphaStandard:
                self.image.set_alpha(self.alphaBlink, pygame.RLEACCEL)
            else:
                self.image.set_alpha(self.alphaStandard, pygame.RLEACCEL)


class AreaCursor(pygame.sprite.Sprite):
    """
        cursor to select portals to puzzles
        - only one instance exists avaliable thru class attribute 'cursor'
    """
    cursor = None

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        AreaCursor.cursor   = self
        self.readyPortals   = []
        self.image          = img
        self.rect           = pygame.rect.Rect(0,0,1,1,)
        self.firstCycle = True

        SelectScreen.me.addSpriteToGroup(self, "CURSOR")

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()
        else:
            self.rect.center = (2000,2000)
            self.firstCycle = False

    @staticmethod
    def wipe():
        AreaCursor.cursor = None

    def addReadyPortal(self, portal):
        self.readyPortals.append(portal)

    def removeReadyPortal(self, portal):
        self.readyPortals.remove(portal)

    def click(self):
        dest = None
        puzzleName = None
        if self.readyPortals and not self.readyPortals[0].isLocked():
            dest = self.readyPortals[0].getDest()
            puzzleName = self.readyPortals[0].getPuzzleName()

        return dest, puzzleName


class InfoBar(spriteBasic.BasicRect):
    """
        subclass of BasicRect manages and displays info for portals
        - takes topRight instead of topleft for init positioning
        - contains methods to control "features" which must be sprite objects

    """
    me = None

    def __init__(self, profileName, size, color, topRight, edgeWidth=None, alpha=None):
        topLeft = (topRight[0] - size[0], topRight[1])
        spriteBasic.BasicRect.__init__(self, size, color, topLeft, edgeWidth, alpha)
        InfoBar.me = self

        WIDTH                       = self.rect.width
        HEIGHT                      = self.rect.height
        LEFT                        = 0
        RIGHT                       = size[0]
        TOP                         = 0
        BOTTOM                      = size[1]
        XMID                        = size[0]/2
        YMID                        = size[1]/2
        YSTEP                       = INFOBAR_YSTEP
        FONTSIZE_S                  = 16

        PROFBOX_HEIGHT              = 50
        PROFBOX_COLOR               = LTGREY
        PROFNAME_COLOR              = BLACK


        self.featureColorOn         = (255, 255, 255)
        self.featureColorOff        = (100, 100, 100)
        self.featureFontSize        = DEFAULT_FONTSIZE
        self.smallFontSize          = SMALL_FONTSIZE
        self.featureDefaultText     = "..."
        self.extrasFontColorOn      = (0, 0, 255)

        # ---- make prof name, labels and totals (constant features)

        # profile box
        profBox_pos                 = (XMID, YSTEP)
        profBox_genPt               = "CENTER"
        profBox                     = spriteBasic.BasicRect((WIDTH, PROFBOX_HEIGHT), PROFBOX_COLOR) # size, color, topLeft, edgeWidth,

        # profile name (at top)
        profName_pos                = (XMID, YSTEP)
        profName_genPt              = "CENTER"
        profName                    = infoGraphic56.TextObject(profileName, TITLE_FONTSIZE, PROFNAME_COLOR)

        # labels
        snaxBox_pos                 = (XMID, 13*YSTEP)
        snaxBox_genPt               = "CENTER"
        snaxBox                     = spriteBasic.BasicImg(ImgLib.getImage("SNAX_BOX"))

        snaxFrame_pos               = (XMID, 15*YSTEP)
        snaxFrame_genPt             = "CENTER"
        snaxFrame                   = spriteBasic.BasicRect(INFOBAR_BOX_UNIT_SIZE, ORANGE, None, 2)

        snaxLabel_pos               = (XMID, 13*YSTEP)
        snaxLabel_genPt             = "CENTER"
        snaxLabel                   = infoGraphic56.TextObject("SNAX COLLECTED", self.smallFontSize, BLACK)

        gTotalsLabel_pos            = (XMID, 30*YSTEP)
        gTotalsLabel_genPt          = "CENTER"
        gTotalsLabel                = infoGraphic56.TextObject("Game Totals:", self.featureFontSize, self.featureColorOff)

        # totals (at bottom)

        ################### get totals data ## ****************
        (mapTotalsRep,
        snaxTotalsRep)              = ProfileDelegate.curProfile.getTotalsData()
        numTilNextSet               = ProfileDelegate.curProfile.getNumTilUnlock()

        if ProfileDelegate.curProfile.getNumberSnaxCollected()[0] == MAX_SNAX:
            unlockText1 = "get every snack"
            unlockText2 = "to unlock last puzzle!"
        else:
            unlockText1                 = "solve " + str(numTilNextSet) + " more puzzle";
            if numTilNextSet > 1: unlockText1 += "s"
            unlockText2                 = "to unlock next set"
        ################### ------------------ ****************

        mapTotals_pos               = (XMID, 600 - 7*YSTEP)
        mapTotals_genPt             = "CENTER"
        mapTotals                   = infoGraphic56.TextObject(mapTotalsRep, XTRA_SMALL_FONTSIZE, LTGREY, None, True) # last tag antialias

        snaxTotals_pos              = (XMID, 600 - 5*YSTEP)
        snaxTotals_genPt            = "CENTER"
        snaxTotals                  = infoGraphic56.TextObject(snaxTotalsRep, XTRA_SMALL_FONTSIZE, LTGREY, None, True)

        bottomMask_pos              = (LEFT, 16*YSTEP)
        bottomMask_genPt            = "TOPLEFT"
        bottomMask                  = spriteBasic.BasicRect((INFOBAR_WIDTH, 200), BLACK)

        puzzleSolvedFrame_pos       = (LEFT, 600 - 8*YSTEP)
        puzzleSolvedFrame_genPt     = "TOPLEFT"
        puzzleSolvedFrame           = spriteBasic.BasicRect(INFOBAR_BOX_UNIT_SIZE, LTGREY, None, 2)

        snaxTotalsFrame_pos         = (LEFT, 600 - 6*YSTEP)
        snaxTotalsFrame_genPt       = "TOPLEFT"
        snaxTotalsFrame             = spriteBasic.BasicRect(INFOBAR_BOX_UNIT_SIZE, LTGREY, None, 2)

        nextUnlockT1_pos            = (XMID, 600 - 3*YSTEP)
        nextUnlockT1_genPt          = "CENTER"
        nextUnlockT1                = infoGraphic56.TextObject(str(unlockText1), XTRA_SMALL_FONTSIZE, BLACK, None, True)

        nextUnlockT2_pos            = (XMID, 600 - 1*YSTEP)
        nextUnlockT2_genPt          = "CENTER"
        nextUnlockT2                = infoGraphic56.TextObject(str(unlockText2), XTRA_SMALL_FONTSIZE, BLACK, None, True)

        nextUnlockBox_pos           = (LEFT, 600 - 4*YSTEP)
        nextUnlockBox_genPt         = "TOPLEFT"
        nextUnlockBox               = spriteBasic.BasicRect((INFOBAR_WIDTH, 4*YSTEP), LTGREY)


        # ---- make variable features:

        # portal name
        self.pName_pos              = (XMID, 3*YSTEP)
        self.pName_genPt            = "CENTER"
        self.pName_defaultText      = "PUZZLE"
        self.pName                  = infoGraphic56.TextObject(self.pName_defaultText, XTRA_SMALL_FONTSIZE, self.featureColorOff)

        # portal preview graphic
        self.pGraphic_pos           = (XMID, 7*YSTEP)
        self.pGraphic_genPt         = "CENTER"
        self.pGraphic_defaultImg    = ImgLib.getImage("PUZZLE_PREVIEW")
        self.pGraphic               = spriteBasic.BasicImg(self.pGraphic_defaultImg)

#        # portal difficulty
#        self.pDif_pos               = (XMID, 8*YSTEP)
#        self.pDif_genPt             = "CENTER"
#        self.pDif_defaultText       = "Difficulty"
#        self.pDif                   = infoGraphic56.TextObject(self.pDif_defaultText, self.featureFontSize, self.featureColorOff)

        # puzzle status solved
        self.pSol_pos               = (XMID, 11*YSTEP)
        self.pSol_genPt             = "CENTER"
        self.pSol_defaultText       = "Solved?"
        self.pSol                   = infoGraphic56.TextObject(self.pSol_defaultText, self.featureFontSize, self.featureColorOff)

        # puzzle snax text
        self.pSnaxText_pos          = (XMID, 15*YSTEP)
        self.pSnaxText_posOn        = (XMID, 15*YSTEP)
        self.pSnaxText_genPt        = "CENTER"
        self.pSnaxText_defaultText  = "- - -"
        self.pSnaxText              = infoGraphic56.TextObject(self.pSnaxText_defaultText, self.featureFontSize, self.featureColorOff)

        # puzzle snax graphic
        self.pSnax_pos              = (2*WIDTH/3 + SNAX_GFX_SPACING, 15*YSTEP)
        self.pSnax_genPt            = "CENTER"
        self.pSnax_defaultImg       = ImgLib.getImage("SNAX"); self.pSnax_defaultImg.set_alpha(SNAX_GFX_ALPHA, pygame.RLEACCEL)
        self.pSnax_liveImg          = ImgLib.getImage("SNAX")
        self.pSnax_lockedImg        = ImgLib.getImage("SNAX_LOCKED")
        self.pSnax                  = spriteBasic.BasicImg(self.pSnax_defaultImg)

        self.pSnax2_pos              = (WIDTH/3 - SNAX_GFX_SPACING, 15*YSTEP)
        self.pSnax2_genPt            = "CENTER"
        self.pSnax2_defaultImg       = ImgLib.getImage("SNAX"); self.pSnax2_defaultImg.set_alpha(SNAX_GFX_ALPHA, pygame.RLEACCEL)
        self.pSnax2_liveImg          = ImgLib.getImage("SNAX")
        self.pSnax2_lockedImg        = ImgLib.getImage("SNAX_LOCKED")
        self.pSnax2                  = spriteBasic.BasicImg(self.pSnax2_defaultImg)


        # ---- initialize position of features and add to group:

        self.setFeaturePosition(profBox, profBox_pos, profBox_genPt)
        self.setFeaturePosition(profName, profName_pos, profName_genPt)
        self.setFeaturePosition(snaxBox, snaxBox_pos, snaxBox_genPt)
        self.setFeaturePosition(snaxFrame, snaxFrame_pos, snaxFrame_genPt)
        self.setFeaturePosition(snaxLabel, snaxLabel_pos, snaxLabel_genPt)
        self.setFeaturePosition(gTotalsLabel, gTotalsLabel_pos, gTotalsLabel_genPt)
        self.setFeaturePosition(bottomMask, bottomMask_pos, bottomMask_genPt)
        self.setFeaturePosition(puzzleSolvedFrame, puzzleSolvedFrame_pos, puzzleSolvedFrame_genPt)
        self.setFeaturePosition(snaxTotalsFrame, snaxTotalsFrame_pos, snaxTotalsFrame_genPt)
        self.setFeaturePosition(mapTotals, mapTotals_pos, mapTotals_genPt)
        self.setFeaturePosition(snaxTotals, snaxTotals_pos, snaxTotals_genPt)
        self.setFeaturePosition(nextUnlockBox, nextUnlockBox_pos, nextUnlockBox_genPt)
        self.setFeaturePosition(nextUnlockT1, nextUnlockT1_pos, nextUnlockT1_genPt)
        self.setFeaturePosition(nextUnlockT2, nextUnlockT2_pos, nextUnlockT2_genPt)
        self.setFeaturePosition(self.pName, self.pName_pos, self.pName_genPt)
        self.setFeaturePosition(self.pGraphic, self.pGraphic_pos, self.pGraphic_genPt)
        self.setFeaturePosition(self.pSol, self.pSol_pos, self.pSol_genPt)
        self.setFeaturePosition(self.pSnaxText, self.pSnaxText_pos, self.pSnaxText_genPt)
        self.setFeaturePosition(self.pSnax, self.pSnax_pos, self.pSnax_genPt)
        self.setFeaturePosition(self.pSnax2, self.pSnax2_pos, self.pSnax2_genPt)

        InfoBar.addToInfoGroup([self,
                                profBox,
                                profName,
                                snaxBox,
                                snaxFrame,
                                snaxLabel,
                                gTotalsLabel,
                                bottomMask,
                                puzzleSolvedFrame,
                                snaxTotalsFrame,
                                mapTotals,
                                snaxTotals,
                                nextUnlockBox,
                                nextUnlockT1,
                                nextUnlockT2,
                                self.pName,
                                self.pGraphic,
                                self.pSol,
                                self.pSnaxText,
                                self.pSnax,
                                self.pSnax2])

    @staticmethod
    def wipe():
        InfoBar.me = None

    @staticmethod
    def addToInfoGroup(spriteList):
        for s in spriteList:
            SelectScreen.me.addSpriteToGroup(s, "INFO")

    def setFeaturePosition(self, feature, pos, genPoint):
        """
            overlays feature on info bar
            -feature must be sprite w/ rect
            -x and y are position relative to InfoBar's top left
            -genPoint can be "TOPLEFT" or "TOPRIGHT" or "CENTER"
        """
        if genPoint == "TOPLEFT":
            feature.rect.topleft = (self.rect.left + pos[0], self.rect.top + pos[1])
        elif genPoint == "TOPRIGHT":
            feature.rect.topright = (self.rect.left + pos[0], self.rect.top + pos[1])
        elif genPoint == "CENTER":
            feature.rect.center = (self.rect.left + pos[0], self.rect.top + pos[1])

    def display(self, portal):
        """ displays portal info when mouse over """
        # portal name
        if not portal.locked:
            self.pName.rerender(portal.name, self.featureColorOn)
        else:
            self.pName.rerender(portal.name, self.featureColorOff)
        self.setFeaturePosition(self.pName, self.pName_pos, self.pName_genPt)

        # portal preview
        if not portal.locked:
            self.pGraphic.setImage(ImgLib.getImage(portal.name))
        else:
            imgKey = portal.name + "_L"
            self.pGraphic.setImage(ImgLib.getImage(imgKey))
            self.pGraphic.superImpose(ImgLib.getImage("LOCKED"), None, True)
        self.setFeaturePosition(self.pGraphic, self.pGraphic_pos, self.pName_genPt)

#        # portal difficulty
#        if not portal.locked:
#            self.pDif.rerender(portal.difToString(), self.featureColorOn)
#        else:
#            self.pDif.rerender(portal.difToString(), self.featureColorOff)
#        self.setFeaturePosition(self.pDif, self.pDif_pos, self.pDif_genPt)

        # puzzle status solved
        if not portal.locked:
            self.pSol.rerender(portal.solvedToString(), self.featureColorOn)
        else:
            self.pSol.rerender(portal.solvedToString(), self.featureColorOff)
        self.setFeaturePosition(self.pSol, self.pSol_pos, self.pSol_genPt)

        # snax text
        if not portal.locked:
            self.pSnaxText.rerender(portal.snaxToString(), SNAX_COLLECTED_TEXT_COLOR)
        else:
            self.pSnaxText.rerender(portal.snaxToString(), self.featureColorOff)
        self.setFeaturePosition(self.pSnaxText, self.pSnaxText_posOn, self.pSnaxText_genPt)

        # snax graphic
        if not portal.locked:
            self.pSnax.setImage(self.pSnax_liveImg)
            self.pSnax2.setImage(self.pSnax2_liveImg)
        else:
            self.pSnax.setImage(self.pSnax_lockedImg)
            self.pSnax2.setImage(self.pSnax2_lockedImg)
        self.setFeaturePosition(self.pSnax, self.pSnax_pos, self.pSnax_genPt)
        self.setFeaturePosition(self.pSnax2, self.pSnax2_pos, self.pSnax2_genPt)

    def clearDisplay(self, portal):
        """ clear display when mouse leaves portal bounds """
        if self.pName.text == portal.name:
            # portal name
            self.pName.rerender(self.pName_defaultText, self.featureColorOff)
            self.setFeaturePosition(self.pName, self.pName_pos, self.pName_genPt)

            # portal preview
            self.pGraphic.setImage(self.pGraphic_defaultImg)
            self.setFeaturePosition(self.pGraphic, self.pGraphic_pos, self.pGraphic_genPt)

#            # portal difficulty
#            self.pDif.rerender(self.pDif_defaultText, self.featureColorOff)
#            self.setFeaturePosition(self.pDif, self.pDif_pos, self.pDif_genPt)

            # puzzle solved status
            self.pSol.rerender(self.pSol_defaultText, self.featureColorOff)
            self.setFeaturePosition(self.pSol, self.pSol_pos, self.pSol_genPt)

            # snax text
            self.pSnaxText.rerender(self.pSnaxText_defaultText, self.featureColorOff)
            self.setFeaturePosition(self.pSnaxText, self.pSnaxText_pos, self.pSnaxText_genPt)

            # snax graphic
            self.pSnax.setImage(self.pSnax_defaultImg)
            self.pSnax2.setImage(self.pSnax2_defaultImg)
            self.setFeaturePosition(self.pSnax, self.pSnax_pos, self.pSnax_genPt)
            self.setFeaturePosition(self.pSnax2, self.pSnax2_pos, self.pSnax2_genPt)

# ----------------------------------------------- functions


def launch(profileName, newGame, _fps, snapshot, swipeDirection):
    """
        build the select screen
        - profileName is name of player's file
        - set newGame to True to write new file
    """

    SCREEN_W    = pygame.display.get_surface().get_width()
    SCREEN_H    = pygame.display.get_surface().get_height()
    IB_W        = SCREEN_W/4
    IB_H        = SCREEN_H
    IB_COL      = (40,40,40)
    IB_TR       = (SCREEN_W, 0)

    ImgLib()
    img = ImgLib.getImage

    if newGame:
        dataStorage56.writeProfile(profileName, NEW_PROFILE)

    profileDelegate = ProfileDelegate(profileName)

    # reset class var lastSnaxCount if coming from load profile only (not coming from puzzles)
    if swipeDirection != "left":
        profileDelegate.checkForUnlockedAndSyncData()


    selectScreen = SelectScreen()
    selectScreen.addSpriteToGroup(scroller56.Scroller(selectScreen, FIELDSIZE, "BL", _fps), "SCROLLER")



    AreaCursor(img("CURSOR"))

    InfoBar(profileName, (IB_W, IB_H), IB_COL, IB_TR, None, IB_ALPHA)

    # Portal (name, imgLocked, imgUnlocked, location)
    Portal("quit to title", img("BACK_ARROW"), img("BACK_ARROW"), img("BACK_ARROW"), grd(1,6))
    Portal("interstellar snax ship", img("SNAX_SUB"), img("SNAX_SUB"), img("SNAX_SUB"), grd(2,6))
    Portal("tutorial", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,6)) # needs label added

    Portal("odd color out", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,6))
    Portal("small detour", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,6))
    Portal("go for it", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,6))
    Portal("switches", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,5))
    Portal("space walk", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,5))
    Portal("wait for me", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,5))
    Portal("crowded crew 1", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,5))
    Portal("cross paths", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,5))
    Portal("loop", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,5))
    Portal("island", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,4))
    Portal("sardines 1", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,4))
    Portal("current", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,4))
    Portal("try the hard way", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,4))
    Portal("double back", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,4))
    Portal("teamwork", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,4))
    Portal("over and out", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,3))
    Portal("symmetry 1", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,3))
    Portal("corral", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,3))
    Portal("crowded crew 2", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,3))
    Portal("split up", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,3))
    Portal("asteroid field", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,3))
    Portal("jump the fence", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,2))
    Portal("symmetry 2", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,2))
    Portal("separate", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,2))
    Portal("under your nose", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,2))
    Portal("so close yet so far", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,2))
    Portal("sections", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,2))
    Portal("sardines 2", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,1))
    Portal("tasty trove", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,1))
    Portal("sandbar", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,1))
    Portal("hopscotch", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,1))
    Portal("corners", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,1))
    Portal("copy cat", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,1))
    Portal("small loop", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(1,0))
    Portal("outpost", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(2,0))
    Portal("take a hike", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(3,0))
    Portal("not so fast", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(4,0))
    Portal("really crowded crew", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(5,0))
    Portal("rescue", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), grd(6,0))

    Portal("gateway", img("PORT_LOCK"), img("PORT_OPEN"), img("PORT_COMP"), (300, grd(3,-1)[1]))

    profileData = profileDelegate.getProfilePackage()

    dest, puzzleName, snapshot = SelectScreen.me.runMe(_fps, snapshot, swipeDirection)
    wipe()

    return dest, puzzleName, snapshot
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ADD PORTAL |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def grd(x, y):
    """ return absolute location from grid """
    return (x * XGRIDSTEP - XGRIDSTEP / 2, y * YGRIDSTEP - YGRIDSTEP / 2)

def wipe():
    """ reset class attributes to none - call before leaving module """
    SelectScreen.wipe()
    ProfileDelegate.wipe()
    AreaCursor.wipe()
    InfoBar.wipe()


#    FPS ---- ****
#    fps = infoGraphic56.FPS(selectScreen)
#    SelectScreen.me.addSpriteToGroup(fps, "BKG1")
#    **** ---- ~~~~




#    # sectors
#    secRadius   = 500
#    secColor    = (50,100,200)
#    secCenter   = (400,700)
#    secWidth    = 1
#    B           = SCREEN_H
#    relCountPos = (secRadius, -20)
#    hideBelow = 1
#
#    #                           curProfile,     color,      center,   radius,   width=0,  toUnlock=0, counterPos=(0,0), hideBelow=0
#    testSector1 = sector.Sector(profileDelegate, secColor, secCenter, secRadius, secWidth, SECTOR1, relCountPos, hideBelow)
#    testSector2 = sector.Sector(profileDelegate, (100, 20, 200), grd(5,2), 600, secWidth, SECTOR2, (600, -20))
#
#    sectorList  = [testSector1, testSector2]
#    counterList = []
#    for s in sectorList:
#        if s.counter:
#            counterList.append(s.counter)
#
#    SelectScreen.me.addSpriteListToGroup(sectorList, "SECTOR")
#    SelectScreen.me.addSpriteListToGroup(counterList, "SECTOR")
#
#    # satellites
#    satRadius = 2
#    spd = .042 # default slow .1  ; creepSnake .02
#    satCount = 145
#    shadeStep = 12
#    tailSize = 2
#
#    if testSector1.unlocked:
#        satList1 = testSector1.makeSatellites(satRadius, spd, satCount, shadeStep, tailSize)
#        SelectScreen.me.addSpriteListToGroup(satList1, "SECTOR")
#    if testSector2.unlocked:
#        satList2 = testSector2.makeSatellites(satRadius, spd, satCount, shadeStep, tailSize)
#        SelectScreen.me.addSpriteListToGroup(satList2, "SECTOR")
#
##    *********************************





