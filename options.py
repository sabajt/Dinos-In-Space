"""
    options.py
    options screen
"""
import pygame
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

BUTTON_POS = [
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, 250), # mute
    (BUTTON_FRAMESIZE[0]/2 + BUTTON_INDENT, 350), # back
]

MUTE_TEXT_COLOR = WHITE
##MUTE_BKG_COLOR = RED
MUTE_CENTER = (BUTTON_POS[0][0] + 220, BUTTON_POS[0][1])


class OptionsScreen(object):
    """ running state """
    me = None

    def __init__(self):
        OptionsScreen.me = self

        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))

        # groups
        self.textGroup = pygame.sprite.Group()
        self.buttonGroup = pygame.sprite.Group()
        self.cursorGroup = pygame.sprite.GroupSingle()

    @staticmethod
    def wipe():
        OptionsScreen.me = None

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
                if dest == "dMute":
                    if soundFx56.SoundPlayer.player.mute:
                        soundFx56.SoundPlayer.player.mute = False
                    else:
                        soundFx56.SoundPlayer.player.mute = True

                elif dest == "dBack":
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

class MuteText(infoGraphic56.TextObject):
    """
        TextObject that checks soundFx for mute and displays on or off
    """
    def __init__(self):
        self.currentText = "off"
        infoGraphic56.TextObject.__init__(self, self.currentText, BUTTON_FONTSIZE, MUTE_TEXT_COLOR, MUTE_CENTER)

    def update(self):
        if soundFx56.SoundPlayer.player.mute:
            if self.currentText != "on":
                self.currentText = "on"
                self.rerender(self.currentText, MUTE_TEXT_COLOR, MUTE_CENTER)
        else:
            if self.currentText != "off":
                self.currentText = "off"
                self.rerender(self.currentText, MUTE_TEXT_COLOR, MUTE_CENTER)



def launch(imageFrom):
    optionsScreen = OptionsScreen()
    bMute = button.Button("dMute", BUTTON_FRAMESIZE, BUTTON_POS[0], BUTTON_FRAMECOLOR, "mute", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    bBack = button.Button("dBack", BUTTON_FRAMESIZE, BUTTON_POS[1], BUTTON_FRAMECOLOR, "back", BUTTON_FONTSIZE, BUTTON_FONTCOLOR)
    tMute = MuteText()
    cursor = cCursor.Cursor()
    optionsScreen.addSpriteListToGroup([bMute, bBack], "button")
    optionsScreen.addSpriteToGroup(cursor, "cursor")
    optionsScreen.addSpriteToGroup(tMute, "text")
    snapshot = optionsScreen.runMe(imageFrom)
    wipe()
    return snapshot

def wipe():
    OptionsScreen.wipe()

if __name__ == '__main__':
    print("module for import only")
