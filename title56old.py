""" title56.py """

import pygame
import dinosInSpace
import controlMenu56
import radar56
import screenWipe
import modeSwitch

class TitleScreen(object):
    background = None
    titleScreenGroup = pygame.sprite.OrderedUpdates()
    _fps = 60

    def __init__(self, screen):
        self.screen = screen
        self.background = self.setBackground("demoSplash.png")
        self.screen.blit(self.background, (0,0))
        self.clock = pygame.time.Clock()
        #foreGround = TitleForeGround(screen)
        self.makeTitleMenu()
        #TitleScreen.titleScreenGroup.add(foreGround, self.titleMenuGroup)
        TitleScreen.titleScreenGroup.add(self.titleMenuGroup)

    @staticmethod
    def wipe():
        TitleScreen.titleScreenGroup = pygame.sprite.OrderedUpdates()

    def setGoTo(self, goTo):
        self.goTo = goTo

    def makeTitleMenu(self):
        titleMenu = controlMenu56.TitleMenu(self)
        self.titleMenuGroup = titleMenu.titleMenuGroup

    def setBackground(self, fileName):
        """ sets TitleScreen.background, returns as surf - give None for blank """
        if not TitleScreen.background:
            if fileName:
                TitleScreen.background = dinosInSpace.loadImage(fileName, self.screen.get_size(), None)
            else:
                TitleScreen.background = pygame.Surface(self.screen.get_size())
                TitleScreen.background.fill((0,0,0))

        background = TitleScreen.background

        return background

    def runTitle(self, imageFrom):
        modeSwitch.ModeSwitch.resetModes()

        self.keepGoing = True
        self.endGame = False
        self.goTo = "QUIT"

        while self.keepGoing:

            self.clock.tick(TitleScreen._fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit
                    self.keepGoing = False
                    self.setGoTo("QUIT")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # quit
                        self.keepGoing = False
                        self.setGoTo("QUIT")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controlMenu56.BasicButton.requestPress()


            TitleScreen.titleScreenGroup.clear(self.screen, self.background)

            for s in TitleScreen.titleScreenGroup:
                methods = dir(s)
                if "updateTitle" in methods:
                    s.updateTitle() # update classes with updateTitle() only

            TitleScreen.titleScreenGroup.draw(self.screen)
            radar56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(TitleScreen._fps, imageFrom, self.screen.copy(), "right")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        TitleScreen.titleScreenGroup.clear(self.screen, self.background)
##        for s in TitleScreen.titleScreenGroup:
##            methods = dir(s)
##            if "updateTitle" in methods:
##                s.updateTitle() # update classes with updateTitle() only
        for s in TitleScreen.titleScreenGroup:
            if s.__class__ == controlMenu56.ControlMenuCursor:
                TitleScreen.titleScreenGroup.remove(s)
        TitleScreen.titleScreenGroup.draw(self.screen)
        radar56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        controlMenu56.wipe()
        TitleScreen.wipe()

        return self.goTo, TitleScreen._fps, snapshot

class ForeGround(pygame.sprite.Sprite):

    def __init__(self, screen, clas):

        pygame.sprite.Sprite.__init__(self)
        self.CLASS = clas
        self.screen = screen

    def setImage(self, fileName, scaleTo, getAt):

        if fileName:

            if not self.CLASS.myImage:

                self.CLASS.myImage = dinosInSpace.loadImage(fileName, scaleTo, getAt)

            self.image = self.CLASS.myImage

        else:

            self.image = pygame.Surface((self.screen.get_size()))
            self.image.fill((0,0,0))

class TitleForeGround(ForeGround):

    myImage = None

    def __init__(self, screen):

        ForeGround.__init__(self, screen, TitleForeGround)
        self.setImage(None, screen.get_size(), (630,0)) # fileName, size, getAt
        self.rect = self.image.get_rect()