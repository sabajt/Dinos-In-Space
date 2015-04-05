""" gfx56.py """

import pygame
import dinosInSpace
import dino56
import scroller56
import static56

class TerminalSeq(pygame.sprite.Sprite):
    """ superclass for objects that disappear after animation - choose child """

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        self.frame = 0
        self.game = game
        self.minSpeed = dinosInSpace.Game.getMinSpeed()
        self.isFirstTick = True

    def update(self):
        if not self.isFirstTick:
            self.setSpeed()

        self.isFirstTick = False
        self.image = self.myFrames[self.frame] # MUST SET myFrames in child class
        self.frame += 1

    def setSpeed(self):
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

class SwooshSeq(TerminalSeq):
    allFrames = []

    def __init__(self, game, insertHere, myWarp):
        TerminalSeq.__init__(self, game)

        self.insertHere = insertHere
        self.myFrames = self.loadImages("twSwooshN")
        self.totalFrames = len(self.myFrames) - 1
        self.image = self.myFrames[0]
        self.rect = self.image.get_rect()
        self.setLocation(myWarp)
        self.myGroupSingle = pygame.sprite.GroupSingle(self)
        self.insertGroup()

    def update(self):
        TerminalSeq.update(self)

        if self.frame > self.totalFrames:
            self.game.removeGroup(self.myGroupSingle)
            self.kill()

    def insertGroup(self):
        """ inserts group single into game.groupList at correct depth """
        self.game.insertGroup(self.myGroupSingle, self.insertHere)

    def setLocation(self, myWarp):
        self.rect.center = myWarp.getCenter()

    def loadImages(self, rootImage):
        if not SwooshSeq.allFrames:
            for i in range(6):
                prefix = "000"
                if i > 9:
                    prefix = "00"

                fileName = rootImage + prefix + str(i) + ".png"
                img = dinosInSpace.loadImage(fileName, "2X", (0,0))
                SwooshSeq.allFrames.append(img)

        return SwooshSeq.allFrames

class WarpSeq(TerminalSeq):
    """ animation appears after dino warp """
    allFrames = []

    def __init__(self, game, insertHere, myWarp):
        TerminalSeq.__init__(self, game)

        self.insertHere = insertHere
        self.myFrames = self.loadImages("twWarp")
        self.totalFrames = len(self.myFrames) - 1
        self.image = self.myFrames[0]
        self.rect = self.image.get_rect()
        self.setLocation(myWarp)
        self.myGroupSingle = pygame.sprite.GroupSingle(self)
        self.insertGroup()

    def update(self):
        TerminalSeq.update(self)

        if self.frame > self.totalFrames:
            self.game.removeGroup(self.myGroupSingle)
            self.kill()

    def insertGroup(self):
        """ inserts group single into game.groupList at correct depth """
        self.game.insertGroup(self.myGroupSingle, self.insertHere)

    def setLocation(self, myWarp):
        self.rect.center = myWarp.getCenter()

    def loadImages(self, rootImage):
        if not WarpSeq.allFrames:
            for i in range(7):
                prefix = "000"
                if i > 9:
                    prefix = "00"

                fileName = rootImage + prefix + str(i) + ".png"
                img = dinosInSpace.loadImage(fileName, "2X", (0,0))
                WarpSeq.allFrames.append(img)

        return WarpSeq.allFrames

class VanishSeq(TerminalSeq):

    allFrames = []
    vanishGroup = pygame.sprite.RenderUpdates()
    hasRemovedGroup = False

    def __init__(self, game, center):
        TerminalSeq.__init__(self, game)

        self.myFrames = self.loadImages("vanishTest2")
        self.totalFrames = len(self.myFrames) - 1
        self.image = self.myFrames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        VanishSeq.vanishGroup.add(self)
        VanishSeq.hasRemovedGroup = False

    def update(self):
        TerminalSeq.update(self)

        if self.frame > self.totalFrames:
            if not VanishSeq.hasRemovedGroup:
                VanishSeq.hasRemovedGroup = True
                self.game.removeGroup(VanishSeq.vanishGroup)
            self.kill()

    @staticmethod
    def getIsRunning():
        if len(VanishSeq.vanishGroup) > 0:
            return True
        else:
            return False

    @staticmethod
    def searchAndCreate(game):
        """ find items that need animation trail and create in place"""
        needAdd = False

        for d in dino56.Dino.dinoGroup:
            if d.active:
                needAdd = True
                VanishSeq(game, d.getCenter())

        for s in static56.Spawn.spawnGroup:
            needAdd = True
            dx, dy = s.reverseStep()
            VanishSeq(game, (s.rect.centerx - dx, s.rect.centery - dy))

        for sw in static56.Switch.switchGroup:
            needAdd = True
            dx, dy = s.reverseStep()
            VanishSeq(game, (sw.rect.centerx - dx, sw.rect.centery - dy))

        for l in static56.StaticArrowL.sArrowLGroup:
            needAdd = True
            dx, dy = l.reverseStep()
            VanishSeq(game, (l.rect.centerx - dx, l.rect.centery - dy))

        if needAdd:
            game.addGroup(VanishSeq.vanishGroup)

    def loadImages(self, rootImage):
        if not VanishSeq.allFrames:
            for i in range(7):
                prefix = "000"
                if i > 9:
                    prefix = "00"

                fileName = rootImage + prefix + str(i) + ".png"
                img = dinosInSpace.loadImage(fileName, "2X", (0,0))
                VanishSeq.allFrames.append(img)

        return VanishSeq.allFrames

class ScreenFlash(TerminalSeq):

    def __init__(self, game, colorList, Length, alpha):
        """ length must be > 2 for some reason """
        TerminalSeq.__init__(self, game)

        self.setMyFrames(colorList, Length, alpha)
        self.totalFrames = len(self.myFrames)
        self.image = self.myFrames[0]
        self.rect = self.image.get_rect()
        self.myGroupSingle = pygame.sprite.GroupSingle(self)

        game.addGroup(self.myGroupSingle)

    def update(self):
        self.image = self.myFrames[self.frame]
        self.frame += 1

        if self.frame > (self.totalFrames - 1):
            self.game.removeGroup(self.myGroupSingle)
            self.kill()

    def setSpeed(self): # override to nullify
        pass

    def setMyFrames(self, colorList, Length, alpha):
        screen = pygame.display.get_surface()
        image = pygame.Surface(screen.get_size())
        self.myFrames = []

        for c in colorList:
            newImage = image.copy()
            newImage.fill(c)
            newImage.set_alpha(alpha)
            self.myFrames.append(newImage)

        colorsLen = len(self.myFrames)
        counter = 0

        for i in range(Length):
            if counter > (colorsLen - 1):
                counter = 0

            self.myFrames.append(self.myFrames[counter].copy())
            counter += 1

def drawBorder(game, color=(255,255,255)):

    screen = game.screen
    pygame.draw.lines(
        screen,
        color,
        True,
        [(0,0),
        (screen.get_width() - 1, 0),
        (screen.get_width() - 1, screen.get_height() - 1),
        (0, screen.get_height() - 1)],
        1
    )

def centerBlit(frame, topSurf):
    """
        blits topSurf onto center of frame surface
        - frame must be >= (w and h) than topSurf
        - returns combined surface
    """
    assert(frame.get_width() >= topSurf.get_width())
    assert(frame.get_height() >= topSurf.get_height())

    left = (frame.get_width() - topSurf.get_width())/2
    top = (frame.get_height() - topSurf.get_height())/2
    combined = frame.copy()
    combined.blit(topSurf, (left, top))

    return combined

def shadeColor(color, shadeStep, rgbLim=None):
    """
        takes a RGB triplet value and changes each value by shadeStep
        returns new color as tuple

        rgbLim should initially be passed in as 3 Falses in a list or tuple
            and will be returned, each modified to true only if a rgb value
            reaches its limit.  this new rgbLim should be passed back in on
            the next iteration.
    """
    assert(len(color) == 3 and len(rgbLim) == 3)

    newColor = []
    newRgbLim = []
    count = 0
    for value in color:
        assert(value >= 0 and value <= 255)

        if not rgbLim:
            value += shadeStep
            if value < 0:
                value = 0
            if value > 255:
                value = 255
        else:
            if rgbLim[count]:
                value -= shadeStep
                if value < 0 or value > 255:
                    value += 2*shadeStep
                    newRgbLim.append(not rgbLim[count])
                else:
                    newRgbLim.append(rgbLim[count])
            else:
                value += shadeStep
                if value < 0 or value > 255:
                    value -= 2*shadeStep
                    newRgbLim.append(not rgbLim[count])
                else:
                    newRgbLim.append(rgbLim[count])

        newColor.append(value)
        count += 1

    if not rgbLim:
        return tuple(newColor)
    else:
        return tuple(newColor), tuple(newRgbLim)


def spiralOut(spr, directionAsInt, rotateStep, scaleStep, terminateAfter, frameCount, ORIGINAL):
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
        spr.image = pygame.transform.rotate(ORIGINAL, directionAsInt*rotateStep*frameCount)
        spr.image = pygame.transform.scale(ORIGINAL, (spr.image.get_width() + scaleStep, spr.iamge.get_height() + scaleStep))
        spr.rect = spr.image.get_rect()
        spr.rect.center = center
        terminate = False

    return terminate



