""" editor56.py """

import pygame
import dinosInSpace
import dataStorage56
import textInput56
import infoGraphic56
import os
import groupMods56
import cannon
import tween
import gfx56
import screenCap
import stickyCoord
import screenWipe
import spriteBasic
import soundFx56

PURPLE = (123, 38, 205)
GREY = (150,150,150)

DINO_BLUE = (29,139,255)
DINO_GREEN = (159,247,23)
DINO_RED = (226,70,79)
DINO_YELLOW = (255,246,0)

X_GRIDMIN = 2
Y_GRIDMIN = 2
X_GRIDMAX = 17
Y_GRIDMAX = 17

COORDPAIR_FONTSIZE = 20
STD_FONTSIZE = 20
EDIT_FONTSIZE = 15
LINKED_TILE_FONTSIZE = 30
INPUT_BOX_FONTSIZE = 16

SPAWNSLOT_SIZE = (15,15)
SLOT_DISTANCE_FROM_MIDDLE = 15
SLOT_RIGHT_FIX = -1
SLOT_BOTTOM_FIX = -1

SLOT_COLORS = [
    None,
    DINO_GREEN,
    DINO_BLUE,
    DINO_RED,
    DINO_YELLOW
]

# ---------------------------------------- imgLib, editor (stateobj), origin

class EditorImgLib(object):

    imgDict = None

    def __init__(self):

        if not EditorImgLib.imgDict:

            (SAVE_BTN,
			FILE_BTN_SMALL,
            EXIT_BTN,
            CANCEL_SURF,
            SET_SURF,
            INVSET_SURF,
            DIRECTION_TXT,
            BAR_SURF,
            BAR2_SURF,
            BARLONG_SURF,
            SLOT_TXT,
            DINO_TXT,
            FLIP,
            MORE,
            LESS,
            SWITCHCHAN_TXT,
            OFF_TXT,
            ON_TXT,
            ERROR_FRAME_HOR,
            ERROR_FRAME_VER,
            INV_TXT,
            AMT_TXT,
            INV_BTN,
            FILE_TXT,
            CHANNEL_TXT,
            MAPS_TXT,
            HELP_BTN,
            HELP_CLOSE,
            HELP_MAIN,
            HELP_ENTRY,
            HELP_SWITCH,
            HELP_ERROR) = self.makeSomeButtons()

            AR_G_SURF = dinosInSpace.loadImage("sArrow1.png", "2X", (0,0))
            AR_B_SURF = dinosInSpace.loadImage("sArrow2.png", "2X", (0,0))
            AR_R_SURF = dinosInSpace.loadImage("sArrow3.png", "2X", (0,0))
            AR_Y_SURF = dinosInSpace.loadImage("sArrow4.png", "2X", (0,0))
            AR_W_SURF = dinosInSpace.loadImage("sArrow5.png", "2X", (0,0))
            IAR_G_SURF = dinosInSpace.loadImage("edit_ar_g.png", "2X", (0,0))
            IAR_B_SURF = dinosInSpace.loadImage("edit_ar_b.png", "2X", (0,0))
            IAR_R_SURF = dinosInSpace.loadImage("edit_ar_r.png", "2X", (0,0))
            IAR_Y_SURF = dinosInSpace.loadImage("edit_ar_y.png", "2X", (0,0))
            IAR_W_SURF = dinosInSpace.loadImage("edit_ar_w.png", "2X", (0,0))
            IHAND_SURF = dinosInSpace.loadImage("edit_hand.png", "2X", (0,0))
            EXIT_SURF = dinosInSpace.loadImage("edit_exit.png", "2X", (0,0))
            SPAWN_SURF = dinosInSpace.loadImage("fnSpawn0.png", "2X", (0,0))
            ISPAWN_SURF = dinosInSpace.loadImage("edit_fnSpawn.png", "2X", (0,0))
            FB_G_SQUARE = dinosInSpace.loadImage("greenSquare.png", "2X", None)
            FB_B_SQUARE = dinosInSpace.loadImage("blueSquare.png", "2X", None)
            FB_R_SQUARE = dinosInSpace.loadImage("redSquare.png", "2X", None)
            FB_Y_SQUARE = dinosInSpace.loadImage("yellowSquare.png", "2X", None)
            FB_N_SQUARE = dinosInSpace.loadImage("noSquare.png", "2X", None)
            FB_SPAWNDIR = dinosInSpace.loadImage("edit_spawnDir.png", "2X", (0,0))
            STATION_W = dinosInSpace.loadImage("nStationW0.png", "2X", (0,0))
            STATION_G = dinosInSpace.loadImage("nStationG0.png", "2X", (0,0))
            STATION_B = dinosInSpace.loadImage("nStationB0.png", "2X", (0,0))
            STATION_R = dinosInSpace.loadImage("nStationR0.png", "2X", (0,0))
            STATION_Y = dinosInSpace.loadImage("nStationY0.png", "2X", (0,0))
            ISTA_W = dinosInSpace.loadImage("StationSelectW.png", "2X", (0,0))
            ISTA_G = dinosInSpace.loadImage("StationSelectG.png", "2X", (0,0))
            ISTA_R = dinosInSpace.loadImage("StationSelectR.png", "2X", (0,0))
            ISTA_B = dinosInSpace.loadImage("StationSelectB.png", "2X", (0,0))
            ISTA_Y = dinosInSpace.loadImage("StationSelectY.png", "2X", (0,0))
            IROCK = dinosInSpace.loadImage("edit_rock.png", "2X", (0,0))

            SPINNER_ADD = dinosInSpace.loadImage("spinnerAdd.png", "2X", (0,0))
            SPINNER_SUB = dinosInSpace.loadImage("spinnerSub.png", "2X", (0,0))
            SPINNER_ADD_B = dinosInSpace.loadImage("spinnerAddBlack.png", "2X", (0,0))
            SPINNER_SUB_B = dinosInSpace.loadImage("spinnerSubBlack.png", "2X", (0,0))

            SWITCH_OFF = dinosInSpace.loadImage("nSwitch0.png", "2X", (0,0))
            SWITCH_ON = dinosInSpace.loadImage("nSwitch1.png", "2X", (0,0))
            ISWITCH = dinosInSpace.loadImage("edit_switch.png", "2X", (0,0))

            LINKED_ARR_W = dinosInSpace.loadImage("linkedArrW.png", "2X", (0,0))
            LINKED_ARR_G = dinosInSpace.loadImage("linkedArrG.png", "2X", (0,0))
            LINKED_ARR_B = dinosInSpace.loadImage("linkedArrB.png", "2X", (0,0))
            LINKED_ARR_R = dinosInSpace.loadImage("linkedArrR.png", "2X", (0,0))
            LINKED_ARR_Y = dinosInSpace.loadImage("linkedArrY.png", "2X", (0,0))
            LINKED_FRAME = dinosInSpace.loadImage("linkedFrame.png", "2X", (0,0))
            ILINKED = dinosInSpace.loadImage("edit_linked.png", "2X", (0,0))

            ILINK_ARR_W = dinosInSpace.loadImage("edit_linkArrW.png", "2X", (0,0))
            ILINK_ARR_G = dinosInSpace.loadImage("edit_linkArrG.png", "2X", (0,0))
            ILINK_ARR_B = dinosInSpace.loadImage("edit_linkArrB.png", "2X", (0,0))
            ILINK_ARR_R = dinosInSpace.loadImage("edit_linkArrR.png", "2X", (0,0))
            ILINK_ARR_Y = dinosInSpace.loadImage("edit_linkArrY.png", "2X", (0,0))
            ILINK_FRAME = dinosInSpace.loadImage("edit_linkFrame.png", "2X", (0,0))

            FB_LINKDIR = dinosInSpace.loadImage("cycleLinkedDir.png", "2X", (0,0))

            INV_AR_G = dinosInSpace.loadImage("ArrIconG.png", "2X", (0,0))
            INV_AR_B = dinosInSpace.loadImage("ArrIconB.png", "2X", (0,0))
            INV_AR_R = dinosInSpace.loadImage("ArrIconR.png", "2X", (0,0))
            INV_AR_Y = dinosInSpace.loadImage("ArrIconY.png", "2X", (0,0))
            INV_AR_W = dinosInSpace.loadImage("ArrIconW.png", "2X", (0,0))
            INV_WARP = dinosInSpace.loadImage("warpIcon.png", "2X", (0,0))

            SCROLLUP = dinosInSpace.loadImage("fileScrollUp.png", "2X", (0,0))
            SCROLLDOWN = dinosInSpace.loadImage("fileScrollDown.png", "2X", (0,0))
            GRID_SPN_UP = dinosInSpace.loadImage("gridSpnUp.png", "2X", (0,0))
            GRID_SPN_DOWN = dinosInSpace.loadImage("gridSpnDown.png", "2X", (0,0))

            PREV_FRAME_TOP = dinosInSpace.loadImage("editPreviewTop.png", "2X", (0,0))
            PREV_FRAME_BOTTOM = dinosInSpace.loadImage("editPreviewBottom.png", "2X", (0,50))
            PREV_BKG = dinosInSpace.loadImage("editPreviewDefault.png", "2X", None)

            HELP1 = dinosInSpace.loadImage("editHelp1.png", None, (0,0))
            HELP2 = dinosInSpace.loadImage("editHelp2.png", None, (0,0))
            HELP3 = dinosInSpace.loadImage("editHelp3.png", None, (0,0))
            HELP4 = dinosInSpace.loadImage("editHelp4.png", None, (0,0))

            SPNTEST = dinosInSpace.loadImage("spnTest.png", "2X", None)
            SPN_ADD = dinosInSpace.loadImage("chexArrowUp.png", "2X", (0,0))
            SPN_SUB = dinosInSpace.loadImage("chexArrowDown.png", "2X", (0,0))
            HAMMER = dinosInSpace.loadImage("hammer.png", "2X", (0,0))

            EditorImgLib.imgDict = {

                "SAVE_BTN" : SAVE_BTN,
				"FILE_BTN_SMALL" : FILE_BTN_SMALL,
                "EXIT_BTN" : EXIT_BTN,
                "CANCEL_SURF" : CANCEL_SURF,
                "SET_SURF" : SET_SURF,
                "INVSET_SURF" : INVSET_SURF,
                "DIRECTION_TXT" : DIRECTION_TXT,
                "BAR_SURF" : BAR_SURF,
                "BAR2_SURF" : BAR2_SURF,
                "BARLONG_SURF" : BARLONG_SURF,
                "SLOT_TXT" : SLOT_TXT,
                "DINO_TXT" : DINO_TXT,
                "FLIP" : FLIP,
                "MORE" : MORE,
                "LESS" : LESS,
                "SWITCHCHAN_TXT" : SWITCHCHAN_TXT,
                "OFF_TXT" : OFF_TXT,
                "ON_TXT" : ON_TXT,
                "ERROR_FRAME_HOR" : ERROR_FRAME_HOR,
                "ERROR_FRAME_VER" : ERROR_FRAME_VER,
                "INV_TXT" : INV_TXT,
                "AMT_TXT" : AMT_TXT,
                "INV_BTN" : INV_BTN,
                "FILE_TXT" : FILE_TXT,
                "CHANNEL_TXT" : CHANNEL_TXT,
                "MAPS_TXT" : MAPS_TXT,
                "HELP_BTN" : HELP_BTN,
                "HELP_CLOSE" : HELP_CLOSE,
                "HELP_MAIN" : HELP_MAIN,
                "HELP_ENTRY" : HELP_ENTRY,
                "HELP_SWITCH" : HELP_SWITCH,
                "HELP_ERROR" : HELP_ERROR,

                "AR_G_SURF" : AR_G_SURF,
                "AR_B_SURF" : AR_B_SURF,
                "AR_R_SURF" : AR_R_SURF,
                "AR_Y_SURF" : AR_Y_SURF,
                "AR_W_SURF" : AR_W_SURF,
                "IAR_G_SURF" : IAR_G_SURF,
                "IAR_B_SURF" : IAR_B_SURF,
                "IAR_R_SURF" : IAR_R_SURF,
                "IAR_Y_SURF" : IAR_Y_SURF,
                "IAR_W_SURF" : IAR_W_SURF,
                "IHAND_SURF" : IHAND_SURF,
                "EXIT_SURF" : EXIT_SURF,
                "SPAWN_SURF" : SPAWN_SURF,
                "ISPAWN_SURF" : ISPAWN_SURF,
                "FB_G_SQUARE" : FB_G_SQUARE,
                "FB_B_SQUARE" : FB_B_SQUARE,
                "FB_R_SQUARE" : FB_R_SQUARE,
                "FB_Y_SQUARE" : FB_Y_SQUARE,
                "FB_N_SQUARE" : FB_N_SQUARE,
                "FB_SPAWNDIR" : FB_SPAWNDIR,
                "STATION_W" : STATION_W,
                "STATION_G" : STATION_G,
                "STATION_B" : STATION_B,
                "STATION_R" : STATION_R,
                "STATION_Y" : STATION_Y,
                "ISTA_W" : ISTA_W,
                "ISTA_G" : ISTA_G,
                "ISTA_B" : ISTA_B,
                "ISTA_R" : ISTA_R,
                "ISTA_Y" : ISTA_Y,
                "IROCK" : IROCK,
                "SPINNER_ADD" : SPINNER_ADD,
                "SPINNER_SUB" : SPINNER_SUB,
                "SPINNER_ADD_B" : SPINNER_ADD_B,
                "SPINNER_SUB_B": SPINNER_SUB_B,
                "SWITCH_OFF" : SWITCH_OFF,
                "SWITCH_ON" : SWITCH_ON,
                "ISWITCH" : ISWITCH,
                "LINKED_ARR_W" : LINKED_ARR_W,
                "LINKED_ARR_G" : LINKED_ARR_G,
                "LINKED_ARR_B" : LINKED_ARR_B,
                "LINKED_ARR_R" : LINKED_ARR_R,
                "LINKED_ARR_Y" : LINKED_ARR_Y,
                "LINKED_FRAME" : LINKED_FRAME,
                "ILINKED" : ILINKED,
                "ILINK_ARR_W" : ILINK_ARR_W,
                "ILINK_ARR_G" : ILINK_ARR_G,
                "ILINK_ARR_B" : ILINK_ARR_B,
                "ILINK_ARR_R" : ILINK_ARR_R,
                "ILINK_ARR_Y" : ILINK_ARR_Y,
                "ILINK_FRAME" : ILINK_FRAME,
                "FB_LINKDIR" : FB_LINKDIR,
                "INV_AR_G" : INV_AR_G,
                "INV_AR_B" : INV_AR_B,
                "INV_AR_R" : INV_AR_R,
                "INV_AR_Y" : INV_AR_Y,
                "INV_AR_W" : INV_AR_W,
                "INV_WARP" : INV_WARP,
                "SCROLLUP" : SCROLLUP,
                "SCROLLDOWN" : SCROLLDOWN,
                "GRID_SPN_DOWN" : GRID_SPN_DOWN,
                "GRID_SPN_UP" : GRID_SPN_UP,
                "PREV_FRAME_TOP" : PREV_FRAME_TOP,
                "PREV_FRAME_BOTTOM" : PREV_FRAME_BOTTOM,
                "PREV_BKG" : PREV_BKG,
                "HELP1" : HELP1,
                "HELP2" : HELP2,
                "HELP3" : HELP3,
                "HELP4" : HELP4,

                "SPNTEST" : SPNTEST,
                "SPN_ADD" : SPN_ADD,
                "SPN_SUB": SPN_SUB,
                "HAMMER" : HAMMER

            }

    @staticmethod
    def getImage(name):

        if name in EditorImgLib.imgDict:

            return EditorImgLib.imgDict[name].copy()

    def makeSomeButtons(self):

        BLACK = (0,0,0)
        WHITE = (255,255,255)
        ORANGE = (255,122,66)
        GREY = (150,150,150)
        RED = (255,0,0)
        BLUE = (0,0,255)
        WMELON = (230,101,166)
        MOONBLUE = (68,103,161)
        YELLOW = (200,200,0)

        FONTSIZE = EDIT_FONTSIZE
        V = 5
        FRAME_W, FRAME_H = (58,24)
        HELP_BW = 150
        SETTER_H = 63
        SAVE_STR_W = 300
        SAVE_STR_H = 113
        ERROR_FRAME_TOP = SAVE_STR_H - (2*FRAME_H + 3*V)

        font = dinosInSpace.FontBank.getFont(FONTSIZE, True)

        # decorator surfaces (text only) :

        DIRECTION_TXT = font.render("DIRECTION", False, BLACK)
        SLOT_TXT = font.render("SLOT", False, BLACK)
        DINO_TXT = font.render("DINO", False, BLACK)
        SWITCHCHAN_TXT = font.render("SWITCH CHANNEL", False, BLACK)
        OFF_TXT = font.render("OFF", False, BLACK)
        ON_TXT = font.render("ON", False, BLACK)
        INV_TXT = font.render("INVENTORY", False, BLACK)
        AMT_TXT = font.render("AMOUNT", False, BLACK)
        FILE_TXT = font.render("FILE", False, WHITE)
        CHANNEL_TXT = font.render("CHANNEL", False, BLACK)
        MAPS_TXT = font.render("MAPS", False, WHITE)

        # divider lines

        BAR_SURF = pygame.Surface((2,SETTER_H))
        BAR_SURF.fill(BLACK)
        BAR2_SURF = pygame.Surface((2*FRAME_W + 3*V, 2))
        BAR2_SURF.fill(BLACK)
        BARLONG_SURF = pygame.Surface((2,100))
        BARLONG_SURF.fill(BLACK)

        ERROR_FRAME_HOR = pygame.Surface((SAVE_STR_W - 2*V, 2 ))
        ERROR_FRAME_HOR.fill(BLUE)
        ERROR_FRAME_VER = pygame.Surface((2, ERROR_FRAME_TOP - 2*V ))
        ERROR_FRAME_VER.fill(BLUE)

        # text buttons

        CANCEL_SURF = self.buildTextButton("BACK", WHITE, BLACK) # text, textColor, frameColor op: w, h, fontSize
        SET_SURF = self.buildTextButton("SET", WHITE, BLACK)
        INVSET_SURF = self.buildTextButton("SET", BLACK, WHITE)
        FLIP = self.buildTextButton("FLIP", WHITE, BLACK)
        SAVE_BTN = self.buildTextButton("SAVE", WHITE, BLACK)
        FILE_BTN_SMALL = self.buildTextButton("FILE", WHITE, BLUE, 45)
        EXIT_BTN = self.buildTextButton("QUIT", WHITE, RED, 95)
        MORE = self.buildTextButton("MORE", WHITE, BLACK)
        LESS = self.buildTextButton("LESS", WHITE, BLACK)
        INV_BTN = self.buildTextButton("INV", WHITE, BLACK, 45)
        HELP_BTN = self.buildTextButton("HELP", BLUE, YELLOW)
        HELP_CLOSE = self.buildTextButton("CLOSE HELP", WHITE, BLACK, HELP_BW, 2*FRAME_H, 20)
        HELP_MAIN = self.buildTextButton("MAIN", WHITE, BLACK, HELP_BW, 2*FRAME_H, 20)
        HELP_ENTRY = self.buildTextButton("ENTRY POINTS", WHITE, BLACK, HELP_BW, 2*FRAME_H, 20)
        HELP_SWITCH = self.buildTextButton("SWITCHES", WHITE, BLACK, HELP_BW, 2*FRAME_H, 20)
        HELP_ERROR = self.buildTextButton("HINTZ", WHITE, BLACK, HELP_BW, 2*FRAME_H, 20)

        return (

            SAVE_BTN,
            FILE_BTN_SMALL,
            EXIT_BTN,
            CANCEL_SURF,
            SET_SURF,
            INVSET_SURF,
            DIRECTION_TXT,
            BAR_SURF,
            BAR2_SURF,
            BARLONG_SURF,
            SLOT_TXT,
            DINO_TXT,
            FLIP,
            MORE,
            LESS,
            SWITCHCHAN_TXT,
            OFF_TXT,
            ON_TXT,
            ERROR_FRAME_HOR,
            ERROR_FRAME_VER,
            INV_TXT,
            AMT_TXT,
            INV_BTN,
            FILE_TXT,
            CHANNEL_TXT,
            MAPS_TXT,
            HELP_BTN,
            HELP_CLOSE,
            HELP_MAIN,
            HELP_ENTRY,
            HELP_SWITCH,
            HELP_ERROR
        )

    def buildTextButton(self, text, textColor, frameColor, width=None, height=None, fontSize=None):
        FONTSIZE = 15
        FRAME_W, FRAME_H = (58,24)

        if width:
            FRAME_W = width
        if height:
            FRAME_H = height
        if fontSize:
            FONTSIZE = fontSize

        font = dinosInSpace.FontBank.getFont(FONTSIZE, True)
        frame = pygame.Surface((FRAME_W, FRAME_H))
        frame.fill(frameColor)
        textSurf = font.render(text, False, textColor)
        xOff = (FRAME_W - textSurf.get_width())/2
        yOff = (FRAME_H - textSurf.get_height())/2
        button = frame.copy()
        button.blit(textSurf, (xOff, yOff))

        return button

class Editor(object):
    """ the editor state """
    me = None

    def __init__(self, gridSize):
        self.screen = pygame.display.get_surface()
        self.editGroupL0 = pygame.sprite.RenderUpdates() # background (moving): *nothing yet
        self.editGroupL1 = pygame.sprite.RenderUpdates() # mid (moving): tiles, grid
        self.editGroupL1b = pygame.sprite.RenderUpdates() # over tiles (moving): highlight
        self.editGroupL2 = pygame.sprite.OrderedUpdates() # forground (non-moving): interface stuff
        self.cursorGroup = pygame.sprite.RenderUpdates() # the front and cursor only
        self.interfaceList = []
        self.gridSize = gridSize # for save map ref
        self.saveInputBox = None # for getInput reference (is active?)
        Editor.me = self

    @staticmethod
    def wipe():
        Editor.me = None

    @staticmethod
    def stop():
        Editor.me.keepGoing = False

    @staticmethod
    def setSaveInputBox(saveInputBox):
        Editor.me.saveInputBox = saveInputBox

    def getGridSize(self):
        return self.gridSize

    def searchGroup(self, group, objClass):
        """ takes str group tag and str obj class - returns objs in list """
        if group == "L0": group = self.editGroupL0
        elif group == "L1": group = self.editGroupL1
        elif group == "L1b": group = self.editGroupL1b
        elif group == "L2": group = self.editGroupL2
        else:
            print(group + " is not a valid group")

        foundObjs = []

        for obj in group:
            if obj.__class__ == objClass:
                foundObjs.append(obj)

        return foundObjs

    def addGroup(self, group, layer):
        if layer == 0: # background
            self.editGroupL0.add(group)
        elif layer == 1: # mid (moving)
            self.editGroupL1.add(group)
        elif layer == "1b": # over (moving)
            self.editGroupL1b.add(group)
        elif layer == 2: # forground (non-moving)
            self.editGroupL2.add(group)
        elif layer == "cursor": # front
            self.cursorGroup.add(group)

    @staticmethod
    def addSpriteToGroup(sprite):
        """currently only for adding slot colors to spawns """
        Editor.me.editGroupL1b.add(sprite)


    def addInterface(self, interface):
        self.interfaceList.append(interface)

    def removeInterface(self, interface):
        self.interfaceList.remove(interface)

    def runEditor(self, _fps, imageFrom):
        bkg = pygame.Surface(self.screen.get_size())
        bkg.fill((0,0,0))
        self.screen.blit(bkg, (0,0))

        borderWidth = 2
        borderSize = [self.screen.get_size()[0], self.screen.get_size()[1]]
        borderSize[0] -= borderWidth/2
        borderSize[1] -= borderWidth/2
        borderRect = pygame.Rect(0,0,borderSize[0],borderSize[1])

        clock = pygame.time.Clock()
        self.keepGoing = True

        while self.keepGoing:

            clock.tick(_fps)
            self.getInput()

            # L0: scrolling sublayer objects; L1: scrolling objects; L1b: scrolling over-objects; L2: non-scrolling top objects

                #self.editGroupL0.clear(screen, bkg)
            self.editGroupL1.clear(self.screen, bkg)
            self.editGroupL1b.clear(self.screen, bkg)
            self.editGroupL2.clear(self.screen, bkg)
            self.cursorGroup.clear(self.screen, bkg)
                #self.editGroupL0.update()
            self.editGroupL1.update()
            self.editGroupL1b.update()
            self.editGroupL2.update()
            self.cursorGroup.update()
                #self.editGroupL0.draw(screen)
            self.editGroupL1.draw(self.screen)
            self.editGroupL1b.draw(self.screen)
            self.editGroupL2.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            self.drawBorder(self.screen, borderRect, borderWidth)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "down")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, bkg)

        self.editGroupL1.draw(self.screen)
        self.editGroupL1b.draw(self.screen)
        self.editGroupL2.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        soundFx56.SoundPlayer.requestSound("woosh_b")
        return snapshot

    def getInput(self):

        chr = None
        for event in pygame.event.get():
            mods = pygame.key.get_mods()
            if event.type == pygame.KEYDOWN:

                # scrolling
                if event.key == pygame.K_LEFT:
                    self.scroll("L")
                elif event.key == pygame.K_RIGHT:
                    self.scroll("R")
                elif event.key == pygame.K_UP:
                    self.scroll("U")
                elif event.key == pygame.K_DOWN:
                    self.scroll("D")

                # shortcuts
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    if SaveSetter.me.onScreen:
                        SaveSetter.me.hideMe()
                    else:
                        SaveSetter.me.showMe((pygame.display.get_surface().get_width() - SaveSetter.me.rect.width, 0))
                elif (event.key == pygame.K_h) and (mods & pygame.KMOD_CTRL):
                    if HelpMain.me.onScreen:
                        HelpMain.me.hideMe()
                    else:
                        HelpMain.me.showMe((0,0))
##                elif event.key == pygame.K_ESCAPE:
##                    self.keepGoing = False
                elif (event.key == pygame.K_s) and (mods & pygame.KMOD_CTRL):
                    if not SaveSetter.me.onScreen:
                        SaveSetter.me.showMe((pygame.display.get_surface().get_width() - SaveSetter.me.rect.width, 0))
                    messageList = SaveSetter.me.shortcutFunctionKey(FB_SaveMap, True)
                    SaveSetter.me.displayMessage(messageList)

                # input key bindings
                if self.saveInputBox.active:

                    if event.key == pygame.K_BACKSPACE:
                        chr = "BACK"
                    elif event.key == pygame.K_q:
                        chr = "Q"
                    elif event.key == pygame.K_w:
                        chr = "W"
                    elif event.key == pygame.K_e:
                        chr = "E"
                    elif event.key == pygame.K_r:
                        chr = "R"
                    elif event.key == pygame.K_t:
                        chr = "T"
                    elif event.key == pygame.K_y:
                        chr = "Y"
                    elif event.key == pygame.K_u:
                        chr = "U"
                    elif event.key == pygame.K_i:
                        chr = "I"
                    elif event.key == pygame.K_o:
                        chr = "O"
                    elif event.key == pygame.K_p:
                        chr = "P"
                    elif event.key == pygame.K_a:
                        chr = "A"
                    elif event.key == pygame.K_s and not (mods & pygame.KMOD_CTRL):
                        chr = "S"
                    elif event.key == pygame.K_d:
                        chr = "D"
                    elif event.key == pygame.K_f:
                        chr = "F"
                    elif event.key == pygame.K_g:
                        chr = "G"
                    elif event.key == pygame.K_h:
                        chr = "H"
                    elif event.key == pygame.K_j:
                        chr = "J"
                    elif event.key == pygame.K_k:
                        chr = "K"
                    elif event.key == pygame.K_l:
                        chr = "L"
                    elif event.key == pygame.K_z:
                        chr = "Z"
                    elif event.key == pygame.K_x:
                        chr = "X"
                    elif event.key == pygame.K_c:
                        chr = "C"
                    elif event.key == pygame.K_v:
                        chr = "V"
                    elif event.key == pygame.K_b:
                        chr = "B"
                    elif event.key == pygame.K_n:
                        chr = "N"
                    elif event.key == pygame.K_m:
                        chr = "M"
                    elif event.key == pygame.K_1:
                        chr = "1"
                    elif event.key == pygame.K_2:
                        chr = "2"
                    elif event.key == pygame.K_3:
                        chr = "3"
                    elif event.key == pygame.K_4:
                        chr = "4"
                    elif event.key == pygame.K_5:
                        chr = "5"
                    elif event.key == pygame.K_6:
                        chr = "6"
                    elif event.key == pygame.K_7:
                        chr = "7"
                    elif event.key == pygame.K_8:
                        chr = "8"
                    elif event.key == pygame.K_9:
                        chr = "9"
                    elif event.key == pygame.K_0:
                        chr = "0"
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_SPACE:
                        chr = "_"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                EditorCursor.me.requestAction()

        if chr:
            self.saveInputBox.render(chr)

    def scroll(self, direction):
        for s in self.editGroupL0: s.move(direction)
        for s in self.editGroupL1: s.move(direction)
        for s in self.editGroupL1b: s.move(direction)

    def drawBorder(self, screen, borderRect, borderWidth):
        # suface, color, rect, width=0
        pygame.draw.rect(screen, (255,255,255), borderRect, borderWidth)

class EditorObjL1(pygame.sprite.Sprite):
    """ parent class for all scrolling, grid-based editor objects """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def move(self, direction):
        step = 50
        x = self.rect.centerx
        y = self.rect.centery

        if direction == "L":
            x += step
        elif direction == "R":
            x -= step
        elif direction == "U":
            y += step
        elif direction == "D":
            y -= step

        self.rect.centerx = x
        self.rect.centery = y

class Origin(EditorObjL1):
    """ point of reference """

    me = None

    def __init__(self):

        EditorObjL1.__init__(self)
        surf = pygame.Surface((10,10))
        surf.fill((255,255,255))
        self.image = surf
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)
        myGroup = pygame.sprite.RenderUpdates(self)
        Editor.me.addGroup(myGroup, 1)
        Origin.me = self # one ref for easy access

    @staticmethod
    def wipe():

        Origin.me = None

    @staticmethod
    def getLoc():
        """ return absolute (x, y) of origin """

        return Origin.me.rect.center

# --------------------------------------------------------- highlight

class Highlight(EditorObjL1):
    """ tile that sits under tile being set - only need 1 instance """

    me = None # access instance

    def __init__(self):

        EditorObjL1.__init__(self)
        self.frame0 = dinosInSpace.loadImage("editorOver.png", "2X", None)
        self.frame1 = dinosInSpace.loadImage("editorOver.png", "2X", (0,0))
        self.frame0.set_alpha(120, pygame.RLEACCEL)
        self.frame1.set_alpha(120, pygame.RLEACCEL)
        self.FRAMESPEED = 5
        self.frameDelay = self.FRAMESPEED
        self.image = self.frame0
        self.rect = self.image.get_rect()
        self.rect.topleft = (-1000,-1000)
        self.active = False
        Highlight.me = self
        myGroup = pygame.sprite.RenderUpdates(self)
        Editor.me.addGroup(myGroup, "1b")

    def update(self):

        if self.active:

            # animate...

            self.frameDelay -= 1

            if self.frameDelay < 0:

                # switch frames

                if self.image == self.frame0:

                    self.image = self.frame1

                elif self.image == self.frame1:

                    self.image = self.frame0

                self.frameDelay = self.FRAMESPEED

    @staticmethod
    def wipe():
        Highlight.me = None

    def slide(self, underTile):
        self.rect.topleft = underTile.rect.topleft
        self.active = True

    def hide(self):
        self.rect.topleft = (-1000,-1000)
        self.active = False

class CustomHL(pygame.sprite.Sprite):

    def __init__(self, caller, color, alphaVal=None, customSize=None):
        pygame.sprite.Sprite.__init__(self)
        self.caller = caller

        if customSize:
            self.image = pygame.Surface(customSize)
        else:
            self.image = self.caller.image.copy()

        self.image.fill(color)

        if alphaVal:
            self.image.set_alpha(alphaVal, pygame.RLEACCEL)

        self.COORDS_OFFSCREEN = (-1000,-1000)
        self.rect = self.image.get_rect()
        self.rect.center = self.COORDS_OFFSCREEN

    def showMe(self, offset=None):
        pos = [self.caller.rect.topleft[0], self.caller.rect.topleft[1]]

        if offset:
            pos[0] += offset[0]
            pos[1] += offset[1]

        self.rect.topleft = pos

    def hideMe(self):
        self.rect.center = self.COORDS_OFFSCREEN


# -------------------------------------------------------- game tiles

class EditorTile(EditorObjL1):
    """ parent class for all editor tiles """
    etGroup = None

    def __init__(self, image):
        if not EditorTile.etGroup:
            EditorTile.etGroup = pygame.sprite.RenderUpdates()

        # get pos to place tile & store coords
        grid_x, grid_y = getGridPos()
        self.COORDS = (grid_x + 1, grid_y + 1)
        pos = getAbsPos((grid_x, grid_y))

        # build tile
        EditorObjL1.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        EditorTile.etGroup.add(self)
        myGroup = pygame.sprite.GroupSingle(self)
        Editor.me.addGroup(myGroup, 1)

    @staticmethod
    def wipe():
        EditorTile.etGroup = None

    def load_init(self, coords):
        """ call imidiately after creation to recover position - may be expanded in child classes """
        self.COORDS = coords
        gridPos = (coords[0] - 1, coords[1] - 1)
        self.rect.topleft = getAbsPos(gridPos)

    def removeMe(self):
        self.kill()

    def checkOverlap(self):
        """ kills self if placed over another tile (bugfix) """
        temp_et_group = EditorTile.etGroup.copy()
        temp_et_group.remove(self)

        if pygame.sprite.spritecollideany(self, temp_et_group):
            self.kill()

class ET_sArrow(EditorTile):
    """ parent class for all sArrow editor tiles """

    def __init__(self, image):
        EditorTile.__init__(self, image)
        self.tileType = "S_ARROW"

    def load_init(self, coords, facing):
        """ adds rotation to base function """
        EditorTile.load_init(self, coords)
        if facing == "east": rotations = 1
        elif facing == "south": rotations = 2
        elif facing == "west": rotations = 3
        else: rotations = None

        if rotations:
            for i in range(rotations):
                self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, -90)

        if self.facing == "north":
            self.facing = "east"
        elif self.facing == "east":
            self.facing = "south"
        elif self.facing == "south":
            self.facing = "west"
        elif self.facing == "west":
            self.facing = "north"

class ET__AR_W(ET_sArrow):
    """ grey arrow editor tile """

    def __init__(self):
        image = EditorImgLib.getImage("AR_W_SURF")
        ET_sArrow.__init__(self, image)
        self.color = None
        self.facing = "north"

class ET__AR_G(ET_sArrow):

    def __init__(self):
        image = EditorImgLib.getImage("AR_G_SURF")
        ET_sArrow.__init__(self, image)
        self.color = "green"
        self.facing = "north"

class ET__AR_B(ET_sArrow):

    def __init__(self):
        image = EditorImgLib.getImage("AR_B_SURF")
        ET_sArrow.__init__(self, image)
        self.color = "blue"
        self.facing = "north"

class ET__AR_R(ET_sArrow):

    def __init__(self):
        image = EditorImgLib.getImage("AR_R_SURF")
        ET_sArrow.__init__(self, image)
        self.color = "red"
        self.facing = "north"

class ET__AR_Y(ET_sArrow):

    def __init__(self):
        image = EditorImgLib.getImage("AR_Y_SURF")
        ET_sArrow.__init__(self, image)
        self.color = "yellow"
        self.facing = "north"

class ET_Spawn(EditorTile):

    def __init__(self):
        image = EditorImgLib.getImage("SPAWN_SURF")
        EditorTile.__init__(self, image)
        self.originalImage = self.image.copy()
        self.tileType = "SPAWN"
        self.dinos = [] # [ direction, (color, number), (color, number) etc ]
        self.direction = "north"
        self.makeSetter()

        # make color slots
        self.slots = []
        for i in range(4):
            slot = EditorSpawnSlot(self, i + 1)
            self.slots.append(slot)
            Editor.addSpriteToGroup(slot)

    def setSlot(self, slotNumber, colorByFrame):
        """ called during FB_Set pressMe() - sets visual slot color """
        self.slots[slotNumber - 1].setColor(SLOT_COLORS[colorByFrame])


    def load_init(self, coords):
        """ adds rotation to base function """
        EditorTile.load_init(self, coords)

    def removeMe(self):
        # remove highlight and setter

        if pygame.sprite.collide_rect(self, Highlight.me):
            Highlight.me.hide()

        Editor.me.removeInterface(self.spawnSetter)

        for spr in self.spawnSetter.myGroup:
            spr.kill()

        for slot in self.slots:
            slot.kill()

        EditorTile.removeMe(self)

    def setMe(self):
        """ user requests to set start parameters for this spawn tile  """

        # hide any other setter interfaces:

        for interface in Editor.me.interfaceList:

            if interface.__class__ != TileBank:

                interface.cancel()

        # display setter

        pos = TileBank.me.getBottomLeft()
        self.spawnSetter.showMe(pos) # bring up interface
        Highlight.me.slide(self) # highlight tile

    def setDirection(self, direction):

        self.direction = direction

        if direction == "north": rot = 0
        elif direction == "east": rot = -90
        elif direction == "south": rot = 180
        elif direction == "west": rot = 90

        self.image = pygame.transform.rotate(self.originalImage, rot)

    def makeSetter(self):

        # define constants / shortcuts

        screenWidth = pygame.display.get_surface().get_width()
        LPURPLE = (174,100,214)
        PURPLE = (144,70,184)
        GREY = (170,170,170)
        BLACK = (0,0,0)
        UNIT_W = 58 # standard fx button width
        UNIT_H = 24 # standard fx button height
        V = 5 # standart unit of space b/w 24h boxes on spawnSetter

        img = EditorImgLib.getImage

        # make the spawn

        spawnSetter = SpawnSetter(self, screenWidth, 63, PURPLE, (-1000,-1000))

        spawnSetter.addFB("CANCEL", img("CANCEL_SURF"), (V,V))
        spawnSetter.addFB("SET", img("SET_SURF"), (2*V + UNIT_W,V))

        spawnSetter.addDecoration(img("DIRECTION_TXT"), (V, UNIT_H + 3*V))
        spawnDir = spawnSetter.addFB("SPAWNDIR", img("FB_SPAWNDIR"), (2*V + 80, UNIT_H + 2*V), True)
        spawnDir.activateHL()


        spawnSetter.addDecoration(img("BAR_SURF"), (2*UNIT_W + 3*V, 0))
        spawnSetter.addDecoration(img("SLOT_TXT"), (2*UNIT_W + 4*V + 2, 3*V))
        spawnSetter.addDecoration(img("DINO_TXT"), (2*UNIT_W + 4*V + 2, UNIT_H + 3*V))

        start = 2*UNIT_W + 4*V + 50
        step = 0
        count = 1
        numDino = 4
        FONTSIZE = 12
        font = dinosInSpace.FontBank.getFont(FONTSIZE, True)

        for i in range(numDino): # place color buttons and numbers

            if count < 10:

                buff = 7

            else:

                buff = 4

            num = font.render(str(count), True, BLACK)
            spawnSetter.addDecoration(num, (start + step + buff, 2*V + 2))
            spawnSetter.addFB("COLOR", img("FB_N_SQUARE"), (start + step, UNIT_H + 2*V))
            step += UNIT_H + V
            count += 1

        self.spawnSetter = spawnSetter
        self.spawnSetter.addToEditor()

class ET_Switch(EditorTile):

    switchCount = 0

    def __init__(self):

        self.imageOff = EditorImgLib.getImage("SWITCH_OFF")
        self.imageOn = EditorImgLib.getImage("SWITCH_ON")
        EditorTile.__init__(self, self.imageOff.copy())

        fontSize = LINKED_TILE_FONTSIZE
        self.font = dinosInSpace.FontBank.getFont(fontSize, True)
        self.fontColor = (0,0,0)

        self.on = False

        self.tileType = "SWITCH"
        self.makeSetter()
        self.setChannel_init()

        ET_Switch.switchCount += 1

    @staticmethod
    def wipe():

        ET_Switch.switchCount = 0

    def load_init(self, coords, channel):

        EditorTile.load_init(self, coords)
        self.setChannel(channel)
        self.updateImage()

    def updateImage(self):

        channelDisplay = self.font.render(str(self.switchChannel), True, self.fontColor)

        if self.on:

            cleanCopy = self.imageOn.copy()

        else:

            cleanCopy = self.imageOff.copy()

        cleanCopy.blit(channelDisplay, (0,0))
        self.image = cleanCopy

    def setChannel_init(self):
        """ sets switch to clean channel when first created """

        # store reserved channels

        self.switchChannel = -1
        reservedChannels = []

        for spr in Editor.me.editGroupL1:

            if hasattr(spr, "flipState") and hasattr(spr, "getChannel"):

                if spr.getChannel() not in reservedChannels:

                    reservedChannels.append(spr.getChannel())

        # find and set lowest free channel

        channel = 0
        freeChannel = None

        while not freeChannel:

            channel += 1

            if channel not in reservedChannels:

                freeChannel = channel

        self.setChannel(freeChannel)

        # sync setter's spinner

        if freeChannel > 1:

            for i in range(freeChannel -1):

                self.switchSetter.channelSpinner.spin("ADD")

        # set the setter

        for fb in self.switchSetter.fbGroup:

            if fb.__class__ == FB_Set:

                fb.pressMe()
                break

    def isOn(self):

        return self.on

    def setChannel(self, channel):

        self.switchChannel = channel

    def getChannel(self):

        return self.switchChannel

    def removeMe(self):

        # remove highlight and setter

        if pygame.sprite.collide_rect(self, Highlight.me):

            Highlight.me.hide()

        Editor.me.removeInterface(self.switchSetter)

        for spr in self.switchSetter.myGroup:

            spr.kill()

        ET_Switch.switchCount -= 1
        EditorTile.removeMe(self)

    @staticmethod
    def getCount():

        return ET_Switch.switchCount

    def setMe(self):

        # hide any other setter interfaces:

        for interface in Editor.me.interfaceList:

            if interface.__class__ != TileBank:

                interface.cancel()

        # display setter

        pos = TileBank.me.getBottomLeft()

        self.switchSetter.showMe(pos) # bring up interface
        Highlight.me.slide(self) # highlight tile

    def sendFlip(self, on_off_tog):
        """ receive request from FB_Flip - pressed by user """

        # flip linked tiles and other switches of same channel

        for spr in Editor.me.editGroupL1:

            if hasattr(spr, "flipState") and hasattr(spr, "getChannel"):

                if spr.getChannel() == self.getChannel():

                    spr.flipState(on_off_tog)

    def flipState(self, on_off_tog):
        """ receive flip request from flipped switch of matching channel """

        if on_off_tog == "on":

            self.on = True

        elif on_off_tog == "off":

            self.on = False

        elif on_off_tog == "tog":

            if self.on:

                self.on = False

            else:

                self.on = True

        self.updateImage()

    def makeSetter(self):

        # define constants / shortcuts

        screenWidth = pygame.display.get_surface().get_width()
        BISQUE = (205,183,158)
        TURQ = (0,250,154)
        WMELON = (230,101,166)
        LPURPLE = (174,100,214)
        PURPLE = (144,70,184)
        GREY = (170,170,170)
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        UNIT_W = 58 # standard fx button width
        UNIT_H = 24 # standard fx button height
        V = 5 # standard unit of space b/w 24h boxes on spawnSetter
        SETTER_LEN = 4*V + 3*UNIT_W

        img = EditorImgLib.getImage

        # make the setter and buttons

        switchSetter = SwitchSetter(self, SETTER_LEN, 63, TURQ, (-1000,-1000))
        switchSetter.addFB("CANCEL", img("CANCEL_SURF"), (V,V))
        switchSetter.addFB("SET", img("SET_SURF"), (2*V + UNIT_W,V))
        switchSetter.addFB("FLIP", img("FLIP"), (3*V + 2*UNIT_W, V))

            #topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue
        SPINNERMIN = 1
        SPINNERMAX = 50
        spinner = SwitchChannelSpinner((-1000,-1000), (UNIT_H,UNIT_H), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 1)


        decOffset = switchSetter.addDecoration(img("CHANNEL_TXT"), (V, UNIT_H + 3*V), True).image.get_width() + V


        spinnerButtonAdd = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinner, "ADD")
        spinnerButtonSub = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinner, "SUBTRACT")
        spinnerButtonAdd.setLocalCursor(EditorCursor.me)
        spinnerButtonSub.setLocalCursor(EditorCursor.me)

        switchSetter.addBasicObject(spinner, (decOffset + 2*V + UNIT_H, UNIT_H + 2*V))
        switchSetter.addBasicObject(spinnerButtonAdd, (decOffset + V, UNIT_H + 2*V), True)
        switchSetter.addBasicObject(spinnerButtonSub, (decOffset + 3*V + 2*UNIT_H, UNIT_H + 2*V), True)


        self.switchSetter = switchSetter
        self.switchSetter.addToEditor()

class ET_LinkedSet(EditorTile):

    linkedCount = 0

    def __init__(self):

        self.imageBlank = EditorImgLib.getImage("LINKED_FRAME")
        self.imageArrG = EditorImgLib.getImage("LINKED_ARR_G")
        self.imageArrB = EditorImgLib.getImage("LINKED_ARR_B")
        self.imageArrR = EditorImgLib.getImage("LINKED_ARR_R")
        self.imageArrY = EditorImgLib.getImage("LINKED_ARR_Y")
        self.imageArrW = EditorImgLib.getImage("LINKED_ARR_W")

        EditorTile.__init__(self, self.imageBlank.copy())

        self.tileType = "LINKED_TILE"
        self.makeSetter()
        self.switchChannel = 1
        self.on = False

        fontSize = 30
        self.font = dinosInSpace.FontBank.getFont(fontSize, True)
        self.fontColor = (255,255,255)

        self.colorOn = "frame" # 'green', 'blue', 'red', 'yellow', 'grey'
        self.colorOff = "frame"
        self.directionOn = "north" # 'east', south', 'west'
        self.directionOff = "north"

        self.updateImage()

        ET_LinkedSet.linkedCount += 1

    @staticmethod
    def wipe():

        ET_LinkedSet.linkedCount = 0

    def getColor(self, on_off):
        """ access for save map """

        if on_off == "on":
            return self.colorOn
        else:
            return self.colorOff

    def getDirection(self, on_off):
        """ access for save map """

        if on_off == "on":

            return self.directionOn

        else:

            return self.directionOff

    def getChannel(self):
        """ access for save map and ET_Switch """
        return self.switchChannel

    def flipState(self, on_off_tog):
        """ receive flip request from flipped switch "of matching channel """

        if on_off_tog == "on":
            self.on = True
        elif on_off_tog == "off":
            self.on = False
        elif on_off_tog == "tog":
            if self.on:
                self.on = False
            else:
                self.on = True
        self.updateImage()

    def setState(self):
        self.colorOff = self.linkedSetter.getCurrentRB("A").getColor()
        self.colorOn = self.linkedSetter.getCurrentRB("B").getColor()
        self.directionOff = self.linkedSetter.getCurrentRB("A").getDirection()
        self.directionOn = self.linkedSetter.getCurrentRB("B").getDirection()
        self.updateImage()

    def updateImage(self):
        """ pull correct image base, rotate if needed, blit channel number and set to self.image """
        # on or off?

        if self.on:
            color = self.colorOn
            direction = self.directionOn
        else:
            color = self.colorOff
            direction = self.directionOff

        # fetch base image copy
        if color != "frame":
            if color == "green":
                newImage = self.imageArrG.copy()
            elif color == "blue":
                newImage = self.imageArrB.copy()
            elif color == "red":
                newImage = self.imageArrR.copy()
            elif color == "yellow":
                newImage = self.imageArrY.copy()
            elif color == "grey":
                newImage = self.imageArrW.copy()

            # rotate if needed
            if direction == "east":
                newImage = pygame.transform.rotate(newImage, -90)
            elif direction == "south":
                newImage = pygame.transform.rotate(newImage, 180)
            elif direction == "west":
                newImage = pygame.transform.rotate(newImage, 90)

        else:
            newImage = self.imageBlank.copy()

        # render channel number and paste on image
        channelDisplay = self.font.render(str(self.switchChannel), True, self.fontColor)
        newImage.blit(channelDisplay, (0,0))
        self.image = newImage

    def setChannel(self, channel):
        self.switchChannel = channel

    def removeMe(self):
        # remove highlight and setter
        if pygame.sprite.collide_rect(self, Highlight.me):
            Highlight.me.hide()

        Editor.me.removeInterface(self.linkedSetter)
        for spr in self.linkedSetter.myGroup:
            spr.kill()

        ET_LinkedSet.linkedCount -= 1
        EditorTile.removeMe(self)

    @staticmethod
    def getCount():

        return ET_LinkedSet.linkedCount

    def setMe(self):

        # hide any other setter interfaces:

        for interface in Editor.me.interfaceList:

            if interface.__class__ != TileBank:

                interface.cancel()

        # display setter

        pos = TileBank.me.getBottomLeft()
        self.linkedSetter.showMe(pos) # bring up interface
        Highlight.me.slide(self) # highlight tile

    def flip(self, ON_OFF_TOGGLE):
        """ user click requests  """

        if ON_OFF_TOGGLE == "ON":

            self.on = True

        elif ON_OFF_TOGGLE == "OFF":

            self.on = False

        elif ON_OFF_TOGGLE == "TOGGLE":

            if self.on:

                self.on = False

            else:

                self.on = True

    def makeSetter(self):

        # SwitchChannelSpinner: topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue
        # SwitchChannelSpinnerButton: self, surf, topLeft, slave, operation
        # RB_LinkedTile: type, unit, img, pos, isFirst, controller

        # define constants / shortcuts

        screenWidth = pygame.display.get_surface().get_width()
        LPURPLE = (174,100,214)
        PURPLE = (144,70,184)
        BROWN = (199,113,64)
        GREY = (170,170,170)
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        UNIT_W = 58 # standard fx button width
        UNIT_H = 24 # standard fx button height
        V = 5 # standard unit of space b/w 24h boxes on spawnSetter

        # local constants

        U_SEL = 50
        BOTTOM = 100
        ROW2_TOP = 2*V + UNIT_H
        TB1_LEFT = 2*UNIT_W + 3*V

        img = EditorImgLib.getImage

        linkedSetter = LinkedSetter(self, screenWidth, BOTTOM, BROWN, (-1000,-1000))

        # set / cancel buttons

        linkedSetter.addFB("CANCEL", img("CANCEL_SURF"), (V,V))
        linkedSetter.addFB("SET", img("SET_SURF"), (2*V + UNIT_W,V))

        # channel select

        linkedSetter.addDecoration(img("BAR2_SURF"), (0, ROW2_TOP + 2*V))
        linkedSetter.addDecoration(img("BARLONG_SURF"), (TB1_LEFT, 0))
        linkedSetter.addDecoration(img("SWITCHCHAN_TXT"), (V, ROW2_TOP + 3*V))
        SPINNERMIN = 1
        SPINNERMAX = 50
        spinner = SwitchChannelSpinner((-1000,-1000), (UNIT_H, UNIT_H), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 1)
        spinnerButtonAdd = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinner, "ADD")
        spinnerButtonSub = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinner, "SUBTRACT")
        spinnerButtonAdd.setLocalCursor(EditorCursor.me)
        spinnerButtonSub.setLocalCursor(EditorCursor.me)
        linkedSetter.addBasicObject(spinner, (2*UNIT_H, BOTTOM - V - UNIT_H)) # (object, location, treat_as_fb = false)
        linkedSetter.addBasicObject(spinnerButtonAdd, (UNIT_H - V, BOTTOM - V - UNIT_H), True)
        linkedSetter.addBasicObject(spinnerButtonSub, (V + 3*UNIT_H, BOTTOM - V - UNIT_H), True)

        # tile selection : off unit

        offText = linkedSetter.addDecoration(img("OFF_TXT"), (V + TB1_LEFT, 4*V), True)
        x_offset = offText.image.get_width()

        TXT_WIDTH = img("DIRECTION_TXT").get_width()
        linkedSetter.addDecoration(img("DIRECTION_TXT"), (TB1_LEFT + V, U_SEL + 15))

        u1_dir = linkedSetter.addFB("LINKDIR", img("FB_LINKDIR"), (2*V + TB1_LEFT + TXT_WIDTH, U_SEL), True)
        u1_dir.activateHL()

        linkedSetter.addUnitSelect("unitTileOff", (U_SEL, U_SEL), (255,255,255)) # unitName, size, color *** unit name is hardcoded into EditorInterface class so don't change!
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_FRAME"), (x_offset +V + TB1_LEFT,0), True, "frame", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_ARR_W"), (x_offset +V + TB1_LEFT + U_SEL, 0), False, "grey", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_ARR_G"), (x_offset +V + TB1_LEFT + 2*U_SEL, 0), False, "green", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_ARR_B"), (x_offset +V + TB1_LEFT + 3*U_SEL, 0), False, "blue", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_ARR_R"), (x_offset +V + TB1_LEFT + 4*U_SEL, 0), False, "red", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOff", img("ILINK_ARR_Y"), (x_offset +V + TB1_LEFT + 5*U_SEL, 0), False, "yellow", u1_dir, True)).activateHL()

        # tile selection : on unit

        TB2_LEFT = x_offset + V + TB1_LEFT + 6*U_SEL

        linkedSetter.addDecoration(img("BARLONG_SURF"), (TB2_LEFT, 0))
        onText = linkedSetter.addDecoration(img("ON_TXT"), (V + TB2_LEFT, 4*V), True)
        x_offset = onText.image.get_width()

        linkedSetter.addDecoration(img("DIRECTION_TXT"), (TB2_LEFT + V, U_SEL + 15))

        u2_dir = linkedSetter.addFB("LINKDIR", img("FB_LINKDIR"), (2*V + TB2_LEFT + TXT_WIDTH, U_SEL), True)
        u2_dir.activateHL()
        linkedSetter.addUnitSelect("unitTileOn", (U_SEL, U_SEL), (255,255,255)) # unitName, size, color *** unit name is hardcoded into EditorInterface class so don't change!
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_FRAME"), (x_offset +V + TB2_LEFT,0), True, "frame", u1_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_ARR_W"), (x_offset +V + TB2_LEFT + U_SEL, 0), False, "grey", u2_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_ARR_G"), (x_offset +V + TB2_LEFT + 2*U_SEL, 0), False, "green", u2_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_ARR_B"), (x_offset +V + TB2_LEFT + 3*U_SEL, 0), False, "blue", u2_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_ARR_R"), (x_offset +V + TB2_LEFT + 4*U_SEL, 0), False, "red", u2_dir, True)).activateHL()
        (linkedSetter.addRB("LINKED_TILE", "unitTileOn", img("ILINK_ARR_Y"), (x_offset +V + TB2_LEFT + 5*U_SEL, 0), False, "yellow", u2_dir, True)).activateHL()

        self.linkedSetter = linkedSetter
        self.fb_dirOff = u1_dir # store for launchEditor function ref
        self.fb_dirOn = u2_dir # store for launchEditor function ref
        self.linkedSetter.addToEditor()

class ET_Station(EditorTile):

    def __init__(self, image):

        EditorTile.__init__(self, image)
        self.tileType = "STATION"

class ET_StationW(ET_Station):

    def __init__(self):

        image = EditorImgLib.getImage("STATION_W")
        ET_Station.__init__(self, image)
        self.color = None

class ET_StationG(ET_Station):

    def __init__(self):

        image = EditorImgLib.getImage("STATION_G")
        ET_Station.__init__(self, image)
        self.color = "green"

class ET_StationB(ET_Station):

    def __init__(self):

        image = EditorImgLib.getImage("STATION_B")
        ET_Station.__init__(self, image)
        self.color = "blue"

class ET_StationR(ET_Station):

    def __init__(self):

        image = EditorImgLib.getImage("STATION_R")
        ET_Station.__init__(self, image)
        self.color = "red"

class ET_StationY(ET_Station):

    def __init__(self):

        image = EditorImgLib.getImage("STATION_Y")
        ET_Station.__init__(self, image)
        self.color = "yellow"

class ET_Rock(EditorTile):

    def __init__(self):

        image = dinosInSpace.loadImage("rock2.png", "2X", (0,0))
        EditorTile.__init__(self, image)
        self.tileType = "ROCK"

# ------------------------------------------------------------------------------ interface

class EditorInterface(pygame.sprite.Sprite):
    """ parent class for editor interface objects """

    def __init__(self, w, h, color, topLeft, topRight=None):

        pygame.sprite.Sprite.__init__(self)
        self.frameW, self.frameH = w, h
        surf = pygame.Surface((w, h))
        surf.fill(color)
        self.image = surf
        self.ORIGINAL = self.image.copy()
        self.rect = self.image.get_rect()

        self.hasTopRight= False
        if not topRight:
            self.rect.topleft = topLeft
            self.screenPosition = topLeft
        else:
            self.hasTopRight = True
            self.rect.topright = topRight
            self.screenPosition = topRight

        self.BOTTOM_Y = self.rect.bottom
        self.unitDict = {} # { "unitName" : unitSelect_obj }
        self.currentRB = None
        self.myGroup = pygame.sprite.OrderedUpdates(self) # everything - to add to editor
        self.rbGroup = pygame.sprite.RenderUpdates() # exclusively for finding rb collisions
        self.fbGroup = pygame.sprite.OrderedUpdates() # for finding fb collisions and other things
        self.positionKey = {} # only used for dynamic interfaces (not TileBank)

        self.myInputBox = None  # set later
        self.onScreen = False

    def hideMe(self):
        self.onScreen = False

        for spr in self.myGroup:
            spr.rect.center = (-1000,-1000)

        if self.__class__ == SaveSetter:
            self.myInputBox.setActive(False)
        elif self.__class__ == SwitchSetter or self.__class__ == LinkedSetter:
            self.channelSpinner.setToLastValue()
        elif self.__class__ == InvSetter:
            for s in self.spinnerList:
                s.setToLastValue()

        self.onScreen = False

    def showMe(self, pos):
        """ pos topleft, all grouped items placed relative / unitSelect sync """

        # hide any other setter interfaces
        for i in Editor.me.interfaceList:
            if i.__class__ != TileBank:
                i.hideMe()
                Highlight.me.hide()

        newGroup = self.myGroup.copy()
        newGroup.remove(self)

        # remove frame and unitSelects AND inputTextCursors
        for spr in newGroup:
            if spr.__class__ == UnitSelect or spr.__class__ == textInput56.InputCursor or spr.__class__ == CustomHL:
                newGroup.remove(spr)
        if self.hasTopRight:
            self.rect.topright = pos
        else:
            self.rect.topleft = pos

        posX, posY = pos

        # place radio / function buttons
        for spr in newGroup:
            # load savedState (function buttons for now)
            if hasattr(spr, "loadState"):
                spr.loadState()
            relPosX, relPosY = self.positionKey[spr]
            myPosX = posX + relPosX
            myPosY = posY + relPosY

            if self.hasTopRight:
                spr.rect.topright = (myPosX, myPosY)
            else:
                spr.rect.topleft = (myPosX, myPosY)

        # unit select(s) for linked setter
        if self.__class__ == LinkedSetter:
            for unitName in self.unitDict:
                if unitName == "unitTileOff":
                    self.loadRB("A")
                    currentRB = self.getCurrentRB("A")
                elif unitName == "unitTileOn":
                    self.loadRB("B")
                    currentRB = self.getCurrentRB("B")
                self.unitDict[unitName].rect.center = currentRB.rect.center

        if self.__class__ == SaveSetter:
            self.myInputBox.setActive(True)

        self.onScreen = True

    def addDecoration(self, surf, pos, returnDec=False):
        """ make / link function button """
        newDecoration = Decoration(surf, pos, self)
        self.myGroup.add(newDecoration)
        self.positionKey[newDecoration] = pos

        if returnDec:
            return newDecoration

    def addInputBox(self, inputBoxData, pos):
        boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor = inputBoxData
        newInputBox = SaveFileInput(boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, 10, 0, 0, True) # nums are default values, last True tag is for getting editor font
        newInputBox.setMaster(self)
        self.myGroup.add(newInputBox)
        self.myGroup.add(newInputBox.cursor)
        newInputBox.setPosition(pos)
        self.positionKey[newInputBox] = pos
        self.myInputBox = newInputBox # for reference (activating)
        Editor.me.setSaveInputBox(newInputBox) # for Editor's reference

    def addUnitSelect(self, unitName, size, color):
        """ add a select box for radio buttons, 1 per unit """
        unitSel = UnitSelect(size, color)
        self.unitDict[unitName] = unitSel
        self.myGroup.add(unitSel)

    def addBasicObject(self, obj, pos, considerAsFB=False):
        self.myGroup.add(obj)
        self.positionKey[obj] = pos

        if obj.__class__ == SwitchChannelSpinner:
            self.channelSpinner = obj # for SwitchSetter reference
        elif obj.__class__ == InventorySpinner or obj.__class__ == WarpSpinner:
            self.spinnerList.append(obj) # for set and saveMap reference
        if considerAsFB:
            self.fbGroup.add(obj)

    def shortcutFunctionKey(self, fbClass, withReturnValues=False):
        """ shortcut to pressing a function button
            meant to be called in main input loop
        """
        for button in self.fbGroup:
            if button.__class__ == fbClass:
                if withReturnValues:
                    return button.pressMe()
                else:
                    button.pressMe()

    def addFB(self, fbType, surf, pos, returnFB=False):
        """ make / link function button """
        # choose fb type

        if fbType == "CANCEL":
            newFB = FB_Cancel(surf, pos, self)
        elif fbType == "SET":
            newFB = FB_Set(surf, pos, self)
        elif fbType == "COLOR":
            newFB = FB_SpawnColor(surf, pos, self)
        elif fbType == "SPAWNDIR":
            newFB = FB_SpawnDir(surf, pos, self)
            self.spawnDir = newFB # store so set-button has reference thru interface
        elif fbType == "SAVE":
            newFB = FB_Save(surf, pos, self)
        elif fbType == "EXIT":
            newFB = FB_Exit(surf, pos, self, (110,80,130)) # custom HL color
        elif fbType == "SAVEMAP":
            newFB = FB_SaveMap(surf, pos, self)
        elif fbType == "LINKDIR":
            newFB = FB_LinkedDir(surf, pos, self)
        elif fbType == "FLIP":
            newFB = FB_Flip(surf, pos, self)
        elif fbType == "INV":
            newFB = FB_Inventory(surf, pos, self)
        elif fbType == "HELP":
            newFB = FB_Help(surf, pos, self, (100,160,200)) # custom HL color
        elif fbType == "HELP_MAIN":
            newFB = FB_HelpMain(surf, pos, self)
        elif fbType == "HELP_ENTRY":
            newFB = FB_HelpEntry(surf, pos, self)
        elif fbType == "HELP_SWITCH":
            newFB = FB_HelpSwitch(surf, pos, self)
        elif fbType == "HELP_ERROR":
            newFB = FB_HelpError(surf, pos, self)

        self.myGroup.add(newFB)
        self.fbGroup.add(newFB)
        self.positionKey[newFB] = pos # store position for dynamic placement

        if returnFB:
            return newFB

    def addRB(self, rbType, unitName, surf, pos, isFirst=False, color=None, controller=None, returnMe=False): # last 3 for RB_LinkedTile only
        """ make / link radiobutton to unit; make unit select first """

        RB_TILES = [

            "AR_W",
            "AR_G",
            "AR_B",
            "AR_R",
            "AR_Y",
            "SPAWN",
            "STA_G",
            "STA_B",
            "STA_R",
            "STA_Y",
            "STA_W",
            "ROCK",
            "SWITCH",
            "LINKED_SET", # set of linked tiles ( in tile bank)
            "LINKED_TILE", # one linked tile itself ( in linked setter)
        ]

        if unitName not in self.unitDict:

            print("error: must create UnitSelect for this unit first")

        else:

            # choose RB type ---------------------------

            newRB = None

            if rbType in RB_TILES:

                if rbType == "LINKED_TILE":

                    newRB = RB_LinkedTile(unitName, surf, pos, self, color, controller)

                else: # build a standard tile selector

                    newRB = RB_TileSelect(rbType, unitName, surf, pos, self)

                self.myGroup.add(newRB)
                self.rbGroup.add(newRB)

            elif rbType == "RECOVER":

                newRB = RB_Recover(unitName, surf, pos, self)
                self.myGroup.add(newRB)
                self.rbGroup.add(newRB)

            elif rbType == "TEST":

                newRB = RB_TestRB(unitName, surf, pos, self)
                self.myGroup.add(newRB)
                self.rbGroup.add(newRB)

            # store position ---------------------------

            if newRB:

                self.positionKey[newRB] = pos # store position for dynamic placement

            else:

                print("rb_type not recognized")

            # if first position unitSelect under this rb and select

            if isFirst:

                self.unitDict[unitName].rect.center = newRB.rect.center

                if self.__class__ != LinkedSetter:

                    self.currentRB = newRB
                    newRB.makeFirst(unitName) # tag as first

                else:  # hardcoded for LinkedSetter

                    if unitName == "unitTileOff":

                        self.currentRB_A = newRB
                        self.saveRB("A")

                    elif unitName == "unitTileOn":

                        self.currentRB_B = newRB
                        self.saveRB("B")

        if returnMe:

            return newRB

    def setCurrentRB(self, rb):
        self.currentRB = rb

    def getCurrentRB(self):
        return self.currentRB

    def getScreenPosition(self):
        return self.screenPosition

    def cancel(self):
        self.hideMe()

    def addToEditor(self):
        Editor.me.addGroup(self.myGroup, 2)
        Editor.me.addInterface(self)

class TileBank(EditorInterface):

    me = None

    def __init__(self, w, h, color, topLeft):

        EditorInterface.__init__(self, w, h, color, topLeft)
        self.onScreen = True
        TileBank.me = self

    @staticmethod
    def wipe():

        TileBank.me = None

    def getBottomLeft(self):

        return self.rect.bottomleft

class SpawnSetter(EditorInterface):

    def __init__(self, mySpawn, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)

        self.mySpawn = mySpawn
        self.colorSlotList = []

#        # make color slots for spawn
#        for i in range(4):
#            slot = EditorSpawnSlot(self.mySpawn, i + 1)
#            # add to a group...

    def load_init(self, facing):
        if facing == "north":
            pass
        else:
            if facing == "east": cycles = 1
            elif facing == "south": cycles = 2
            elif facing == "west": cycles = 3

            for button in self.fbGroup:
                if button.__class__ == FB_SpawnDir:
                    for cycle in range(cycles):
                        button.pressMe()

class SwitchSetter(EditorInterface):

    def __init__(self, mySwitch, w, h, color, topLeft):

        EditorInterface.__init__(self, w, h, color, topLeft)
        self.mySwitch = mySwitch

class LinkedSetter(EditorInterface):

    def __init__(self, myLinkedSet, w, h, color, topLeft):

        EditorInterface.__init__(self, w, h, color, topLeft)
        self.myLinkedSet = myLinkedSet

        self.currentRB_A = None # these are used instead of self.currentRB
        self.currentRB_B = None

    def setCurrentRB(self, rb, section):

        if section == "A":
            self.currentRB_A = rb
        elif section == "B":
            self.currentRB_B = rb

    def getCurrentRB(self, section):

        if section == "A":
            return self.currentRB_A

        elif section == "B":
            return self.currentRB_B

    def saveRB(self, section):
        """ store currently selected RB - call when set is pressed """

        if section == "A":
            self.savedRB_A = self.currentRB_A

        elif section == "B":
            self.savedRB_B = self.currentRB_B

    def loadRB(self, section):
        """ load last saved RB - call when displaying interface """

        if section == "A":

            self.currentRB_A = self.savedRB_A

        elif section == "B":

            self.currentRB_B = self.savedRB_B

class SaveSetter(EditorInterface):
    me = None

    def __init__(self, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)
        SaveSetter.me = self
        self.FONTSIZE = EDIT_FONTSIZE # 15
        self.FONTCOLOR = (150,0,0)

        FRAME_W, FRAME_H = (58,24) #(58,24)
        V = 5
        SAVE_STR_W = 300
        SAVE_STR_H = 113 #113
        self.ERROR_TOPLEFT = (2*V, 2*FRAME_H + 3*V + 4)

    @staticmethod
    def wipe():
        SaveSetter.me = None

    def displayMessage(self, messageList):
        """ takes string message and builds text block """
        addHeight = 8 # add height to text box (bugfix no cut off w/ new font)
        addSpace = 4 # add space between lines in text box (bugfix...)
        textBlock = infoGraphic56.TextBlock(messageList, self.FONTSIZE, self.FONTCOLOR, addHeight, addSpace, True) # last tag editfont
        message = textBlock.image
        self.image.blit(message, self.ERROR_TOPLEFT)

    def eraseMessage(self):
        self.image.blit(self.ORIGINAL, (0,0))

    def hideMe(self):
        EditorInterface.hideMe(self)
        self.eraseMessage()
        FB_SaveMap.setFileSafety()

class InvSetter(EditorInterface):

    me = None

    def __init__(self, w, h, color, topLeft):

        EditorInterface.__init__(self, w, h, color, topLeft)
        self.spinnerList = [] # populated as spinners are added to interface
        InvSetter.me = self

    @staticmethod
    def wipe():

        InvSetter.me = None

    @staticmethod
    def getSpinners():

        return InvSetter.me.spinnerList

class HelpMain(EditorInterface):
    """ a simple interface with buttons to other interfaces with pics """
    me = None

    def __init__(self, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)
        HelpMain.me = self

    @staticmethod
    def wipe():
        HelpMain.me = None

class HelpEntry(EditorInterface):
    """ a simple interface with buttons to other interfaces with pics """
    me = None

    def __init__(self, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)
        HelpEntry.me = self

    @staticmethod
    def wipe():
        HelpEntry.me = None

class HelpSwitch(EditorInterface):
    """ a simple interface with buttons to other interfaces with pics """
    me = None

    def __init__(self, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)
        HelpSwitch.me = self

    @staticmethod
    def wipe():
        HelpSwitch.me = None

class HelpError(EditorInterface):
    """ a simple interface with buttons to other interfaces with pics """
    me = None

    def __init__(self, w, h, color, topLeft):
        EditorInterface.__init__(self, w, h, color, topLeft)
        HelpError.me = self

    @staticmethod
    def wipe():
        HelpError.me = None

class UnitSelect(pygame.sprite.Sprite):
    """ box that shows user what radiobutton is selected """

    def __init__(self, size, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.myClass = UnitSelect

    def hideMe(self):
        self.rect.center = (-1000,-1000)

# ----------------------------------------- function and radio buttons

class FunctionButton(pygame.sprite.Sprite):
    """ button that does something when clicked - linked to interface """

    def __init__(self, surf, pos, master):

        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect()
        self.posX, self.posY = pos
        self.master = master
        self.myClass = FunctionButton

        # relative formatting:

        self.rect.left = self.master.rect.left + self.posX
        self.rect.top = self.master.rect.top + self.posY

    def pressMe(self):

        pass # container for function - define in child class

class FunctionButtonHL(FunctionButton):
    """ adds mouse over highlight """

    def __init__(self, surf, pos, master, overColor=None):
        FunctionButton.__init__(self, surf, pos, master)

        self.imgOff = surf
        self.makeOverImg(overColor)

    def update(self):
        if pygame.sprite.collide_rect(self, EditorCursor.me):
            self.image = self.imgOn
        else:
            self.image = self.imgOff

    def makeOverImg(self, overColor):
        color = self.image.get_at((0,0))
        keyCol = color

        if not overColor:
            for n in range(3):
                c = color[n]
                c += 60
                if c > 255:
                    c = 255
                color[n] = c
        else:
            color = overColor

        size = self.image.get_size()
        textSurf = self.image.copy()
        textSurf.set_colorkey(keyCol, pygame.RLEACCEL)

        newSurf = pygame.Surface(size)
        newSurf.fill(color)
        newSurf.blit(textSurf, (0,0), None, pygame.BLEND_ADD)
        self.imgOn = newSurf

class FB_Inventory(FunctionButtonHL):
    me = None

    def __init__(self, surf, pos, master):
        FunctionButtonHL.__init__(self, surf, pos, master)

        self.setterPos = None
        FB_Inventory.me = self

    @staticmethod
    def wipe():
        FB_Inventory.me = None

    def pressMe(self):
        InvSetter.me.showMe(self.setterPos)

    @staticmethod
    def setSetterPos(pos):
        FB_Inventory.me.setterPos = pos

class FB_Save(FunctionButtonHL):
    """ brings up save setter """
    me = None

    def __init__(self, surf, pos, master):
        FunctionButtonHL.__init__(self, surf, pos, master)

        self.setterPos = None
        FB_Save.me = self

    @staticmethod
    def wipe():
        FB_Save.me = None

    def pressMe(self):
        SaveSetter.me.showMe(self.setterPos)

    @staticmethod
    def setSetterPos(pos):
        FB_Save.me.setterPos = pos

class FB_Help(FunctionButtonHL):
    """ brings up help menu - nested in file setter """
    me = None

    def __init__(self, surf, pos, master, overColor):
        FunctionButtonHL.__init__(self, surf, pos, master, overColor)
        self.menuPos = None
        FB_Help.me = self

    @staticmethod
    def wipe():
        FB_Help.me = None

    def pressMe(self):
        HelpMain.me.showMe(self.menuPos)

    @staticmethod
    def setMenuPos(pos):
        FB_Help.me.menuPos = pos

class FB_SaveMap(FunctionButtonHL):
    """ button on save setter that writes / saves map """
    fileSafety = True

    @staticmethod
    def setFileSafety():
        FB_SaveMap.fileSafety = True

    def pressMe(self):
        DSPEED = 6 # standard dino speed
        DSTEP = 25 # standard delay between dinos launching

        BERRY = (153, 86, 98)
        TWILIGHT = (23, 123, 159)
        MOONSTRUCK = (68, 103, 161)
        LILAC = (172, 191, 233)
        PLUM = (134, 106, 125)
        KEYLIME = (198, 227, 171)

        NON_LETTER = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_")

        self.master.eraseMessage()
        mapName = Editor.me.saveInputBox.getMapName()

        if mapName:
            if mapName[0] in NON_LETTER:
                errMsg1 = "error: file name must begin with"
                errMsg2 = "a letter"

                return [errMsg1, errMsg2]

            if dataStorage56.checkDir(mapName) and FB_SaveMap.fileSafety:
                FB_SaveMap.fileSafety = False
                errMsg1 = "warning: map with same name exists,"
                errMsg2 = "press save again to overwrite"

                return [errMsg1, errMsg2]

            FB_SaveMap.setFileSafety()
        else:

            FB_SaveMap.setFileSafety()
            errMsg1 = "error: file must be named"

            return [errMsg1]

        mapData = []
        mode = "puzzle"
        mustSave = 0
        gridSize = Editor.me.gridSize
        bkgObjData = [("star", 6, BERRY)] # override in levelXX.py
        userBlocks = []
        stations = []
        spawns = []
        sArrows = []
        linkedArrows = []
        rocks = []
        switches = []
        dinos = []
        message = None # override in levelXX.py

        spawnCount = 0
        errorMessage = None
        reservedChannels = [] # catch duplicate switches
        invSpinnerList = InvSetter.me.spinnerList

        if EditorTile.etGroup:

            for tile in EditorTile.etGroup:
                if tile.tileType == "ROCK":
                    rocks.append([tile.COORDS])
                elif tile.tileType == "STATION":
                    stations.append([tile.COORDS, tile.color])
                elif tile.tileType == "S_ARROW":
                    sArrows.append([tile.COORDS, tile.color, tile.facing])
                elif tile.tileType == "SPAWN":

                    spawns.append([tile.COORDS, tile.direction ])
                    spawnCount += 1
                    slotCount = 1
                    validSpawn = False

                    for button in tile.spawnSetter.colorSlotList: # used to be .fbGroup
                        if button.__class__ == FB_SpawnColor:
                            if button.image == button.frames[0]:
                                color = None
                            elif button.image == button.frames[1]:
                                color = "green"
                            elif button.image == button.frames[2]:
                                color = "blue"
                            elif button.image == button.frames[3]:
                                color = "red"
                            elif button.image == button.frames[4]:
                                color = "yellow"
                            if color: # only create if player chooses a color
                                # [type, num, color, speed, spawn, delayStart, delayStep]
                                dinoSet = ["delux", 1, color, DSPEED, spawnCount, slotCount * DSTEP, 0]
                                dinos.append(dinoSet)
                                mustSave += 1
                                validSpawn = True
                            slotCount += 1 # count increased regardless to control timing

                    if not validSpawn:
                        errMsg1 = "error: reported that entry point at"
                        errMsg2 = "(" + str(tile.COORDS[0]) + "," + str(tile.COORDS[1]) + ")"
                        errMsg2 += " receives no crew members"

                        return [errMsg1, errMsg2]

                elif tile.__class__ == ET_Switch:
                    if tile.getChannel() in reservedChannels: # 2 switches set to same channel
                        errMsg1 = "error: reported that switch tile at "
                        errMsg2 = "(" + str(tile.COORDS[0]) + "," + str(tile.COORDS[1]) + ")"
                        errMsg2 += " duplicates channel " + str(tile.getChannel())

                        return [errMsg1, errMsg2]

                    switches.append([tile.COORDS, tile.getChannel()])
                    reservedChannels.append(tile.getChannel())
                elif tile.__class__ == ET_LinkedSet:
                    #[ (6, 1), None, "hidden", "east", 1 ],
                    colorOff = tile.getColor("off")
                    colorOn = tile.getColor("on")
                    directionOff = tile.getDirection("off")
                    directionOn = tile.getDirection("on")
                    channel = tile.getChannel()
                    if colorOff == colorOn: # linked tile not set to change state
                        if (colorOff == "frame") or (directionOff == directionOn):
                            errMsg1 = "error: reported that linked tile at "
                            errMsg2 = "(" + str(tile.COORDS[0]) + "," + str(tile.COORDS[1]) + ")"
                            errMsg2 += " is not set to change states"

                            return [errMsg1, errMsg2]

                    if colorOff == "frame" or colorOn == "frame":
                        if colorOff == "grey":
                            colorOff = None
                        if colorOn == "grey":
                            colorOn = None

                        # construct 1 linked tile
                        if colorOff == "frame":
                            linkedArrows.append([tile.COORDS, colorOn, "hidden", directionOn, channel])
                        elif colorOn == "frame":
                            linkedArrows.append([tile.COORDS, colorOff, directionOff, "hidden", channel])
                    else:
                        # construct 2 linked tiles (to fit existing code structure)
                        if colorOff == "grey":
                            colorOff = None
                        if colorOn == "grey":
                            colorOn = None
                        linkedArrows.append( [tile.COORDS, colorOn, "hidden", directionOn, channel])
                        linkedArrows.append( [tile.COORDS, colorOff, directionOff, "hidden", channel])

        tileColor = [None, "green", "blue", "red", "yellow"]
        colorIndex = 0

        for s in invSpinnerList:
            numTiles = s.getCurrentValue()
            if numTiles > 0:
                if colorIndex < 5:
                    userBlocks.append(["arrow", tileColor[colorIndex], numTiles])
                else:
                    userBlocks.append(["warp", None, numTiles])
            colorIndex += 1

        # post catalog error checking ===================================================================

        # check if inventory is populated
        if not userBlocks:
            errMsg1 = "error: reported that inventory is"
            errMsg2 = "empty"

            return [errMsg1, errMsg2]

        # check for spawns
        if not spawns:
            errMsg1 = "error: reported that no entry"
            errMsg2 = "points exist"

            return [errMsg1, errMsg2]

        # check for stations
        if not stations:
            errMsg1 = "error: reported that no research"
            errMsg2 = "stations exist"

            return [errMsg1, errMsg2]

        # check if linked tiles have no switch
        for t in linkedArrows:
            match = False
            for s in switches:
                if s[1] == t[4]: # compare channels
                    match = True
            if not match:
                errMsg1 = "error: reported that linked tile at"
                errMsg2 = "(" + str(t[0][0]) + "," + str(t[0][1]) + ")"
                errMsg2 += " isolates channel " + str(t[4])

                return [errMsg1, errMsg2]

        # check if switch has no linked tiles
        for s in switches:
            match = False
            for t in linkedArrows:
                if t[4] == s[1]:
                    match = True
            if not match:
                errMsg1 = "error: reported that switch tile at"
                errMsg2 = "(" + str(s[0][0]) + "," + str(s[0][1]) + ")"
                errMsg2 += " isolates channel " + str(s[1])

                return [errMsg1, errMsg2]

        mapData.extend( [
            mode,
            mustSave,
            gridSize,
            bkgObjData, # override in levelXX.py
            userBlocks,
            stations,
            spawns,
            sArrows,
            linkedArrows,
            rocks,
            switches,
            dinos,
            message # override in levelXX.py
        ] )

        dataStorage56.writeMap(mapName, mapData, True) # isUserMap default false for now
        msg1 = "'" + mapName + "'"
        msg2 = "succesfully saved"

        camera = screenCap.ScreenCamera()
        camera.takePicture(pygame.display.get_surface(), mapName, "EDIT", .5) # take picture for preview
        dataStorage56.removeUserMapsEntry(mapName)

        return [msg1, msg2] # return message list -- no errors

class FB_Exit(FunctionButtonHL):
    """ exits level w/out saving """

    def pressMe(self):
        Editor.stop()

class FB_Cancel(FunctionButtonHL):

    def pressMe(self):
        self.master.cancel()
        Highlight.me.hide()

class FB_HelpMain(FunctionButtonHL):

    def pressMe(self):
        HelpMain.me.showMe((0,0))

class FB_HelpEntry(FunctionButtonHL):

    def pressMe(self):
        HelpEntry.me.showMe((0,0))

class FB_HelpSwitch(FunctionButtonHL):

    def pressMe(self):
        HelpSwitch.me.showMe((0,0))

class FB_HelpError(FunctionButtonHL):

    def pressMe(self):
        HelpError.me.showMe((0,0))

class FB_Set(FunctionButtonHL):

    def pressMe(self):
        if self.master.__class__ == SpawnSetter:
            spawnDirFB = self.master.spawnDir
            spawnTile = self.master.mySpawn
            fbGroup = self.master.fbGroup

            if spawnDirFB:
                # frame 0 = north, 1 = east, 2 = south, 3 = west
                if spawnDirFB.currentFrame == 0:
                    spawnTile.setDirection("north")
                elif spawnDirFB.currentFrame == 1:
                    spawnTile.setDirection("east")
                elif spawnDirFB.currentFrame == 2:
                    spawnTile.setDirection("south")
                elif spawnDirFB.currentFrame == 3:
                    spawnTile.setDirection("west")

            for button in fbGroup:
                if hasattr(button, "saveState"):
                    button.saveState()

                if button.__class__ == FB_SpawnColor:
                    spawnTile.setSlot(button.slotNumber, button.currentFrame) # frames [N,G,B,R,Y]



        elif self.master.__class__ == SwitchSetter:
            switch = self.master.mySwitch
            channelSpinner = self.master.channelSpinner
            fbGroup = self.master.fbGroup
            switch.setChannel(channelSpinner.getCurrentValue())
            switch.updateImage()
            channelSpinner.saveState()

            for button in fbGroup:
                if hasattr(button, "saveState"):
                    button.saveState()

            # sync with existing switches on same channel
            switches = Editor.me.searchGroup("L1", ET_Switch)
            if switches:
                switches.remove(switch)
                for s in switches:
                    if s.getChannel() == switch.getChannel():
                        if s.isOn():
                            switch.flipState("on")
                        else:
                            switch.flipState("off")
                        break

            # sync existing linked tiles on same channel with switch

            linkedTiles = Editor.me.searchGroup("L1", ET_LinkedSet)

            if linkedTiles:

                for lt in linkedTiles:

                    if lt.getChannel() == switch.getChannel():

                        if switch.isOn():

                            lt.flipState("on")

                        else:

                            lt.flipState("off")

        elif self.master.__class__ == LinkedSetter:

            linkedSet = self.master.myLinkedSet
            channelSpinner = self.master.channelSpinner
            fbGroup = self.master.fbGroup
            rbGroup = self.master.rbGroup
            linkedSet.setChannel(channelSpinner.getCurrentValue())
            channelSpinner.saveState()

            for button in fbGroup:
                if hasattr(button, "saveState"):
                    button.saveState()

            for button in rbGroup:
                if hasattr(button, "saveState"):
                    button.saveState()

            # unit selects
            self.master.saveRB("A")
            self.master.saveRB("B")

            linkedSet.setState() # set the tile itself (colors, direction)

             # sync with existing switches on same channel
            switches = Editor.me.searchGroup("L1", ET_Switch)

            if switches:
                for s in switches:
                    if s.getChannel() == linkedSet.getChannel():
                        if s.isOn():
                            linkedSet.flipState("on")
                        else:
                            linkedSet.flipState("off")
                        break

        elif self.master.__class__ == InvSetter:
            spinnerList = self.master.spinnerList
            for s in spinnerList:
                s.saveState()

        self.master.cancel()
        Highlight.me.hide()

class FB_Cycle(FunctionButton):
    """ function button that cycles through frames when clicked """

    def __init__(self, surf, pos, master):

        FunctionButton.__init__(self, surf, pos, master)
        self.frames = [] # fill in child class
        self.currentFrame = 0
        self.saveState()

    def pressMe(self):
        """ cycle through frames """

        self.currentFrame += 1

        if self.currentFrame > (len(self.frames) - 1):

            self.currentFrame = 0

        self.image = self.frames[self.currentFrame]

    def saveState(self):
        """ save frame when 'set' is pressed and when first created """

        self.savedFrame = self.currentFrame

    def loadState(self):
        """ load frame when opened from last saved state """

        self.currentFrame = self.savedFrame
        self.image = self.frames[self.currentFrame]

class FB_SpawnColor(FB_Cycle):
    """ cycle function button to choose dino color """

    def __init__(self, surf, pos, master):
        FB_Cycle.__init__(self, surf, pos, master)

        # assign slot number based on x position
        # ... super hacky don't do this again
        # position: 186, 215, 244, 273
        if pos[0] == 186: self.slotNumber = 1
        elif pos[0] == 215: self.slotNumber = 2
        elif pos[0] == 244: self.slotNumber = 3
        elif pos[0] == 273: self.slotNumber = 4


        N = EditorImgLib.getImage("FB_N_SQUARE")
        G = EditorImgLib.getImage("FB_G_SQUARE")
        B = EditorImgLib.getImage("FB_B_SQUARE")
        R = EditorImgLib.getImage("FB_R_SQUARE")
        Y = EditorImgLib.getImage("FB_Y_SQUARE")

        self.frames = [N,G,B,R,Y]
        self.image = N

        master.colorSlotList.append(self) # for saving

        size = [self.image.get_size()[0], self.image.get_size()[1]]
        size[0] += 4
        size[1] += 4
        self.offset = [-2,-2]
        self.myHL = CustomHL(self, (255,255,255), None, size)
        self.activateHL()

    def update(self):
        if pygame.sprite.collide_rect(self, EditorCursor.me):
            self.myHL.showMe(self.offset)
        else:
            self.myHL.hideMe()

    def activateHL(self):
        self.master.addBasicObject(self.myHL, (0,0))

class FB_SpawnDir(FB_Cycle):
    """ cycle function button to choose launch direction """
    # frame 0 = north, 1 = east, 2 = south, 3 = west

    def __init__(self, surf, pos, master):
        FB_Cycle.__init__(self, surf, pos, master)

        orig = EditorImgLib.getImage("FB_SPAWNDIR")
        N = orig.copy()
        E = pygame.transform.rotate(orig, -90)
        S = pygame.transform.rotate(orig, 180)
        W = pygame.transform.rotate(orig, 90)

        self.frames = [N,E,S,W]
        self.image = N
        self.myHL = CustomHL(self, (200,200,255), 100)

    def update(self):
        if pygame.sprite.collide_rect(self, EditorCursor.me):
            self.myHL.showMe()
        else:
            self.myHL.hideMe()

    def activateHL(self):
        self.master.addBasicObject(self.myHL, (0,0))

class FB_LinkedDir(FB_Cycle):

    def __init__(self, surf, pos, master):

        FB_Cycle.__init__(self, surf, pos, master)

        orig = surf
        N = orig.copy()
        E = pygame.transform.rotate(orig, -90)
        S = pygame.transform.rotate(orig, 180)
        W = pygame.transform.rotate(orig, 90)

        self.frames = [N,E,S,W]
        self.image = N
        self.members = [] # populate with radio butons to rotate

        self.myHL = CustomHL(self, (200,200,255), 100)

    def update(self):

        if pygame.sprite.collide_rect(self, EditorCursor.me):

            self.myHL.showMe()

        else:

            self.myHL.hideMe()

    def pressMe(self):
        """ go to new frame and rotate members """

        FB_Cycle.pressMe(self)

        for m in self.members:

            m.rotate(self.currentFrame)

    def addMember(self, member):
        """ add radiobutton to be controlled """

        self.members.append(member)

    def getMembers(self):
        """ return list of radiobuttons in this unit """

        return self.members

    def activateHL(self):

        self.master.addBasicObject(self.myHL, (0,0))


class FB_Flip(FunctionButtonHL):

    def pressMe(self):

        self.master.mySwitch.sendFlip("tog")

class RadioButton(pygame.sprite.Sprite):
    """ allows only one button among a set to be selected - linked to interface """

    def __init__(self, unitName, surf, pos, master):

        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect()
        self.unitName = unitName
        self.posX, self.posY = pos
        self.master = master
        self.isFirst = False

        # position relative to interface surface:

        self.rect.left = self.master.rect.left + self.posX
        self.rect.top = self.master.rect.top + self.posY

        self.myHL = CustomHL(self, (255,255,255), 100, self.image.get_size())

    def update(self):

        if pygame.sprite.collide_rect(self, EditorCursor.me):

            self.myHL.showMe()

        else:

            self.myHL.hideMe()

    def selectMe(self):

        selector = self.master.unitDict[self.unitName]
        selector.rect.center = self.rect.center

    def makeFirst(self, unitName):
        """ tag as first, for reference when moving hiding/showing """

        self.isFirst = True
        self.unitName = unitName # access to unitName if isFirst only

    def getUnitName(self):

        return self.unitName

    def activateHL(self):

        self.master.addBasicObject(self.myHL, (0,0))

class RB_Recover(RadioButton):
    """ choose to recover tiles from board """

    def __init__(self, unitName, surf, pos, master):

        RadioButton.__init__(self, unitName, surf, pos, master)
        self.myClass = RB_Recover

class RB_TileSelect(RadioButton):
    """ choose to place tiles on board """

    def __init__(self, rbType, unitName, surf, pos, master):

        RadioButton.__init__(self, unitName, surf, pos, master)
        self.myClass = RB_TileSelect

        if rbType == "AR_G":

            self.tileClass = ET__AR_G

        elif rbType == "AR_B":

            self.tileClass = ET__AR_B

        elif rbType == "AR_R":

            self.tileClass = ET__AR_R

        elif rbType == "AR_Y":

            self.tileClass = ET__AR_Y

        elif rbType == "AR_W":

            self.tileClass = ET__AR_W

        elif rbType == "SPAWN":

            self.tileClass = ET_Spawn

        elif rbType == "STA_W":

            self.tileClass = ET_StationW

        elif rbType == "STA_G":

            self.tileClass = ET_StationG

        elif rbType == "STA_B":

            self.tileClass = ET_StationB

        elif rbType == "STA_R":

            self.tileClass = ET_StationR

        elif rbType == "STA_Y":

            self.tileClass = ET_StationY

        elif rbType == "ROCK":

            self.tileClass = ET_Rock

        elif rbType == "SWITCH":

            self.tileClass = ET_Switch

        elif rbType == "LINKED_SET":

            self.tileClass = ET_LinkedSet

class RB_LinkedTile(RadioButton):

    def __init__(self, unitName, surf, pos, master, color, controller):
        """ tile selectors for linked interface, controller is rotator fb """

        RadioButton.__init__(self, unitName, surf, pos, master)

        self.color = color

        if self.color != "frame":

            self.original = self.image
            controller.addMember(self) # add self to FB_LinkedDir so the latter can call rotate
            self.currentFrame = 0
            self.saveState()
            self.direction = "north"

    def rotate(self, currentFrame):
        """ rotates radio button 90 """

        # get degrees

        if currentFrame == 0:

            deg = None

        elif currentFrame == 1:

            deg = -90

        elif currentFrame == 2:

            deg = 180

        elif currentFrame == 3:

            deg = 90

        # get image

        if deg:

            self.image = pygame.transform.rotate(self.original.copy(), deg)

        else:

            self.image = self.original.copy()

        self.currentFrame = currentFrame # set virtual attribute

    def saveState(self):
        """ save frame when 'set' is pressed and when first created """

        if self.color != "frame": # frame doesn't have currentFrame

            self.savedFrame = self.currentFrame

            # if not frame selector, save direction

            if self.color != "frame":

                if self.savedFrame == 0:

                    self.direction = "north"

                elif self.savedFrame == 1:

                    self.direction = "east"

                elif self.savedFrame == 2:

                    self.direction = "south"

                elif self.savedFrame == 3:

                    self.direction = "west"

    def loadState(self):
        """ load frame when opened from last saved state """

        if self.color != "frame": # frame doesn't rotate

            self.currentFrame = self.savedFrame
            self.rotate(self.currentFrame)

    def getColor(self):

        return self.color

    def getDirection(self):

        if self.color != "frame":

            return self.direction

        else:

            return None

class Decoration(pygame.sprite.Sprite):
    """ non - interactive surface linked to an interface """

    def __init__(self, surf, pos, master):

        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect()
        self.posX, self.posY = pos
        self.master = master
        self.myClass = Decoration

        # temporary formatting:

        self.rect.left = self.master.rect.left + self.posX
        self.rect.top = self.master.rect.top + self.posY

class EditorSpawnSlot(spriteBasic.BasicRect):
    """
        same as static56.SpawnSlot but adds color changing functionality
        - copied class instead of inherit for import bugfix
    """

    def __init__(self, spawnTile, slot):
        spriteBasic.BasicRect.__init__(self, SPAWNSLOT_SIZE, (0,0,0)) # ... + topleft, rimsize, alpha, opaque cnt
        self.spawnTile = spawnTile

        if slot == 1:
            self.distanceFromMid = (-SLOT_DISTANCE_FROM_MIDDLE, -SLOT_DISTANCE_FROM_MIDDLE)
        elif slot == 2:
            self.distanceFromMid = (SLOT_DISTANCE_FROM_MIDDLE + SLOT_RIGHT_FIX, -SLOT_DISTANCE_FROM_MIDDLE)
        elif slot == 3:
            self.distanceFromMid = (-SLOT_DISTANCE_FROM_MIDDLE, SLOT_DISTANCE_FROM_MIDDLE + SLOT_BOTTOM_FIX)
        elif slot == 4:
            self.distanceFromMid = (SLOT_DISTANCE_FROM_MIDDLE + SLOT_RIGHT_FIX, SLOT_DISTANCE_FROM_MIDDLE + SLOT_BOTTOM_FIX)

        self.hide()

    def update(self):
        self.rect.center = (
            self.spawnTile.rect.centerx + self.distanceFromMid[0],
            self.spawnTile.rect.centery + self.distanceFromMid[1]
        )

    def hide(self):
        self.image.set_alpha(0, pygame.RLEACCEL)

    def show(self):
        self.image.set_alpha(255, pygame.RLEACCEL)

    def setColor(self, color):
        if color:
            self.image.fill(color)
            self.show()
        else:
            self.hide()

    def move(self, direction):
        step = 50
        x = self.rect.centerx
        y = self.rect.centery

        if direction == "L":
            x += step
        elif direction == "R":
            x -= step
        elif direction == "U":
            y += step
        elif direction == "D":
            y -= step

        self.rect.centerx = x
        self.rect.centery = y



# ------------------------------------------------------------------------------ cursor, grid, exit

class EditorCursor(pygame.sprite.Sprite):

    imageStd = None
    imageRot = None
    imageSetter = None
    imageSetterBlack = None
    me = None

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        if not EditorCursor.imageStd:

            img = EditorImgLib.getImage

            EditorCursor.imageStd = dinosInSpace.loadImage("controlCursor.png", "2X", (21,21))
            EditorCursor.imageRot = dinosInSpace.loadImage("edit_rotate.png", "2X", (0,0))
            EditorCursor.imageSetter = img("INVSET_SURF")
            EditorCursor.imageSetterBlack = img("SET_SURF")

        self.image = EditorCursor.imageStd
        self.rect = pygame.rect.Rect((0,0,1,1))
        myGroup = pygame.sprite.GroupSingle(self)
        EditorCursor.me = self
        self.firstCycle = True

        Editor.me.addGroup(myGroup, "cursor")

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()
            if not self.checkOverET():
                self.image = EditorCursor.imageStd
        else:
            self.rect.topleft = (2000,2000)
            self.firstCycle = False

    @staticmethod
    def wipe():

        EditorCursor.me = None

    def checkOverET(self):

        selection = TileBank.me.getCurrentRB()

        if selection and selection.myClass == RB_Recover:

            return False

        for i in Editor.me.interfaceList:

            if pygame.sprite.collide_rect(self, i): # collides with an interface?

                return False

        if EditorTile.etGroup:

            tileList = pygame.sprite.spritecollide(self, EditorTile.etGroup, False)

            if tileList:

                tile = tileList[0]

                if tile.tileType == "S_ARROW":

                    self.image = EditorCursor.imageRot
                    return True

                elif tile.tileType == "SPAWN":

                    self.image = EditorCursor.imageSetter
                    return True

                elif tile.tileType == "SWITCH":

                    self.image = EditorCursor.imageSetterBlack
                    return True

                elif tile.__class__ == ET_LinkedSet:

                    self.image = EditorCursor.imageSetter
                    return True

            else:

                return False

        else:

            return False

    def requestAction(self):
        """ determine correct action upon clicking """

        if self.isInterfaceCollide():

            # if true, isInterfaceCollide will set rb or fb (see below)
            pass

        elif self.image == EditorCursor.imageRot:

            if EditorTile.etGroup:

                tileList = pygame.sprite.spritecollide(self, EditorTile.etGroup, False)

                if tileList:

                    tile = tileList[0]

                    if tile.tileType == "S_ARROW":

                        tile.rotate()

        elif self.image == EditorCursor.imageSetter or self.image == EditorCursor.imageSetterBlack:

            if EditorTile.etGroup:

                tileList = pygame.sprite.spritecollide(self, EditorTile.etGroup, False)

                if tileList:

                    tile = tileList[0]

                    if tile.tileType == "SPAWN" or tile.tileType == "SWITCH" or tile.__class__ == ET_LinkedSet:

                        tile.setMe()

        else:

            # see if a tile should be placed

            rb = TileBank.me.getCurrentRB()

            if rb and rb.myClass == RB_Recover:

                if EditorTile.etGroup:

                    s = pygame.sprite.spritecollide(self, EditorTile.etGroup, False)

                    if s:

                        s[0].removeMe()

            else:
                if (getGridPos()[0] + 1 <= Editor.me.getGridSize()[0]) and (getGridPos()[1] + 1 <= Editor.me.getGridSize()[1]):
                    if (getGridPos()[0] >= 0) and (getGridPos()[1] >= 0):
                        # place tile according to rb's assignment
                        newTile = rb.tileClass()

                        # destroy if collision (bugfix) ***
                        newTile.checkOverlap()

    def getTopInterface(self, iList):
        """ if interfaces are overlapping, return "top layer" interface """

        if len(iList) > 1:
            for i in iList:
                if i.__class__ == SaveSetter \
                or i.__class__ == HelpMain \
                or i.__class__ == HelpEntry \
                or i.__class__ == HelpSwitch \
                or i.__class__ == HelpError:
                    top = i
                    break
                else:
                    top = None

        elif len(iList) > 0:
            top = iList[0]
        else:
            top = None
        return top

    def isInterfaceCollide(self):
        """ if cursor clicks over interface, select rb and return true """

        interfaceList = []

        for i in Editor.me.interfaceList: # collides with an interface?

            if pygame.sprite.collide_rect(self, i):

                interfaceList.append(i)

        activeInterface = self.getTopInterface(interfaceList)

        if activeInterface:

            # was a radiobutton pressed?
            rb = pygame.sprite.spritecollide(self, activeInterface.rbGroup, False)

            if rb:

                rb[0].selectMe() # move unitSelect under rb

                if activeInterface.__class__ == LinkedSetter: # handle case with 2 radio buttons

                    unitName = rb[0].getUnitName()

                    if unitName == "unitTileOff":

                        selection = "A"

                    elif unitName == "unitTileOn":

                        selection = "B"

                    activeInterface.setCurrentRB(rb[0], selection)

                else:

                    activeInterface.setCurrentRB(rb[0]) # set activeInterface.currentRB

            else:

                # was a function button pressed?
                fb = pygame.sprite.spritecollide(self, activeInterface.fbGroup, False)

                if fb:

                    if fb[0].__class__ == FB_SaveMap:

                        messageList = fb[0].pressMe()
                        activeInterface.displayMessage(messageList)

                    else:

                        fb[0].pressMe() # activate function

            return True

        else:

            return False

class EditorGridLine(EditorObjL1):

    def __init__(self, size, midLeft, midTop):

        EditorObjL1.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()

        if midLeft:

            self.rect.midleft = midLeft

        elif midTop:

            self.rect.midtop = midTop

# ----------------------------------------------------- editor subclasses: inputBox

class SaveFileInput(textInput56.TextInputBox):

    def __init__(self, boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, endBuffer=10, text_offset_x=0, text_offset_y=0, editorFont=False):
        textInput56.TextInputBox.__init__(self, boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, endBuffer, text_offset_x, text_offset_y, editorFont)

    def render(self, chr):
        textInput56.TextInputBox.render(self, chr)
        FB_SaveMap.setFileSafety()

    def setMaster(self, master):
        self.master = master

    def setPosition(self, pos):
        posX, posY = pos
        self.rect.left = self.master.rect.left + posX
        self.rect.top = self.master.rect.top + posY

    def setActive(self, isActive):
        self.active = isActive

    def getMapName(self):
        return self.message

class SwitchChannelSpinner(textInput56.Spinner):
    "self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue"

    def __init__(self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue):
        textInput56.Spinner.__init__(self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue, True)
        self.lastValue = self.defaultValue

    def saveState(self):
        self.lastValue = self.currentValue

    def setToLastValue(self):
        self.currentValue = self.lastValue
        self.renderValue()

class InventorySpinner(SwitchChannelSpinner):
    """ new class name so interface can identify during addBasicObj """
    pass

class WarpSpinner(InventorySpinner):
    """ spin step 2 - warps only functional in pairs """

    def __init__(self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue):

        textInput56.Spinner.__init__(self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue, True)
        self.lastValue = self.defaultValue
        self.SPIN_STEP = 2

class SwitchChannelSpinnerButton(textInput56.SpinnerButton):
    """ self, surf, topLeft, slave, operation """
    pass






#************************************************************************************************************************************
# ------------------------------------------------------ editor setup ~~~~~~~~~~~~~~~************************************************
#************************************************************************************************************************************
#************************************************************************************************************************************
#************************************************************************************************************************************
#************************************************************************************************************************************
#************************************************************************************************************************************

class EditorSetup(object):
    """ state that runs before editor is launched """
    me = None

    def __init__(self, BOXSIZE, LBOX_TOPLEFT, RBOX_TOPLEFT, FONTSIZE):

        self.screen = pygame.display.get_surface()
        self.bkg = pygame.Surface(self.screen.get_size())
        self.bkg.fill((0,0,0))
        self.screen.blit(self.bkg, (0,0))


        self.ES_group = pygame.sprite.OrderedUpdates()
        self.FB_group = pygame.sprite.RenderUpdates()
        self.flyerGroup = pygame.sprite.RenderUpdates()
        self.cursorGroup = pygame.sprite.RenderUpdates()
        self.ynGroup = pygame.sprite.RenderUpdates()
        self.loadData = None # map data to load is stored here if requested

        # boxes to be drawn
        self.BOXSIZE = BOXSIZE
        self.LBOX_TOPLEFT = LBOX_TOPLEFT
        self.RBOX_TOPLEFT = RBOX_TOPLEFT
        self.FONTSIZE = FONTSIZE

        bttn_w = EditorImgLib.getImage("SPINNER_ADD").get_width()

        self.lbox = pygame.rect.Rect(self.LBOX_TOPLEFT, self.BOXSIZE)
        self.rbox = pygame.rect.Rect((0,self.BOXSIZE[1]), self.BOXSIZE)
        self.fileBox = pygame.rect.Rect((self.LBOX_TOPLEFT[0] + 6, self.LBOX_TOPLEFT[1] + FONTSIZE + 6), (self.BOXSIZE[0] - bttn_w - 12, self.BOXSIZE[1] - FONTSIZE - 12))

        self.shiftDown = False
        self.cannons = [] # use addCannnonList to add

        EditorSetup.me = self

    @staticmethod
    def wipe():
        EditorSetup.me = None

    @staticmethod
    def getFileBounds():
        bottom = EditorSetup.me.LBOX_TOPLEFT[1] + EditorSetup.me.FONTSIZE
        top = bottom - EditorSetup.me.FONTSIZE + EditorSetup.me.BOXSIZE[1] - 6

        return top, bottom

    @staticmethod
    def addObject(obj, group=None):
        if not group:
            EditorSetup.me.ES_group.add(obj)
        elif group == "cursor":
            EditorSetup.me.cursorGroup.add(obj)
        elif group == "yesNo":
            EditorSetup.me.ynGroup.add(obj)

    @staticmethod
    def addFB(obj):
        EditorSetup.me.FB_group.add(obj)

    @staticmethod
    def setLoadData(loadData):
        EditorSetup.me.loadData = loadData

    def runMe(self, _fps, imageFrom, swipeDirection):
        clock = pygame.time.Clock()
        dest = None

        while not dest:
            clock.tick(_fps)
            dest = self.getInput(_fps)

            for c in self.cannons:
                c.update()

            self.FB_group.clear(self.screen, self.bkg)
            self.ES_group.clear(self.screen, self.bkg)
            self.flyerGroup.clear(self.screen, self.bkg)
            self.cursorGroup.clear(self.screen, self.bkg)

            self.FB_group.update()
            self.ES_group.update()
            self.flyerGroup.update()
            self.cursorGroup.update()

            self.FB_group.draw(self.screen)
            self.ES_group.draw(self.screen)
            self.flyerGroup.draw(self.screen)
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

        self.FB_group.draw(self.screen)
        self.ES_group.draw(self.screen)
        self.flyerGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        soundFx56.SoundPlayer.requestSound("woosh_b")

        return dest, snapshot


    def runYN(self, _fps):
        """ create tween YN message / wait for user input """

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
            self.FB_group.clear(self.screen, self.bkg)
            self.ES_group.clear(self.screen, self.bkg)
            self.ynGroup.clear(self.screen, self.bkg)
            self.flyerGroup.clear(self.screen, self.bkg)

            self.ynGroup.update()

            self.FB_group.draw(self.screen)
            self.ES_group.draw(self.screen)
            self.ynGroup.draw(self.screen)
            self.flyerGroup.draw(self.screen)

            gfx56.drawBorder(self)

            pygame.display.flip()

##        self.ynGroup.clear(self.screen, self.bkg)
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dest = "_EXIT"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    dest = SetupCursor.me.checkPressed(_fps)

        return dest

    def getFlyerGroup(self):
        return self.flyerGroup

    def addCannonList(self, cList):
        for c in cList:
            self.cannons.append(c)

    def removeCannon(self, c):
        self.cannons.remove(c)


class SetupButton(pygame.sprite.Sprite):
    """ basic text button for editor setup screen """

    def __init__(self, sizeOrImage, color0_orMaskCol, color1, text, fontSize, fontColor, topLeft, myDest, textMult=None):

        pygame.sprite.Sprite.__init__(self)
        self.mouseOver = False

        if type(sizeOrImage) == tuple:
            if textMult: # can make button with multiple lines of text, textMult is list of strings
                self.makeButtonsWithMult(sizeOrImage, color0_orMaskCol, color1, textMult, fontSize, fontColor)
            else:
                self.makeButtons(sizeOrImage, color0_orMaskCol, color1, text, fontSize, fontColor)
        else:
            self.makeButtonsWithImage_putTextOnTop(sizeOrImage, color0_orMaskCol, text, fontSize, fontColor) # -- quick fix method

        self.image = self.imgOff
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft
        self.myDest = myDest

        if self.__class__ != FileButton: # use addFB to place in bkg group
            EditorSetup.me.addObject(self)

    def update(self):

        if pygame.sprite.collide_rect(self, SetupCursor.me):

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
        font = dinosInSpace.FontBank.getFont(fontSize, True)
        text = font.render(text, False, fontColor)
        textBlitX = ( size[0] - text.get_width() ) / 2
        textBlitY = ( size[1] - text.get_height() ) / 2
        self.imgOff.blit(text, (textBlitX, textBlitY))
        self.imgOn.blit(text, (textBlitX, textBlitY))

    def makeButtonsWithMult(self, size, color0, color1, textMult, fontSize, fontColor):
        """ alt button maker makes buttons with multiple lines of text """

        self.imgOff = pygame.Surface(size)
        self.imgOff.fill(color0)
        self.imgOn = pygame.Surface(size)
        self.imgOn.fill(color1)
        text = (infoGraphic56.TextBlock(textMult, fontSize, fontColor)).image
        textBlitX = ( size[0] - text.get_width() ) / 2
        textBlitY = ( size[1] - text.get_height() ) / 2
        self.imgOff.blit(text, (textBlitX, textBlitY))
        self.imgOn.blit(text, (textBlitX, textBlitY))

    def makeButtonsWithImage_putTextOnTop(self, image, maskColor, text, fontSize, fontColor):
        self.imgOff = image
        overMask = image.copy()
        overMask.fill(maskColor)
        overMask.set_alpha(70, pygame.RLEACCEL)
        self.imgOn = image.copy()
        self.imgOn.blit(overMask, (0,0))
        self.imgOn.set_colorkey(self.imgOn.get_at((0,0)), pygame.RLEACCEL)

        font = dinosInSpace.FontBank.getFont(fontSize, True)
        text = font.render(text, False, fontColor)
        textBlitX = ( image.get_width() - text.get_width() ) / 2
        textBlitY = ( image.get_height() - text.get_height() ) / 6
        self.imgOff.blit(text, (textBlitX, textBlitY))
        self.imgOn.blit(text, (textBlitX, textBlitY))


    def getDest(self):

        return self.myDest

class FileButton(SetupButton):
    """ each is a link to a user map - height must be divisible by 4 for swishing to work"""

    def __init__(self, master, size, color0, color1, colorDel, text, fontSize, fontColor, topLeft, myDest, mapData):
        SetupButton.__init__(self, size, color0, color1, text, fontSize, fontColor, topLeft, myDest)

        EditorSetup.me.addFB(self)
        self.imgDel = self.makeDel(size, colorDel, text, fontSize, fontColor)
        self.STEP = 8
        self.SWISHSTEP = 4 # height must be divisible by 4!!!!!!
        self.swishTick = 0
        self.mapData = mapData
        self.mapName = text
        self.master = master
        self.swishing = False
        self.previewImg = dataStorage56.getDynamicImage(self.mapName, "EDIT")

    def update(self): # overwrite to detect delete
        if pygame.sprite.collide_rect(self, SetupCursor.me):
            if EditorSetup.me.shiftDown:
                self.image = self.imgDel
            else:
                self.image = self.imgOn
            self.mouseOver = True
            MapPreviewImage.me.setImage(self.previewImg)
        else:
            self.image = self.imgOff
            self.mouseOver = False

        if self.swishing:
            if self.swishTick == self.rect.height:
                self.swishing = False
                self.swishTick = 0
            else:
                self.rect.top -= self.SWISHSTEP
                self.swishTick += self.SWISHSTEP

    def swish(self):
        self.swishing = True

    def getMapName(self):
        return self.mapName

    def makeDel(self, size, colorDel, text, fontSize, fontColor):
        imgDel = pygame.Surface(size)
        imgDel.fill(colorDel)
        font = dinosInSpace.FontBank.getFont(fontSize, True)
        text = font.render(text, False, fontColor)
        textBlitX = ( size[0] - text.get_width() ) / 2
        textBlitY = ( size[1] - text.get_height() ) / 2
        imgDel.blit(text, (textBlitX, textBlitY))

        return imgDel

    def move(self, direction):
        if direction == "UP":
            self.rect.centery -= self.STEP
        elif direction == "DOWN":
            self.rect.centery += self.STEP

    def erase(self):
        i = self.master.getIndex(self)
        self.kill()
        self.master.closeGap(i)


class MapPreviewFrame(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()

class MapPreviewImage(pygame.sprite.Sprite):
    me = None

    def __init__(self, defaultImg):
        pygame.sprite.Sprite.__init__(self)
        MapPreviewImage.me = self
        self.EMPTY_IMG = defaultImg
        self.image = self.EMPTY_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (600,300)

    def setImage(self, image):
        self.image = image

    def clearImage(self):
        self.image = self.EMPTY_IMG

    @staticmethod
    def wipe():
        MapPreviewImage.me = None


class FileScroller(object):
    """ generates and keeps track of files buttons """

    me = None

    def __init__(self):

        FileScroller.me = self
        self.fileButtonList = []

        self.BUTTON_W = EditorSetup.me.fileBox.width
        self.BUTTON_H = 40
        self.BUTTON_X = EditorSetup.me.fileBox.left
        self.BUTTON_Y = EditorSetup.me.fileBox.top
        self.BOTTOM = EditorSetup.me.fileBox.bottom

        self.head = None # scroller bounds
        self.tail = None

    @staticmethod
    def wipe():

        FileScroller.me = None

    def closeGap(self, index):
        if self.fileButtonList:
            for b in self.fileButtonList[index:]:
                b.swish()

    def scroll(self, direction):

        if self.fileButtonList:

            if direction == "DOWN":

                if self.head.rect.top < self.BUTTON_Y: # BUTTON_Y == top of gridbox

                    for b in self.fileButtonList:

                        b.move(direction)

            else:

                if self.tail.rect.bottom > self.BOTTOM:

                    for b in self.fileButtonList:

                        b.move(direction)

    def makeFileButtons(self):

        size = (self.BUTTON_W, self.BUTTON_H)
        color0 = (0,0,0)
        color1 = (0,0,255)
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

                    b = FileButton( self, size, color0, color1, colorDel, mapName, fontSize, fontColor, topLeft, myDest, mapData)
                    self.fileButtonList.append(b)
                    y += self.BUTTON_H

        if self.fileButtonList:

            self.head = self.fileButtonList[0]
            self.tail = self.fileButtonList[-1]

    def getIndex(self, button):

        return self.fileButtonList.index(button)


class FileScrollerButton(pygame.sprite.Sprite):
    """ button that controlls the file links (buttons) """

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

        if pygame.sprite.collide_rect(self, SetupCursor.me):

            self.mouseOver = True
            self.image = self.imgOn

        else:

            self.mouseOver = False
            self.image = self.imgOff

        if self.mouseOver:

            FileScroller.me.scroll(self.direction)

    def makeOverImg(self):

        bkgColor = (0,191,255)
        size = self.image.get_size()
        newSurf = pygame.Surface(size)
        newSurf.fill(bkgColor)
        origSurf = self.image.copy()
        newSurf.blit(origSurf, (0,0), None, pygame.BLEND_ADD)
        self.imgOn = newSurf
        self.imgOn.set_colorkey((255,255,255), pygame.RLEACCEL)

class SetupCursor(pygame.sprite.Sprite):
    image = None
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not SetupCursor.image:
            SetupCursor.image = dinosInSpace.loadImage("controlCursor.png", "2X", (21,21))

        self.image = SetupCursor.image
        self.rect = pygame.Rect((0,0,1,1))
        self.firstCycle = True

        SetupCursor.me = self

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()

            # clear map preview if not touching any fileButton
            if not self.isInFileButtonBounds() or not pygame.sprite.spritecollideany(self, EditorSetup.me.FB_group):
                MapPreviewImage.me.clearImage()
        else:
            self.rect.topleft = (2000,2000)
            self.firstCycle = False

    @staticmethod
    def wipe():
        SetupCursor.me = None

    def checkPressed(self, _fps=60):
        dest = None

        for spr in EditorSetup.me.ES_group:
            if spr.__class__ == SetupButton and spr.mouseOver:
                dest = spr.getDest()
                break
            elif spr.__class__ == GridSpinnerButton:
                if spr.mouseOver:
                    spr.pressMe()

        if not dest:
            for spr in EditorSetup.me.FB_group:
                if spr.__class__ == FileButton and spr.mouseOver:
                    if self.isInFileButtonBounds():
                        if not spr.swishing:
                            if EditorSetup.me.shiftDown:
                                makeYN()
                                if EditorSetup.me.runYN(_fps) == "y":
                                    dataStorage56.removeDynamicImage(spr.getMapName(), "EDIT")
                                    dataStorage56.removeDynamicImage(spr.getMapName(), "PLAY")
                                    dataStorage56.deleteMap(spr.getMapName())
                                    spr.erase()
                            else:
                                EditorSetup.setLoadData(spr.mapData)
                                dest = spr.getDest()
                                break

        return dest

    def isInFileButtonBounds(self):
        inBounds = False
        bounds = EditorSetup.me.getFileBounds() # top, bottom
        yPos = pygame.mouse.get_pos()[1]
        if yPos < bounds[0] and yPos > bounds[1]:
            inBounds = True
        return inBounds

class SetupTxt(pygame.sprite.Sprite):

    def __init__(self, text, fontSize, fontColor, center):

        pygame.sprite.Sprite.__init__(self)

        font = dinosInSpace.FontBank.getFont(fontSize, True)

        self.image = font.render(text, False, fontColor)
        self.rect = self.image.get_rect()
        self.rect.center = center

        EditorSetup.addObject(self)

class SetupSol(pygame.sprite.Sprite):

    def __init__(self, size, color, topLeft, width=None):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft

        if width:

            self.toRim(color, width)

        EditorSetup.me.addObject(self)

    def toRim(self, color, width):

        if color != (0,0,0):

            keyCol = (0,0,0)

        else:

            keyCol = (255,255,255)

        size = (self.image.get_width() - 2 * width, self.image.get_height() - 2 * width)

        keySurf = pygame.Surface(size)
        keySurf.fill(keyCol)
        self.image.blit(keySurf, (width, width))
        self.image.set_colorkey(keyCol, pygame.RLEACCEL)

# ~~~~~~~ setup sublcasses ~~~~~~~

class GridSpinnerButton(textInput56.SpinnerButton):
    """ adds mouseOver check to parent class """

    def __init__(self, surf, topLeft, slave, operation, specialHL=None):

        textInput56.SpinnerButton.__init__(self, surf, topLeft, slave, operation, specialHL)
        self.mouseOver = False


# ------------------------------------------------------ stand alone functions

def getGridPos():
    """ converts cursor pos to grid coord and returns """

    orgCoord_x, orgCoord_y = Origin.getLoc()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    xDist = mouse_x - orgCoord_x
    yDist = mouse_y - orgCoord_y
    grid_x = xDist // 100
    grid_y = yDist // 100

    # todo: check for oob

    return grid_x, grid_y

def getAbsPos(gridCoord):
    """ converts grid coord to absolute map position and returns """

    grid_x, grid_y = gridCoord
    relPosX = grid_x * 100
    relPosY = grid_y * 100
    orgCoord_x, orgCoord_y = Origin.getLoc()
    posX = orgCoord_x + relPosX
    posY = orgCoord_y + relPosY

    return posX, posY

def makeEditorGrid(gridSize):
    """ make editor grid and coordinates """

    gridGroup = pygame.sprite.RenderUpdates()
    coordGroup = pygame.sprite.RenderUpdates()

    gridSizeX, gridSizeY = gridSize
    w, h = (gridSizeX * 100), (gridSizeY * 100)
    xFix, yFix = 5, 10
    xBuffFix = 1
    x, y = 0, 0
    yOriginal = y

    for i in range(gridSizeY + 1):
        if i < gridSizeY:
            sCoord = stickyCoord.StickyCoord("y", i+1, (xBuffFix, y+50-yFix))
            coordGroup.add(sCoord)

        gL = EditorGridLine((w, 1), (x, y), None)
        y += 100
        gridGroup.add(gL)

    y = yOriginal

    for i in range(gridSizeX + 1):
        if i < gridSizeX:
            sCoord = stickyCoord.StickyCoord("x", i+1, (x+50-xFix, pygame.display.get_surface().get_height()))
            coordGroup.add(sCoord)

        gL = EditorGridLine((1, h), None, (x, y))
        x += 100
        gridGroup.add(gL)

    Editor.me.addGroup(gridGroup, 1)
    Editor.me.addGroup(coordGroup, "1b")

def makeInterfaces():

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    LPURPLE = (174,100,214)
    PURPLE = (144,70,184)
    GREY = (170,170,170)
    BLUE = (0,0,255)
    MOONBLUE = (68,103,161)
    WMELON = (230,101,166)

    UNIT_W = 58 # standard fx button width
    UNIT_H = 24 # standard fx button height
    FONTSIZE = 12
    CURSOR_W = 4
    V = 5 # standart unit of space b/w 24h boxes on spawnSetter

    EditorImgLib()
    img = EditorImgLib.getImage
    screenWidth = pygame.display.get_surface().get_width()
    screenHeight = pygame.display.get_surface().get_height()
    rhButton_h = 16
    rhButton_w = 45

    # tile bank, the main item select bar

    tileBank_h = 50
    tileBank = TileBank(screenWidth, tileBank_h, GREY, (0,0)) # w, h, color, topleft
    tileBank.addUnitSelect("mainUnit", (50,50), (255,255,255)) # unitName, size, color

    # rbType, unitName, image, pos, isFirst, color=None, controller=None, returnMe=False
    (tileBank.addRB("RECOVER", "mainUnit", img("IHAND_SURF"), (0,0), False, None, None, True)).activateHL()
    (tileBank.addRB("AR_W", "mainUnit", img("IAR_W_SURF"), (50,0), True, None, None, True)).activateHL()
    (tileBank.addRB("AR_G", "mainUnit", img("IAR_G_SURF"), (100,0), False, None, None, True)).activateHL()
    (tileBank.addRB("AR_B", "mainUnit", img("IAR_B_SURF"), (150,0), False, None, None, True)).activateHL()
    (tileBank.addRB("AR_R", "mainUnit", img("IAR_R_SURF"), (200,0), False, None, None, True)).activateHL()
    (tileBank.addRB("AR_Y", "mainUnit", img("IAR_Y_SURF"), (250,0), False, None, None, True)).activateHL()
    (tileBank.addRB("SPAWN", "mainUnit", img("ISPAWN_SURF"), (300,0), False, None, None, True)).activateHL()
    (tileBank.addRB("STA_W", "mainUnit", img("ISTA_W"), (350,0), False, None, None, True)).activateHL()
    (tileBank.addRB("STA_G", "mainUnit", img("ISTA_G"), (400,0), False, None, None, True)).activateHL()
    (tileBank.addRB("STA_B", "mainUnit", img("ISTA_B"), (450,0), False, None, None, True)).activateHL()
    (tileBank.addRB("STA_R", "mainUnit", img("ISTA_R"), (500,0), False, None, None, True)).activateHL()
    (tileBank.addRB("STA_Y", "mainUnit", img("ISTA_Y"), (550,0), False, None, None, True)).activateHL()
    (tileBank.addRB("ROCK", "mainUnit", img("IROCK"), (600,0), False, None, None, True)).activateHL()
    (tileBank.addRB("SWITCH", "mainUnit", img("ISWITCH"), (650,0), False, None, None, True)).activateHL()
    (tileBank.addRB("LINKED_SET", "mainUnit", img("ILINKED"), (700,0), False, None, None, True)).activateHL()

    tileBank.addFB("SAVE", img("FILE_BTN_SMALL"), (screenWidth - rhButton_w - 2, 1))
    #tileBank.addFB("EXIT", img("EXIT_BTN"), (screenWidth - rhButton_w - 2, 1 + rhButton_h))
    tileBank.addFB("INV", img("INV_BTN"), (screenWidth - rhButton_w - 2, 24))
    tileBank.addToEditor()

    # file (save) setter -- saves the map / exits editor / contains help menu

    std_setter_h = 63
    setter_w = 300
    setter_h = tileBank_h + std_setter_h
    saveSetterPos = (screenWidth - 300, 0)
    FB_Save.setSetterPos(saveSetterPos)

    saveSetter = SaveSetter(setter_w, setter_h, MOONBLUE, saveSetterPos)
    saveSetter.addFB("SAVEMAP", img("SAVE_BTN"), (  (setter_w - UNIT_W) - V, V))
    saveSetter.addFB("CANCEL", img("CANCEL_SURF"), (  (setter_w - 2*UNIT_W) - 2*V, V))
    saveSetter.addFB("HELP", img("HELP_BTN"), ((setter_w - 3*UNIT_W) - 3*V, V))
    saveSetter.addFB("EXIT", img("EXIT_BTN"), (V,V))
    saveSetter.addDecoration(img("FILE_TXT"), (V ,3*V + UNIT_H))

    edge = 10*V
    inpData = ( ( (setter_w - edge), UNIT_H + 5), BLUE, INPUT_BOX_FONTSIZE, WHITE, CURSOR_W, MOONBLUE) # boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor
    saveSetter.addInputBox( inpData, (edge - V, 2*V + UNIT_H) )

    saveSetter.addDecoration(img("ERROR_FRAME_VER"), (V, (2*UNIT_H + 3*V)))
    saveSetter.addDecoration(img("ERROR_FRAME_VER"), (setter_w - V - 2, (2*UNIT_H + 3*V)))
    saveSetter.addDecoration(img("ERROR_FRAME_HOR"), (V, (2*UNIT_H + 3*V)))
    saveSetter.addDecoration(img("ERROR_FRAME_HOR"), (V, setter_h - V - V))

    saveSetter.addToEditor()
    saveSetter.hideMe()

        # help menu (nested in file [save] setter)

##    menu_w = UNIT_W + 2*V
##    menu_h = 4*UNIT_H + 5*V
##    helpFile_w = 640
##    helpFile_h = 480
##       menu_TR = (screenWidth, tileBank_h)

    menu_w = screenWidth
    menu_h = screenHeight
    menu_color = (200,200,0)
    menu_button_w = img("HELP_CLOSE").get_width()
    mb_x1 = 0
    mb_x2 = screenWidth/5
    mb_x3 = 2*screenWidth/5
    mb_x4 = 3*screenWidth/5
    mb_x5 = 4*screenWidth/5

    FB_Help.setMenuPos((0,0)) # give help button menu position info

    helpMain = HelpMain(menu_w, menu_h, menu_color, (0,0))
    helpMain.addDecoration(img("HELP1"),(0,0))
    helpMain.addFB("CANCEL", img("HELP_CLOSE"), (mb_x1,V))
    helpMain.addFB("HELP_MAIN", img("HELP_MAIN"), (mb_x2,V))
    helpMain.addFB("HELP_ENTRY", img("HELP_ENTRY"), (mb_x3,V))
    helpMain.addFB("HELP_SWITCH", img("HELP_SWITCH"), (mb_x4,V))
    helpMain.addFB("HELP_ERROR", img("HELP_ERROR"), (mb_x5,V))
    helpMain.addToEditor()
    helpMain.hideMe()

    helpEntry = HelpEntry(menu_w, menu_h, menu_color, (0,0))
    helpEntry.addDecoration(img("HELP2"),(0,0))
    helpEntry.addFB("CANCEL", img("HELP_CLOSE"), (mb_x1,V))
    helpEntry.addFB("HELP_MAIN", img("HELP_MAIN"), (mb_x2,V))
    helpEntry.addFB("HELP_ENTRY", img("HELP_ENTRY"), (mb_x3,V))
    helpEntry.addFB("HELP_SWITCH", img("HELP_SWITCH"), (mb_x4,V))
    helpEntry.addFB("HELP_ERROR", img("HELP_ERROR"), (mb_x5,V))
    helpEntry.addToEditor()
    helpEntry.hideMe()

    helpSwitch = HelpSwitch(menu_w, menu_h, menu_color, (0,0))
    helpSwitch.addDecoration(img("HELP3"),(0,0))
    helpSwitch.addFB("CANCEL", img("HELP_CLOSE"), (mb_x1,V))
    helpSwitch.addFB("HELP_MAIN", img("HELP_MAIN"), (mb_x2,V))
    helpSwitch.addFB("HELP_ENTRY", img("HELP_ENTRY"), (mb_x3,V))
    helpSwitch.addFB("HELP_SWITCH", img("HELP_SWITCH"), (mb_x4,V))
    helpSwitch.addFB("HELP_ERROR", img("HELP_ERROR"), (mb_x5,V))
    helpSwitch.addToEditor()
    helpSwitch.hideMe()

    helpError = HelpError(menu_w, menu_h, menu_color, (0,0))
    helpError.addDecoration(img("HELP4"),(0,0))
    helpError.addFB("CANCEL", img("HELP_CLOSE"), (mb_x1,V))
    helpError.addFB("HELP_MAIN", img("HELP_MAIN"), (mb_x2,V))
    helpError.addFB("HELP_ENTRY", img("HELP_ENTRY"), (mb_x3,V))
    helpError.addFB("HELP_SWITCH", img("HELP_SWITCH"), (mb_x4,V))
    helpError.addFB("HELP_ERROR", img("HELP_ERROR"), (mb_x5,V))
    helpError.addToEditor()
    helpError.hideMe()

    # inventory setter
    inv_w = 300
    inv_h = 130
    invPos = ( pygame.display.get_surface().get_width() - inv_w, tileBank_h)
    inv_leftbound = img("INV_TXT").get_width() + 3*V
    inv_yR1 = V
    inv_yR2 = 2*V + UNIT_H
    inv_yR3 = 3*V + 2*UNIT_H
    inv_yR4 = 4*V + 3*UNIT_H
    inv_horStep = 2*V + UNIT_H
    SPINNERMIN = 0
    SPINNERMAX = 50

    FB_Inventory.setSetterPos(invPos)

    invSetter = InvSetter(inv_w, inv_h, WMELON, invPos)
    invSetter.addDecoration(img("INV_TXT"), (V, inv_yR2 + V))
    invSetter.addDecoration(img("AMT_TXT"), (V, inv_yR3 + V))
    invSetter.addDecoration(img("INV_AR_W"), (inv_leftbound, inv_yR2))
    invSetter.addDecoration(img("INV_AR_G"), (inv_leftbound + inv_horStep, inv_yR2))
    invSetter.addDecoration(img("INV_AR_B"), (inv_leftbound + 2*inv_horStep, inv_yR2))
    invSetter.addDecoration(img("INV_AR_R"), (inv_leftbound + 3*inv_horStep, inv_yR2))
    invSetter.addDecoration(img("INV_AR_Y"), (inv_leftbound + 4*inv_horStep, inv_yR2))
    invSetter.addDecoration(img("INV_WARP"), (inv_leftbound + 5*inv_horStep, inv_yR2))

    #topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue
    spinnerW = InventorySpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 0)
    spinnerG = InventorySpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 0)
    spinnerB = InventorySpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 0)
    spinnerR = InventorySpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 0)
    spinnerY = InventorySpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, SPINNERMAX, 0)
    spinnerWarp = WarpSpinner((-1000,-1000), (24,24), BLACK, 14, WHITE, SPINNERMIN, 10, 0)

    #self, surf, topLeft, slave, operation
    addW = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerW, "ADD")
    subW = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerW, "SUBTRACT")
    addG = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerG, "ADD")
    subG = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerG, "SUBTRACT")
    addB = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerB, "ADD")
    subB = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerB, "SUBTRACT")
    addR = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerR, "ADD")
    subR = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerR, "SUBTRACT")
    addY = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerY, "ADD")
    subY = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerY, "SUBTRACT")
    addWarp = SwitchChannelSpinnerButton(img("SPINNER_ADD_B"), (-1000,-1000), spinnerWarp, "ADD")
    subWarp = SwitchChannelSpinnerButton(img("SPINNER_SUB_B"), (-1000,-1000), spinnerWarp, "SUBTRACT")

    invSetter.addBasicObject(spinnerW, (inv_leftbound, inv_yR3))
    invSetter.addBasicObject(spinnerG, (inv_leftbound + inv_horStep, inv_yR3))
    invSetter.addBasicObject(spinnerB, (inv_leftbound + 2*inv_horStep, inv_yR3))
    invSetter.addBasicObject(spinnerR, (inv_leftbound + 3*inv_horStep, inv_yR3))
    invSetter.addBasicObject(spinnerY, (inv_leftbound + 4*inv_horStep, inv_yR3))
    invSetter.addBasicObject(spinnerWarp, (inv_leftbound + 5*inv_horStep, inv_yR3))

    invSetter.addBasicObject(addW, (inv_leftbound, inv_yR1), True)
    invSetter.addBasicObject(addG, (inv_leftbound + inv_horStep, inv_yR1), True)
    invSetter.addBasicObject(addB, (inv_leftbound + 2*inv_horStep, inv_yR1), True)
    invSetter.addBasicObject(addR, (inv_leftbound + 3*inv_horStep, inv_yR1), True)
    invSetter.addBasicObject(addY, (inv_leftbound + 4*inv_horStep, inv_yR1), True)
    invSetter.addBasicObject(addWarp, (inv_leftbound + 5*inv_horStep, inv_yR1), True)

    invSetter.addBasicObject(subW, (inv_leftbound, inv_yR4), True)
    invSetter.addBasicObject(subG, (inv_leftbound + inv_horStep, inv_yR4), True)
    invSetter.addBasicObject(subB, (inv_leftbound + 2*inv_horStep, inv_yR4), True)
    invSetter.addBasicObject(subR, (inv_leftbound + 3*inv_horStep, inv_yR4), True)
    invSetter.addBasicObject(subY, (inv_leftbound + 4*inv_horStep, inv_yR4), True)
    invSetter.addBasicObject(subWarp, (inv_leftbound + 5*inv_horStep, inv_yR4), True)

    invSetter.addFB("SET", img("SET_SURF"), (V, inv_yR1))
    invSetter.addFB("CANCEL", img("CANCEL_SURF"), (V, inv_yR4))

    invSetter.addToEditor()
    invSetter.hideMe()

    return (addW, subW, addG, subG, addB, subB, addR, subR, addY, subY, addWarp, subWarp)

def launchEditor(gridSize, loadData, _fps, snapshot):

    editor = Editor(gridSize)
    makeEditorGrid(gridSize)
    Origin()
    Highlight()
    spinnerButtons = makeInterfaces()
    cursor = EditorCursor()

    for bttn in spinnerButtons:

        bttn.setLocalCursor(cursor)

    if loadData:

        inventory, stations, spawns, sArrows, linkedArrows, rocks, switches, dinoSets = loadData

        if inventory:

            (spn_greyAr,
             spn_greenAr,
             spn_blueAr,
             spn_redAr,
             spn_yellowAr,
             spn_warp) = InvSetter.getSpinners()

            for tSet in inventory:

                tileType = tSet[0]
                color = tSet[1]
                num = tSet[2]

                if tileType == "arrow":

                    if not color:

                        for i in range(num):

                            spn_greyAr.spin("ADD")

                    elif color == "green":

                        for i in range(num):

                            spn_greenAr.spin("ADD")

                    elif color == "blue":

                        for i in range(num):

                            spn_blueAr.spin("ADD")

                    elif color == "red":

                        for i in range(num):

                            spn_redAr.spin("ADD")

                    elif color == "yellow":

                        for i in range(num):

                            spn_yellowAr.spin("ADD")

                elif tileType == "warp":

                    for i in range(num/2):

                        spn_warp.spin("ADD")

            for s in InvSetter.getSpinners():

                s.saveState()

        if switches:

            for s in switches:

                coords = s[0]
                channel = s[1]

                t = ET_Switch()
                t.load_init(coords, channel)

        if linkedArrows:

            tileList = [] # look for duplicates (build same tile)

            for a in linkedArrows:

                coords = a[0]
                color = a[1]
                directionOff = a[2]
                directionOn = a[3]
                channel = a[4]

                # covert object data to editor data

                if not color:
                    color = "grey"

                if directionOff == "hidden":
                    directionOff = None
                elif directionOn == "hidden":
                    directionOn = None

                sameTile = False

                for tile in tileList:
                    if tile[0] == coords:
                        sameTile = tile[1]
                        break

                # if coords have not occured, create a new tile
                if not sameTile:
                    t = ET_LinkedSet()
                    t.load_init(coords)

                # if coords have occured, this is existing tile: set 2nd state
                else:
                    t = sameTile

                # set the interface / tile -----------------------------------
                setter = t.linkedSetter

                if channel > 1:
                    t.setChannel(channel)

                    if not sameTile:
                        for c in range(channel - 1):
                            for obj in setter.myGroup:
                                if obj.__class__ == SwitchChannelSpinnerButton:
                                    if obj.operation == "ADD":
                                        obj.pressMe()

                fb_dirOff = t.fb_dirOff
                fb_dirOn = t.fb_dirOn

                for fb in setter.fbGroup:
                    if fb.__class__ == FB_Set:
                        setButton = fb
                        break

                # rotate
                if directionOff:
                    if directionOff == "east":
                        fb_dirOff.pressMe()
                    elif directionOff == "south":
                        fb_dirOff.pressMe()
                        fb_dirOff.pressMe()
                    elif directionOff == "west":
                        fb_dirOff.pressMe()
                        fb_dirOff.pressMe()
                        fb_dirOff.pressMe()

                    # not frame, so select rb that matches color
                    off_members = fb_dirOff.getMembers()
                    for m in off_members:
                        if m.getColor() == color:
                            m.selectMe()
                            setter.setCurrentRB(m, "A")

                if directionOn:
                    if directionOn == "east":
                        fb_dirOn.pressMe()
                    elif directionOn == "south":
                        fb_dirOn.pressMe()
                        fb_dirOn.pressMe()
                    elif directionOn == "west":
                        fb_dirOn.pressMe()
                        fb_dirOn.pressMe()
                        fb_dirOn.pressMe()

                    # not frame, so select rb that matches color
                    on_members = fb_dirOn.getMembers()
                    for m in on_members:
                        if m.getColor() == color:
                            m.selectMe()
                            setter.setCurrentRB(m, "B")

                if not sameTile: # add to list if not already added
                    tileList.append((coords, t))

                # press the tile's setter
                setButton.pressMe()

        if spawns: # assume there are dinoSets

            spawnCount = 0 # pull from list same order placed in

            for s in spawns:

                spawnCount += 1
                coords = s[0]
                facing = s[1]

                t = ET_Spawn()
                t.load_init(coords)

                # [TYPE='delux', NUM=1, color, SPEED, spawn, delayStart, DELAYSTEP=0]

                for s in dinoSets:

                    spawnNum = s[4]

                    if spawnNum == spawnCount:

                        delayStart = s[5]
                        setterSlot = delayStart // 25
                        color = s[2]

                        if color == "green": cycleSteps = 1
                        elif color == "blue": cycleSteps = 2
                        elif color == "red": cycleSteps = 3
                        elif color == "yellow": cycleSteps = 4

                        cycleButton = t.spawnSetter.colorSlotList[setterSlot - 1]

                        for steps in range(cycleSteps): cycleButton.pressMe()

                t.spawnSetter.load_init(facing)

                for button in t.spawnSetter.fbGroup:

                    if button.__class__ == FB_Set:

                        button.pressMe()

        if stations:

            for s in stations:

                coords = s[0]
                color = s[1]

                if color:

                    if color == "green": tile = ET_StationG
                    elif color == "blue": tile = ET_StationB
                    elif color == "red": tile = ET_StationR
                    elif color == "yellow": tile = ET_StationY

                else: tile = ET_StationW

                t = tile()
                t.load_init(coords)

        if rocks:

            for r in rocks:

                coords = r[0]
                t = ET_Rock()
                t.load_init(coords)

        if sArrows:

            for s in sArrows:

                coords = s[0]
                color = s[1]
                facing = s[2]

                if color:

                    if color == "green": tile = ET__AR_G
                    elif color == "blue": tile = ET__AR_B
                    elif color == "red": tile = ET__AR_R
                    elif color == "yellow": tile = ET__AR_Y

                else: tile = ET__AR_W

                t = tile()
                t.load_init(coords, facing)

    snapshot = editor.runEditor(_fps, snapshot)
    wipe()
    return snapshot

def launchSetup(_fps, snapshot, swipeDirection):

    EditorImgLib()
    img = EditorImgLib.getImage
    screen = pygame.display.get_surface()

    BOX_SIZE = (400, 300)
    BOX_TOP = 0
    BOX_BOTTOM = BOX_TOP + BOX_SIZE[1]
    LEFTBOX_LEFT = 0
    RIGHTBOX_LEFT = LEFTBOX_LEFT + BOX_SIZE[0]
    #RIGHTBOX_RIGHT = screen.get_width() - 100
    SET_BTTN_H = 40
    FONTSIZE = 20
    GRIDBOX_SIZE = (BOX_SIZE[0] - 16, 150)
    GRIDBOX_LEFT = 8
    GRIDBOX_TOP = BOX_BOTTOM + SET_BTTN_H
    GRIDBOX_BOTTOM = GRIDBOX_TOP + GRIDBOX_SIZE[1]
    GRIDBOX_YMID = GRIDBOX_TOP + GRIDBOX_SIZE[1]/2
    sbu_w = img("SPINNER_ADD").get_width() # scroll button width

    editorSetup = EditorSetup(BOX_SIZE, (LEFTBOX_LEFT, BOX_TOP), (RIGHTBOX_LEFT, BOX_TOP), FONTSIZE)

    SetupSol((BOX_SIZE[0], BOX_TOP + FONTSIZE + 6), (0,0,0), (LEFTBOX_LEFT, 0)) # file hider top
    SetupSol((BOX_SIZE[0], 500), (0,0,0), (LEFTBOX_LEFT, BOX_BOTTOM - 6)) # file hider bottom
    SetupSol(GRIDBOX_SIZE, (0,255,0), (GRIDBOX_LEFT, GRIDBOX_TOP), 2) # gridbox
    SetupSol(BOX_SIZE, (255,255,255), (0,0), 2) # quarter box top left
    ## moved after exit button: SetupSol(BOX_SIZE, (255,255,255), (0,BOX_SIZE[1]), 2) # quarter box bottom left
    SetupSol((BOX_SIZE[0] - sbu_w - 12, BOX_SIZE[1] - FONTSIZE - 12), (0,255,0), (LEFTBOX_LEFT + 6, BOX_TOP + FONTSIZE + 6), 2) # fileBox


    #self.fileBox = pygame.rect.Rect((self.LBOX_TOPLEFT[0] + 6, self.LBOX_TOPLEFT[1] + FONTSIZE + 6), (self.BOXSIZE[0] - bttn_w - 12, self.BOXSIZE[1] - FONTSIZE - 12))

##    SPN_TOPLEFT = (GRIDBOX_LEFT + 5, GRIDBOX_TOP + 5)
##
##    SPN_RIGHTCOL = SPN_TOPLEFT[0] +
##    SPN_BOXSIZE = (40,40)
##    SPN_BOXCOL = (0,0,0)
##    SPN_FONTSIZE = 30
##    SPN_NUMCOL = (255,255,255)

    SPN_LEFTCOL = GRIDBOX_LEFT + (GRIDBOX_SIZE[0])/5
    SPN_RIGHTCOL = GRIDBOX_LEFT + 2*(GRIDBOX_SIZE[0])/5 + 10
    SPN_BOXSIZE = (40,40)
    SPN_BOXCOL = (0,0,0)
    SPN_FONTSIZE = 30
    SPN_NUMCOL = (255,255,255)

    build_x = SPN_RIGHTCOL + SPN_BOXSIZE[0]/2 + 3

    buildFix_x = 15
    buildFix_y = 15
    SetupButton(img("HAMMER"), (230,230,255), None, "BUILD NEW", STD_FONTSIZE, (0,0,0), (build_x + buildFix_x, GRIDBOX_TOP + buildFix_y), "BUILD")
    SetupButton((BOX_SIZE[0], SET_BTTN_H), GREY, (0,0,255), "BACK", STD_FONTSIZE, (0,0,0), (LEFTBOX_LEFT, screen.get_height() - SET_BTTN_H), "_EXIT")
    SetupSol(BOX_SIZE, (255,255,255), (0,BOX_SIZE[1]), 2) # quarter box bottom left

    # decorations
    SetupTxt( "Edit Existing Map:", FONTSIZE, (0,255,0), (LEFTBOX_LEFT + BOX_SIZE[0]/2, BOX_TOP + (FONTSIZE)/2 + 4) )
    SetupTxt( "New Map Size:", FONTSIZE, (0,255,0), (BOX_SIZE[0]/2, BOX_BOTTOM + (FONTSIZE)/2 + 12) )
    SetupTxt( "Delete Map: Hold", FONTSIZE, (255,0,0), (BOX_SIZE[0]/2, screen.get_height() - SET_BTTN_H - 3*FONTSIZE + 15) )
    SetupTxt( "'CTRL' while selecting", FONTSIZE, (255,0,0), (BOX_SIZE[0]/2, screen.get_height() - SET_BTTN_H - FONTSIZE) )

    # spinner:
    xGridMin = X_GRIDMIN
    yGridMin = Y_GRIDMIN
    xGridMax = X_GRIDMAX
    yGridMax = Y_GRIDMAX
    xDefault = 8
    yDefault = 6

    #       (topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue)
    SetupTxt( "X:", COORDPAIR_FONTSIZE, (0,255,0), (SPN_LEFTCOL - SPN_BOXSIZE[0]/2 - 10, GRIDBOX_YMID))
    SetupTxt( "Y:", COORDPAIR_FONTSIZE, (0,255,0), (SPN_RIGHTCOL - SPN_BOXSIZE[0]/2 - 10, GRIDBOX_YMID))

#    for i in range(10):
#
#        SetupSol((2, GRIDBOX_SIZE[1]), (0,255,0), (xPos, GRIDBOX_TOP))
#        xPos += step

    spinner_x = textInput56.Spinner( (SPN_LEFTCOL - SPN_BOXSIZE[0]/2, GRIDBOX_YMID - SPN_BOXSIZE[1]/2), SPN_BOXSIZE, SPN_BOXCOL, COORDPAIR_FONTSIZE, SPN_NUMCOL, xGridMin, xGridMax, xDefault, True) # last tag editorfont
    spinner_y = textInput56.Spinner( (SPN_RIGHTCOL - SPN_BOXSIZE[0]/2, GRIDBOX_YMID - SPN_BOXSIZE[1]/2), SPN_BOXSIZE, SPN_BOXCOL, COORDPAIR_FONTSIZE, SPN_NUMCOL, yGridMin, yGridMax, yDefault, True)
    EditorSetup.me.addObject(spinner_x)  # manually add these for now (not based off of setup button class)
    EditorSetup.me.addObject(spinner_y)

    # spinner button: (surf, topLeft, slave, operation ['ADD' or 'SUBTRACT'])
    changeFix_x = 29
    changeFix_y = 16

    addButton_x = GridSpinnerButton( img("SPN_ADD"), (SPN_LEFTCOL - SPN_BOXSIZE[0] - changeFix_x, GRIDBOX_TOP + 20 - changeFix_y), spinner_x, "ADD", True )
    subButton_x = GridSpinnerButton( img("SPN_SUB"), (SPN_LEFTCOL - SPN_BOXSIZE[0] - changeFix_x, GRIDBOX_BOTTOM - sbu_w - 20 - changeFix_y), spinner_x, "SUBTRACT", True )
    addButton_y = GridSpinnerButton( img("SPN_ADD"), (SPN_RIGHTCOL - SPN_BOXSIZE[0] - changeFix_x, GRIDBOX_TOP + 20 - changeFix_y), spinner_y, "ADD", True )
    subButton_y = GridSpinnerButton( img("SPN_SUB"), (SPN_RIGHTCOL - SPN_BOXSIZE[0] - changeFix_x, GRIDBOX_BOTTOM - sbu_w - 20 - changeFix_y), spinner_y, "SUBTRACT", True )
    EditorSetup.me.addObject(addButton_x) # manually add these for now (not based off of setup button class)
    EditorSetup.me.addObject(subButton_x)
    EditorSetup.me.addObject(addButton_y)
    EditorSetup.me.addObject(subButton_y)

    fileScroller = FileScroller()
    fileScroller.makeFileButtons()

    SCROLLBTN_H = img("SCROLLUP").get_height()

    scrollButtonUp = FileScrollerButton(img("SCROLLUP"), (RIGHTBOX_LEFT - sbu_w - 3, BOX_TOP + FONTSIZE + 7), "DOWN")
    scrollButtonDown = FileScrollerButton(img("SCROLLDOWN"), (RIGHTBOX_LEFT - sbu_w - 3, BOX_BOTTOM - SCROLLBTN_H - 6), "UP")
    EditorSetup.me.addObject(scrollButtonUp)
    EditorSetup.me.addObject(scrollButtonDown)

    # map preview stuff
    mapPreviewImage = MapPreviewImage(img("PREV_BKG"))
    prevFrameTop = MapPreviewFrame(img("PREV_FRAME_TOP"))
    prevFrameBottom = MapPreviewFrame(img("PREV_FRAME_BOTTOM"))
    prevFrameTop.rect.bottomleft = (mapPreviewImage.rect.left, mapPreviewImage.rect.top - 1)
    prevFrameBottom.rect.topleft = (mapPreviewImage.rect.left, mapPreviewImage.rect.bottom + 1)
    EditorSetup.me.addObject(mapPreviewImage)
    EditorSetup.me.addObject(prevFrameTop)
    EditorSetup.me.addObject(prevFrameBottom)

    # cannons
    # group, flyers, pos=D_POS, step=D_STEP, var=D_STEPVAR, speed=D_FLSPEED, spin=D_FLSPIN, edge=D_FLEDGE, customBound=None, terminal=False
    bullet = pygame.Surface((4,4)); bullet.fill((0,0,255))
    bulletVariation = 0
    bulletSpin = 0

    if _fps == 60:
        bulletSpd = 2
        bulletStep = 10
        fpsFix = 1
    elif _fps == 30:
        bulletSpd = 4
        bulletStep = 5
        fpsFix = 2

    topCannon = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400,115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572)
    topCannonT1 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 2*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT2 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 4*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT3 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 6*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT4 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 8*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT5 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 10*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT6 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 12*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)
    topCannonT7 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 14*bulletStep*fpsFix, 115), bulletStep, bulletVariation, (bulletSpd, 0), bulletSpin, "R", 572, True)

    bottomCannon = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 17*bulletStep*fpsFix,485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404)
    bottomCannonT1 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT2 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 3*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT3 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 5*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT4 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 7*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT5 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 9*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT6 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 11*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT7 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 13*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)
    bottomCannonT8 = cannon.Cannon(EditorSetup.me.getFlyerGroup(), [bullet], (400 + 15*bulletStep*fpsFix, 485), bulletStep, bulletVariation, (-bulletSpd, 0), bulletSpin, "L", 404, True)

    editorSetup.addCannonList([topCannon,
                                topCannonT1,
                                topCannonT2,
                                topCannonT3,
                                topCannonT4,
                                topCannonT5,
                                topCannonT6,
                                topCannonT7,
                                bottomCannon,
                                bottomCannonT1,
                                bottomCannonT2,
                                bottomCannonT3,
                                bottomCannonT4,
                                bottomCannonT5,
                                bottomCannonT6,
                                bottomCannonT7,
                                bottomCannonT8])

    # cursor
    cursor = SetupCursor()
    editorSetup.addObject(cursor, "cursor")

    addButton_x.setLocalCursor(cursor)
    subButton_x.setLocalCursor(cursor)
    addButton_y.setLocalCursor(cursor)
    subButton_y.setLocalCursor(cursor)

    dest, snapshot = editorSetup.runMe(_fps, snapshot, swipeDirection)
    goTo = ""

    if dest == "BUILD":
        grid_x = spinner_x.getCurrentValue()
        grid_y = spinner_y.getCurrentValue()
        snapshot = launchEditor((grid_x, grid_y), None, _fps, snapshot)

    elif dest == "LOAD":
        (mode,
        mustSave,
        gridSize,
        bkgObjData,
        userBlocks,
        goals,
        spawns,
        sArrows,
        linkedArrows,
        mines,
        switches,
        dinoSets,
        message) = EditorSetup.me.loadData

        grid_x, grid_y = gridSize
        loadData = (userBlocks, goals, spawns, sArrows, linkedArrows, mines, switches, dinoSets)
        snapshot = launchEditor((grid_x, grid_y), loadData, _fps, snapshot)

    elif dest == "_EXIT":
        goTo = "_EXIT"

    setupWipe()
    return goTo, snapshot

def makeYN():
    ynSize      = (400,200)
    ynColor     = (255,0,0)
    ynFontSize  = 30
    ynFontColor = (255,255,255)
    alpha       = 180
    ynMenu      = tween.TweenYN(ynSize, ynColor, ynFontSize, ynFontColor, alpha)

    EditorSetup.addObject(ynMenu, "yesNo")


def wipe():

    Editor.wipe()
    EditorTile.wipe()
    TileBank.wipe()
    Origin.wipe()
    EditorCursor.wipe()
    SaveSetter.wipe()
    ET_Switch.wipe()
    Highlight.wipe()
    InvSetter.wipe()
    HelpMain.wipe()
    FB_Inventory.wipe()
    FB_Save.wipe()
    FB_Help.wipe()

def setupWipe():

    EditorSetup.wipe()
    SetupCursor.wipe()
    FileScroller.wipe()
    MapPreviewImage.wipe()