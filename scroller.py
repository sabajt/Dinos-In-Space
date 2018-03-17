""" scroller56.py

    class
        Sprite
            Scroller
    function
        wipe

"""

import pygame
import math
import dinosInSpace
import areaSelect

class Scroller(pygame.sprite.Sprite):
    """ box controlling the scrolling mechanism
        -gets int from mouse that is speed multiple dependent on d from center
        -when scroller box reaches edge of the screen, everything stops
        -every moving object gets its speed from this box's speed
        -this box has the lowest multiple of speed
        -must give objs that get minSpeed from here an INT to stay in-sync
    """
    speedData = None    # (int, int) all moving objects get speed from here
    theScroller = None  # (sprite) ref to the 1 instance of the scroll box itself
    fieldWidth = None   # (int) total width of the playing field
    fieldHeight = None  # (int) total height of the playing field

    def __init__(self, game, gridSize, cameraPos=None):
        """ cameraPos can be strings: T, B, R, L, TR, TL, BR, BL or None for center """
        pygame.sprite.Sprite.__init__(self)

        self.CLASS          = "Scroller"
        size                = self.setSize(gridSize, game)
        self.image          = pygame.Surface(size)  # box size determines size of field
        self.rect           = self.image.get_rect()
        self.screen         = game.screen
        self.minSpeed       = 1
        scrollerGroup       = pygame.sprite.GroupSingle(self)

        self.image.fill((255,255,255))
        self.image.set_alpha(0, pygame.RLEACCEL)
        self.positionCamera(cameraPos)

        if game.__class__ == dinosInSpace.Game:
            game.groupList.append(scrollerGroup)

#        elif game.CLASS == areaSelect56.StageSystem:
#            game.addSprite(self)

#        elif game.__class__ = areaSelect.SelectScreen:
#                game.

        Scroller.theScroller = self
        self.setFieldBounds()

    def update(self):
        dx, dy = self.getSpeed()
        self.setPos(dx, dy)

    @staticmethod
    def wipe():
        Scroller.speedData = None
        Scroller.theScroller = None
        Scroller.fieldWidth = None
        Scroller.fieldHeight = None

    def positionCamera(self, cameraPos):
        top         = 0
        bottom      = self.screen.get_height()
        left        = 0
        right       = self.screen.get_width()
        center_x    = self.screen.get_width()/2
        center_y    = self.screen.get_height()/2

        if cameraPos == "B":
            self.rect.top       = top
            self.rect.centerx   = center_x
        elif cameraPos == "T":
            self.rect.bottom    = bottom
            self.rect.centerx   = center_x
        elif cameraPos == "L":
            self.rect.right     = right
            self.rect.centery   = center_y
        elif cameraPos == "R":
            self.rect.left      = left
            self.rect.center_y  = center_y
        elif cameraPos == "BL":
            self.rect.top       = top
            self.rect.right     = right
        elif cameraPos == "BR":
            self.rect.top       = top
            self.rect.left      = left
        elif cameraPos == "TL":
            self.rect.bottom    = bottom
            self.rect.right     = right
        elif cameraPos == "TR":
            self.rect.bottom    = bottom
            self.rect.left      = left
        else:
            self.rect.centerx   = center_x
            self.rect.centery   = center_y


    def setSize(self, gridSize, game):
        """ returns: scroller box width, scroller box height """
        c, r = gridSize # columns, rows
        m = game.getMinSpeed()
        resW = game.screen.get_width()
        resH = game.screen.get_height()
        sw = resW - ( ((100 * c) - resW) // m ) # scroller box width
        sh = resH - ( ((100 * r) - resH) // m ) # scroller box height

        return (sw, sh)

    @staticmethod
    def getMe():
        return Scroller.theScroller

    def setFieldBounds(self):
        """ sets: fieldWidth, fieldHeight """
        m = dinosInSpace.Game.getMinSpeed()
        screenWidth = self.screen.get_width()
        screenHeight = self.screen.get_height()
        baseWidth = screenWidth - self.image.get_width()
        baseHeight = screenHeight - self.image.get_height()

        Scroller.fieldWidth = baseWidth * m + screenWidth + m
        Scroller.fieldHeight = baseHeight * m+ screenHeight + m

    @staticmethod
    def getFieldBounds():
        """ returns: fieldWidth, fieldHeight """
        return Scroller.fieldWidth, Scroller.fieldHeight

    def getSpeed(self):
        """ the scroller box's speed itself """

        speedData = self.getSpeedRatio()
        (xSpeedRatio, ySpeedRatio) = speedData # unpack
        dx = xSpeedRatio * self.minSpeed # get self's speed
        dy = ySpeedRatio * self.minSpeed

        return (dx, dy)

    def setPos(self, dx, dy):
        """ update pos, restore speedData """

        if dx != 0:  # stop if we get to the boundary
            dx = self.checkBoundary(dx, "x")

        if dy != 0:
            dy = self.checkBoundary(dy, "y")

        self.rect.centerx += dx # change position
        self.rect.centery += dy
        self.speedData = (dx,dy)
        Scroller.speedData = self.speedData # store for access by other objects

    def checkBoundary(self, speed, plane):
        """ returns: speed; if speed > than the distance to screen: speed
            == distance to screen else leave speed alone """

        if plane == "x":
            if speed > 0:
                distance = self.screen.get_width() - self.rect.right
                closer = min
            elif speed < 0:
                distance = -self.rect.left
                closer = max

        elif plane == "y":
            if speed > 0:
                distance = self.screen.get_height() - self.rect.bottom
                closer = min
            elif speed < 0:
                distance = -self.rect.top
                closer = max

        if speed != distance:
            speed = closer(distance, speed)

        return speed

    def getSpeedRatio(self):
            """ returns: speedRatio from mousePos; far from cnt is larger speed """

            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            ## outside the following box, mouse determines speed

            boxWidth = 100
            boxHeight = 100
            cbLeft = self.screen.get_width()/2 - boxWidth
            cbRight = self.screen.get_width()/2 + boxWidth
            cbTop = self.screen.get_height()/2 + boxHeight
            cbBottom = self.screen.get_height()/2 - boxHeight

            # MUST use modular division (//) to preserve intergers

            xSpeedInc = 30 # larger means slower (try x 30, y 22) .. (20, 15 (minSpeed3))
            ySpeedInc = 22

            if mouseX > self.screen.get_width()/2:
                if mouseX > cbRight:
                    distance = mouseX - cbRight
                    xSpeedRatio = -distance // xSpeedInc   # larger means slower
                else:
                    xSpeedRatio = 0

            else:
                if mouseX < cbLeft:
                    distance = int(math.fabs(mouseX - cbLeft))
                    xSpeedRatio = distance // xSpeedInc
                else:
                    xSpeedRatio = 0

            if mouseY > self.screen.get_height()/2:
                if mouseY > cbTop:
                    distance = mouseY - cbTop
                    ySpeedRatio = -distance // ySpeedInc
                else:
                    ySpeedRatio = 0

            else:
                if mouseY < cbBottom:
                    distance = int(math.fabs(mouseY - cbBottom))
                    ySpeedRatio = distance // ySpeedInc
                else:
                    ySpeedRatio = 0

            speedData = (xSpeedRatio, ySpeedRatio)
            return speedData

def wipe():

    Scroller.wipe()

if __name__ == "__main__":

    print("module for import only")