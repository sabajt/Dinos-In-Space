"""
    winningScreen.py
    screen player is taken to if last puzzle just completed
"""

import pygame
import dinosInSpace
import infoGraphic56
import soundFx56

RED = (150,0,0)
BLACK = (0,0,0)
LINE1 = "you are a master of spatial reasoning!"
LINE2 = "thanks for playing, here's a picture of my cat:"
LINE3 = "try creating puzzles for your friends!"
TEXTSIZE = 20
TEXTCOLOR = RED
BACKGROUNDCOLOR = BLACK
LINECENTERS = ((400,30), (400,60), (400, 570))
BLITCAT = (80,60)

class WinScreen(object):
    backgroundImage = None

    def __init__(self):
        if not WinScreen.backgroundImage:
            WinScreen.backgroundImage = dinosInSpace.loadImage("magz.png")
        self.background = pygame.Surface((800,600))
        self.background.fill(BACKGROUNDCOLOR)
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.background, (0,0))
        self.screen.blit(WinScreen.backgroundImage.copy(), BLITCAT)

        self.mainGroup = pygame.sprite.OrderedUpdates()

    def runMe(self):
        clock = pygame.time.Clock()
        keepGoing = True
        pygame.display.update()
        soundFx56.SoundPlayer.requestSound("winGame")
        while keepGoing:
            clock.tick(60)

            # input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    keepGoing = False

            # update cycle
            self.mainGroup.clear(self.screen, self.background)
            self.mainGroup.update()
            self.mainGroup.draw(self.screen)

            pygame.display.update()

    def addSpriteToGroup(self, sprite, group="mainGroup"):
        if group == "mainGroup":
            self.mainGroup.add(sprite)

    def addSpriteListToGroup(self, spriteList, group="mainGroup"):
        for s in spriteList:
            self.addSpriteToGroup(s, group)


def launch():
    winScreen = WinScreen()
    text1 = infoGraphic56.TextObject(LINE1, TEXTSIZE, TEXTCOLOR, LINECENTERS[0])
    text2 = infoGraphic56.TextObject(LINE2, TEXTSIZE, TEXTCOLOR, LINECENTERS[1])
    text3 = infoGraphic56.TextObject(LINE3, TEXTSIZE, TEXTCOLOR, LINECENTERS[2])
    winScreen.addSpriteListToGroup([text1, text2, text3])
    winScreen.runMe()
