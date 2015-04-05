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

F30_BOXW = 500
F30_BOXH = 300
F60_BOXW = 500
F60_BOXH = 300

F30_XSPD_INC = 13
F30_YSPD_INC = 13
F60_XSPD_INC = 26 # larger means slower: try x 30, y 22 at 30 fps : x 55, y 55 at 60... 20, 15 minSpeed3
F60_YSPD_INC = 26


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

    def __init__(self, game, gridSize, cameraPos=None, _fps=60):
        """ cameraPos can be strings: T, B, R, L, TR, TL, BR, BL or None for center """
        pygame.sprite.Sprite.__init__(self)

        self._fps = _fps
        self.CLASS          = "Scroller"
        self.gridSize       = gridSize
        size                = self.setSize(gridSize, game)
        self.image          = pygame.Surface(size)  # box size determines size of field
        self.rect           = self.image.get_rect()
        self.screen         = game.screen
        self.minSpeed       = 1
        scrollerGroup       = pygame.sprite.RenderUpdates(self)

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

    @staticmethod
    def getGridSize():
        """ called by radar56.Radar.makeTracker """
        return Scroller.theScroller.gridSize

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
            self.rect.centery  = center_y
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
        """ returns: scroller box width, scroller box height
            max compatible with function is 20 x 17 -- game sets as 17 x 17
        """
        columns, rows = 8, 6
        if gridSize[0] >= 8:
            columns = gridSize[0]
        if gridSize[1] >= 6:
            rows = gridSize[1]

        m = game.getMinSpeed()
        resW = game.screen.get_width()
        resH = game.screen.get_height()
        sw = resW - ( ((100 * columns) - resW) // m ) # scroller box width
        sh = resH - ( ((100 * rows) - resH) // m ) # scroller box height

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

            if self._fps == 60:
                boxWidth = F60_BOXW
                boxHeight = F60_BOXH
                xSpeedInc = F60_XSPD_INC
                ySpeedInc = F60_YSPD_INC
            elif self._fps == 30:
                boxWidth = F30_BOXW
                boxHeight = F30_BOXH
                xSpeedInc = F30_XSPD_INC
                ySpeedInc = F30_YSPD_INC

            ## outside the following box, mouse determines speed
            cbLeft = self.screen.get_width()/2 - boxWidth/2
            cbRight = self.screen.get_width()/2 + boxWidth/2
            cbTop = self.screen.get_height()/2 + boxHeight/2
            cbBottom = self.screen.get_height()/2 - boxHeight/2

            # MUST use modular division (//) to preserve intergers
            if mouseX > self.screen.get_width()/2:
                if mouseX > cbRight:
                    distance = mouseX - cbRight + 2 # +2 bugfix
                    xSpeedRatio = -(distance // xSpeedInc)   # larger means slower
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
                    distance = mouseY - cbTop + 2 # +2 bugfix
                    ySpeedRatio = -(distance // ySpeedInc)
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

    print "module for import only"