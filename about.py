"""
    options.py
    options screen
"""
import pygame
import dinosInSpace
import fpsSwitch
import button
import gfx56
import screenWipe
import soundFx56
import cCursor
import infoGraphic56


BLACK = (0,0,0)
GREY = (150,150,150)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED = (255,0,0)

BUTTON_FRAMESIZE = (350, 40)
BUTTON_FRAMECOLOR = (GREY, WHITE)
BUTTON_FONTSIZE = 20
BUTTON_FONTCOLOR = BLACK
BUTTON_INDENT = 25


BACKBUTTON_POS = (265,500) # back


class AboutScreen(object):
    """ running state """
    me = None
    bkg = None

    def __init__(self):
        AboutScreen.me = self
        if not AboutScreen.bkg:
            AboutScreen.bkg = dinosInSpace.loadImage("aboutScreen.png")

        self.screen = pygame.display.get_surface()
        self.background = AboutScreen.bkg.copy()
        self.screen.blit(self.background, (0,0))

        # groups
        self.textGroup = pygame.sprite.Group()
        self.buttonGroup = pygame.sprite.Group()
        self.cursorGroup = pygame.sprite.GroupSingle()

    @staticmethod
    def wipe():
        AboutScreen.me = None

    def addSpriteToGroup(self, sprite, group):
        if group == "text":
            self.textGroup.add(sprite)
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
        clock = pygame.time.Clock()
        keepGoing = True
        firstCycle = True
        dest = None
        _fps = fpsSwitch.FPSSwitch._fps

        while keepGoing:

            clock.tick(_fps)
            dest = self.getInput()

            # clear - update - draws
            self.textGroup.clear(self.screen, self.background)
            self.buttonGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)

            self.textGroup.update()
            self.buttonGroup.update()
            self.cursorGroup.update()

            self.textGroup.draw(self.screen)
            self.buttonGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            if imageFrom:
                screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "left")
                imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            if dest:
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

        soundFx56.SoundPlayer.requestSound("woosh_b")
        return snapshot

def launch(imageFrom):
    aboutScreen = AboutScreen()
    bBack = button.Button("dBack", BUTTON_FRAMESIZE, BACKBUTTON_POS, BUTTON_FRAMECOLOR, "back", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    cursor = cCursor.Cursor()
    aboutScreen.addSpriteToGroup(bBack, "button")
    aboutScreen.addSpriteToGroup(cursor, "cursor")

    snapshot = aboutScreen.runMe(imageFrom)
    wipe()
    return snapshot

def wipe():
    AboutScreen.wipe()

if __name__ == '__main__':
    print "module for import only"
