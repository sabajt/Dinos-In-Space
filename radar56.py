""" radar56.py

    class
        Sprite
            GridLine
            Radar
            RObj
                RBack
                RCursor
                RView
                RBlock
                RDino
                RStatic
    function
        drawBorder
        makeGrid
        wipe

"""

import pygame
import dino56
import scroller56
import dinosInSpace
import static56
import interface56
import block56
import infoGraphic56

STD_GRIDSTEP = 100

class GridLine(pygame.sprite.Sprite):

    def __init__(self, game, size, midLeft, midTop):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill((0,255,0))
        self.image.set_alpha(40, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.minSpeed = game.getMinSpeed()

        if midLeft:
            self.rect.midleft = midLeft
        elif midTop:
            self.rect.midtop = midTop

    def update(self):
        """ called every tick in runGame """

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        scrollingDx = xSpeedRatio * self.minSpeed
        scrollingDy = ySpeedRatio * self.minSpeed
        self.rect.centerx += scrollingDx
        self.rect.centery += scrollingDy

class Radar(pygame.sprite.Sprite):
    """ radar of key objects """

    theRadar = None # the 1 radar instance
    dinoGroup = None # sprite Group of all dinos
    blockGroup = None # sprite Group of all the Blocks
    staticGroup = None # sprite Group of all static Blocks (spawn / goal)

    def __init__(self, game):

        pygame.sprite.Sprite.__init__(self)

        Radar.theRadar = self
        self.radarGroup = pygame.sprite.OrderedUpdates()    # group for screen updates
        self.screen = game.screen
        self.formatRadarScreen()
        self.makeTracker()

        game.addGroup(self.radarGroup)

    def update(self):
        """ called every tick in runGame """

        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        scrollingDx = xSpeedRatio * self.minSpeed
        scrollingDy = ySpeedRatio * self.minSpeed
        self.rect.centerx += scrollingDx
        self.rect.centery += scrollingDy

    @staticmethod
    def wipe():

        Radar.theRadar = None
        Radar.dinoGroup = None
        Radar.blockGroup = None
        Radar.staticGroup = None

    @staticmethod
    def quickReset():

        Radar.setDinoGroup()
        Radar.theRadar.makeRDino()

    @staticmethod
    def setDinoGroup():

        Radar.dinoGroup = dino56.Dino.getDinoGroup()

    @staticmethod
    def setBlockGroup():

        Radar.blockGroup = block56.Block.getBlockGroup()

    @staticmethod
    def setStaticGroup():

        Radar.staticGroup = static56.StaticBlock.getStaticGroup()

    @staticmethod
    def getInitData():
        """ return rScreenLeft, rScreenTop, SCALE """

        r = Radar.theRadar

        return (r.rScreenLeft, r.rScreenTop, r.SCALE)

    @staticmethod
    def getTrackerLoc():
        """ return radar rect centerx, rect centery """

        r = Radar.theRadar

        return (r.rect.centerx, r.rect.centery)

    @staticmethod
    def reqDrawRadarScreen():

        Radar.theRadar.drawRadarScreen()

    def formatRadarScreen(self):
        """ scale radar according to level size """

        self.SCALE = 20 # as num gets larger, radar gets smaller
        self.minSpeed = dinosInSpace.Game.getMinSpeed()
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()
        self.fieldWidth, self.fieldHeight = scroller56.Scroller.getFieldBounds()
        self.rScreenWidth = self.fieldWidth/self.SCALE
        self.rScreenHeight = self.fieldHeight/self.SCALE
        self.rScreenLeft = self.screenWidth - self.rScreenWidth
        self.rScreenTop = self.screenHeight - self.rScreenHeight

    def makeTracker(self):
        """ the r-obj's sprite, all r-obj get loc relative to tracker """
        gridSize = scroller56.Scroller.getGridSize()

        if gridSize[0] >= 8: # normal case, toRight will be <=0
            toRight = (scroller56.Scroller.theScroller.rect.right - self.screenWidth) * self.minSpeed
        else: # tracker will start at a positive value
            toRight = (self.screenWidth - gridSize[0]*STD_GRIDSTEP) / 2

        if gridSize[1] >= 6: # normal case, toBottom will be <=0
            toBottom = (scroller56.Scroller.theScroller.rect.bottom - self.screenHeight) * self.minSpeed
        else: # tracker will start at a positive value
            toBottom = (self.screenHeight - gridSize[1]*STD_GRIDSTEP) / 2

        startHere = (toRight, toBottom)

        self.image = pygame.Surface((8,8))    # the tracker is just a box
        self.image.fill((255,0,0))
        self.image.set_alpha(0, pygame.RLEACCEL)

        self.rect = self.image.get_rect()
        self.rect.center = startHere
        self.radarGroup.add(self)

##    def makeTracker(self):
##        """ the r-obj's sprite, all r-obj get loc relative to tracker """
##        toRight = (scroller56.Scroller.theScroller.rect.right - self.screenWidth) * self.minSpeed
##
##
##        toBottom = (scroller56.Scroller.theScroller.rect.bottom - self.screenHeight) * self.minSpeed
##        startHere = (toRight, toBottom)
##
##        self.image = pygame.Surface((8,8))    # the tracker is just a box
##        self.image.fill((255,0,0))
##        self.image.set_alpha(0, pygame.RLEACCEL)
##
##        self.rect = self.image.get_rect()
##        self.rect.center = startHere
##        self.radarGroup.add(self)

    def makeImages(self):
        """ make all radar images """

        self.makeRBack()
        self.makeRBlock()
        self.makeRStatic()
        self.makeRDino()
        self.makeRView()
        self.makeRCursor()

    def makeRBack(self):
        """ radar background """

        w = self.screenWidth - self.rScreenLeft
        h = self.rScreenHeight
        rBack = RBack(None, w, h, (0,0,0))

    def makeRCursor(self):
        """ the player's cursor """

        cursor = interface56.Cursor.theCursor
        rCursor = RCursor(cursor, 3, 3, (255,255,255))

    def makeRView(self):
        """ the player's screen """

        w = self.screenWidth/self.SCALE
        h = self.screenHeight/self.SCALE
        rView = RView(None, w, h, (255,255,255)) # this color will be hidden, cannot be yellow

    def makeRDino(self):
        """ dino objs """

        if Radar.dinoGroup:

            for d in Radar.dinoGroup:

                RDino(d, 3, 3, (0,255,0))

    def makeRBlock(self):
        """ block objs """

        if Radar.blockGroup:

            for b in Radar.blockGroup:

                if b.CLASS == "Arrow":

                    RBlock(b, 3, 3, (0,100,255))

                if b.CLASS == "Warp":

                    RBlock(b, 3, 3, (0,100,255))

    def makeRStatic(self):
        """ static blocks (spawn / goal ) """

        if Radar.staticGroup:

            for s in Radar.staticGroup:

                if s.CLASS == "Goal":

                    RStatic(s, 3, 3, (255,255,0))

                elif s.CLASS == "Spawn":

                    RStatic(s, 3, 3, (200,100,255))

                elif s.CLASS == "Mine":

                    RStatic(s, 3, 3, (255,0,0))

                elif s.CLASS == "StaticArrow":

                    RStatic(s, 3, 3, (120,120,120))

                elif s.CLASS == "StaticArrowL":

                    RStatic(s, 3, 3, (120,120,120))

                elif s.CLASS == "Switch":

                    RStatic(s, 3, 3, (120,120,120))

    def drawRadarScreen(self):
        """ draw the radar screen - uses draw fx, no sprites """

        if infoGraphic56.InfoGraphic.visible:

            pygame.draw.lines(  # radar box
                self.screen,
                (255,255,255),
                False,
                [(self.rScreenLeft - 1, self.screenHeight),
                (self.rScreenLeft - 1 , self.rScreenTop - 1),
                (self.screenWidth, self.rScreenTop - 1)],
                1
            )

class RObj(infoGraphic56.InfoGraphic):
    """ parent class of radar images """

    rObjGroup = pygame.sprite.OrderedUpdates()

    def __init__(self, followMe, w, h, color):
        """ build radar representation of obj on field to follow """

        infoGraphic56.InfoGraphic.__init__(self)

        self.ALPHA = 255
        self.rScreenLeft, self.rScreenTop, self.SCALE = Radar.getInitData()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.followMe = followMe

        RObj.rObjGroup.add(self)

    def update(self):
        """ update location of followMe (if at all) scaled to radar screen """

        if self.followMe:

            (rBoxX, rBoxY) = Radar.getTrackerLoc()
            xDist = self.followMe.rect.centerx - rBoxX
            yDist = self.followMe.rect.centery - rBoxY
            x = self.rScreenLeft + xDist/self.SCALE
            y = self.rScreenTop + yDist/self.SCALE
            self.rect.center = (x, y)

    @staticmethod
    def wipe():

        RObj.rObjGroup = pygame.sprite.OrderedUpdates()

class RBack(RObj):
    """ background for radar """

    def __init__(self, followMe, w, h, color):

        RObj.__init__(self, followMe, w, h, color)

        self.ALPHA = 200
        (x, y, throwAway) = Radar.getInitData()
        self.rect.topleft = (x, y)
        self.image.set_alpha(self.ALPHA, pygame.RLEACCEL)

class RCursor(RObj):
    """ radar image of the player's cursor """

    pass

class RView(RObj):
    """ radar image of the view of the player - scaled screen size """

    def __init__(self, followMe, w, h, color):

        RObj.__init__(self, followMe, w, h, (0,0,0))

        self.image.set_colorkey((0,0,0), pygame.RLEACCEL)
        pygame.draw.rect(self.image, color, self.rect, 1)

    def update(self):
        """ overwrites parent update method, view is screen, not followMe """

        (rBoxX, rBoxY) = Radar.getTrackerLoc()
        xDist = - rBoxX
        yDist = - rBoxY
        x = self.rScreenLeft + xDist/self.SCALE
        y = self.rScreenTop + yDist/self.SCALE
        self.rect.topleft = (x, y)

class RBlock(RObj):
    """ radar image of the blocks """

    def update(self):
        """ extends RObj update method - only display if active """

        if self.followMe.active and infoGraphic56.InfoGraphic.visible:

            if self.image.get_alpha != 255:

                self.image.set_alpha(255)

            RObj.update(self)

        else:

            if self.image.get_alpha != 0:

                self.image.set_alpha(0, pygame.RLEACCEL)

class RDino(RBlock):
    """ radar image of the dinos """

    def update(self):
        """ extends RBlock.update to remove if dino is gone """

        RBlock.update(self)

        if self.followMe not in Radar.dinoGroup:

            self.kill()

class RStatic(RObj):
    """ radar image of static blocks: spawn and goal """

    pass

def drawBorder(game):

    screen = game.screen
    pygame.draw.lines(
        screen,
        (255,255,255),
        True,
        [(0,0),
        (screen.get_width() - 1, 0),
        (screen.get_width() - 1, screen.get_height() - 1),
        (0, screen.get_height() - 1)],
        1
    )

def makeGrid(game, gridSize):
    gridGroup = pygame.sprite.RenderUpdates()

    (x, y) = Radar.getTrackerLoc()
    w = gridSize[0]*STD_GRIDSTEP
    h = gridSize[1]*STD_GRIDSTEP
    xStep, yStep = gridSize

    yOriginal = y
    for i in range(yStep + 1):
        g = GridLine(game, (w, 1), (x, y), None)
        y += 100
        gridGroup.add(g)

    y = yOriginal
    for i in range(xStep + 1):
        g = GridLine(game, (1, h), None, (x, y))
        x += 100
        gridGroup.add(g)

    game.addGroup(gridGroup)

def wipe():

    Radar.wipe()
    RObj.wipe()

if __name__ == "__main__":

    print "module for import only"