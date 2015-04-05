""" dino56.py
    - the dino classes
"""
if __name__ == "__main__":
    print "module for import only"

import pygame
import math
import random
import scroller56
import groupMods56
import block56
import radar56
import dinosInSpace
import static56
import soundFx56
import level56
import infoGraphic56
import gfx56
import snack
import modeSwitch
import title56
import fpsSwitch
import snackPacket

DINOSCALE = (100,100)
FRAME_DELAY = 10
HAT_MODE = "_hat"
BOUNCE_DELAY = 5

BOUNCE_INERTIA_MODE = "decel"
KILL_INERTIA_MODE = "accel"

INERTIA_SPIN_DELAY = 3
INERTIA_SPIN_STEP = 4
INERTIA_SPIN_JUMP = 25

SPIN_RANGE = 4

STATION_FADE_STEP = 20


class Dino(pygame.sprite.Sprite):
    """ superclass for friendly spinning dinos """
    image = None
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    OFFSCREEN = (-200,-200)
    lost = 0
    activeGroup = pygame.sprite.RenderUpdates()
    dinoGroup = groupMods56.SR_OrderedUpdates()
    packetGroup = pygame.sprite.Group()
    totalCount = 0
    PA_DEPTH = None
    gridSize = None

    def __init__(self, game, floatingSpeed, spawnKey, delay):
        pygame.sprite.Sprite.__init__(self)

        Dino.minSpeed = dinosInSpace.Game.getMinSpeed()
        Dino.dinoGroup.add(self)
        if floatingSpeed:   # most dinos will get this from spawn
            self.setFloatingSpeed(floatingSpeed)
        self.spawnKey = spawnKey
        self.delay = delay  # the startup delay (not the bounce)
        self.active = False # must give each child it's own activate method!
        self.hitArrows = pygame.sprite.RenderUpdates() # has hit center of these arrows
        self.game = game
        self.paDepth = None # passing animation depth: set in level.py after dinos
        self.alpha = 255 # used for fading
        self.packet = None
        Dino.totalCount += 1


        self.spinRange = SPIN_RANGE
        if fpsSwitch.FPSSwitch._fps == 60:
            self.spinRange /= 2

    def update(self):
        """ called every tick by game """
        if self.game.getHasStarted():
            if self.active:
                self.setSpeed()
                self.checkCollision()
                self.checkHitArrows()
                self.spin()
                self.checkBounds()
            else:   # delay before activating self
                self.delay -= 1
                if self.delay < 1:
                    self.activate()  # must give the child this method

    @staticmethod
    def wipe():
        Dino.image = None
        Dino.lost = 0
        Dino.activeGroup = pygame.sprite.RenderUpdates()
        Dino.dinoGroup = groupMods56.SR_OrderedUpdates()
        Dino.packetGroup = pygame.sprite.Group()
        Dino.totalCount = 0
        Dino.gridSize = None

    @staticmethod
    def setPaDepth(paDepth):
        """ passing animation depth """
        Dino.PA_DEPTH = paDepth
        for d in Dino.dinoGroup:
            d.paDepth = paDepth

    @staticmethod
    def getDinoGroup():
        return Dino.dinoGroup

    @staticmethod
    def getLost():
        return Dino.lost

    def getCenter(self):
        return self.rect.center

    def setFloatingSpeed(self, floatingSpeed):
        floatingDx, floatingDy = floatingSpeed
        self.floatingDx = floatingDx
        self.floatingDy = floatingDy

    def setSpeed(self):
        """ scrolling speed + floating speed """
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        scrollingDx = xSpeedRatio * self.minSpeed   # scrolling speed
        scrollingDy = ySpeedRatio * self.minSpeed
        self.rect.centerx += scrollingDx + self.floatingDx # move
        self.rect.centery += scrollingDy + self.floatingDy

    def setSpin(self, rangeStart, rangeStop):
        """ initiate spin cycle """
        self.spinStep = 0
        while self.spinStep == 0:   # make sure 0 isn't picked
            self.spinStep = random.randint(rangeStart, rangeStop)
        self.defaultSpinStep = self.spinStep
        self.spinDistance   = 0

    @staticmethod
    def setGridSize(gridSize):
        Dino.gridSize = gridSize

    def checkBounds(self):
        """ kill if out of field bounds """
        screen = pygame.display.get_surface()
        (rBoxX, rBoxY) = radar56.Radar.getTrackerLoc()

        if Dino.gridSize[0] < 8:
            if self.rect.left > screen.get_width():
                self.escape()
            elif self.rect.right < 0:
                self.escape()
        else:
            if self.rect.left - rBoxX > scroller56.Scroller.fieldWidth:
                self.escape()
            elif rBoxX - self.rect.right > 0:
                self.escape()

        if Dino.gridSize[1] < 6:
            if self.rect.bottom > screen.get_height():
                self.escape()
            elif self.rect.top < 0:
                self.escape()
        else:
            if self.rect.top - rBoxY > scroller56.Scroller.fieldHeight:
                self.escape()
            elif rBoxY - self.rect.bottom > 0:
                self.escape()

    def killMe(self):
        Dino.lastDinoImage = self.image.copy()
        Dino.lastDinoCenter = self.rect.center
        self.kill()
        Dino.totalCount -= 1

    @staticmethod
    def getLastDinoImageAndCenter():
        return Dino.lastDinoImage, Dino.lastDinoCenter

    def escape(self):
##        if not self.isEscaping:
        soundFx56.GameSoundManager.registerSound("squeal") # was 'lost'
        Dino.lost += 1
        self.killMe()

    def fadeWithStep(self, step=STATION_FADE_STEP):
        self.alpha -= step
        if self.alpha < 0:
            return "end"

    def checkCollision(self): ###################### optimization by surrounding grid collision?
        """ checks collision for many object types """

        # goal
        goalSprites = pygame.sprite.spritecollide(self, static56.Goal.goalGroup, False)
        if goalSprites:
            for sprite in goalSprites:
                if sprite.CLASS == "Goal":
                    if sprite.objColor == self.objColor or not sprite.objColor:
                        if self.fadeWithStep() == "end":
                            if self.packet:
                                self.packet.hookToStation(sprite)
                            soundFx56.GameSoundManager.registerSound("goal")  # play sound
                            static56.Goal.saveDino()  # save the dino
                            self.killMe() # remove self

        # switch
        if len(static56.Switch.switchGroup) > 0:
            switchSprites = pygame.sprite.spritecollide(self, static56.Switch.switchGroup, False)
            if switchSprites:
                for sprite in switchSprites:
                    if sprite.CLASS == "Switch": # redun...
                        if pygame.sprite.collide_rect_ratio(.50)(self, sprite):
                            sprite.flipSwitch(True, False)

        # rocks (called mines)
        if len(static56.Mine.mineGroup) > 0:
            mineSprites = pygame.sprite.spritecollide(self, static56.Mine.mineGroup, False)
            if mineSprites:
                for sprite in mineSprites:
                    if sprite.CLASS == "Mine":
                        self.requestScreenSnd("squeal")
                        Dino.lost += 1
                        self.killMe()

        # user blocks
        if len(block56.Block.activeGroup) > 0:
            blockSprites = pygame.sprite.spritecollide(self, block56.Block.activeGroup, False)
            if blockSprites:
                for sprite in blockSprites:
                    if sprite.CLASS == "Arrow":
                        if sprite.objColor == self.objColor or not sprite.objColor:
                            self.changeDirection(sprite, sprite.facing)
                    if sprite.CLASS == "Warp":
                        if sprite.state == "enter":
                            self.warp(sprite)

        # static arrows
        if len(static56.StaticArrow.sArrowGroup) > 0:
            sArrowSprites = pygame.sprite.spritecollide(self, static56.StaticArrow.sArrowGroup, False)
            if sArrowSprites:
                for sprite in sArrowSprites:
                    if sprite.CLASS == "StaticArrow":    # this is redundant...
                        if sprite.objColor == self.objColor or not sprite.objColor:
                            self.changeDirection(sprite, sprite.facing)

        # static linked arrows
        if len(static56.StaticArrowL.sArrowLGroup) > 0:
            linkedArrowSprites = pygame.sprite.spritecollide(self, static56.StaticArrowL.sArrowLGroup, False)
            if linkedArrowSprites:
                for sprite in linkedArrowSprites:
                    if sprite.CLASS == "StaticArrowL":  # redun
                        if sprite.active:
                            if sprite.objColor == self.objColor \
                                or not sprite.objColor:
                                self.changeDirection(sprite, sprite.facing)

        # snax
        if len(snack.Snack.snaxGroup) > 0:
            snackSprites = pygame.sprite.spritecollide(self, snack.Snack.snaxGroup, False)
            if snackSprites:
                for sprite in snackSprites:
                    if sprite.collect():
                        if not self.packet:
                            self.packet = snackPacket.SnackPacket(self)
                            Dino.packetGroup.add(self.packet)
                        else:
                            self.packet.addCount()

    def changeDirection(self, sprite, direction):
        """ prepares for direction change """
        if sprite not in self.hitArrows:   ## ensures only 1 hit
            distance, speed, targetCenter, axis = self.distanceToCenter(sprite)
            if distance <= math.fabs(speed):
                if direction == Dino.NORTH:
                    self.newDirection(sprite, targetCenter, axis, 0, -int(math.fabs(speed)))
                elif direction == Dino.SOUTH:
                    self.newDirection(sprite, targetCenter, axis, 0, int(math.fabs(speed)))
                elif direction == Dino.EAST:
                    self.newDirection(sprite, targetCenter, axis, int(math.fabs(speed)), 0)
                elif direction == Dino.WEST:
                    self.newDirection(sprite, targetCenter, axis, -int(math.fabs(speed)), 0)

    def warp(self, sprite):
        distance, speed, targetCenter, axis = self.distanceToCenter(sprite)
        if distance <= math.fabs(speed):
            self.requestScreenSnd("dinoWarp")
            gfx56.WarpSeq(self.game, self.paDepth, sprite) # warp in fx
            self.rect.center = sprite.linkedWarp.rect.center
            self.requestScreenSnd("dinoWarp")
            gfx56.SwooshSeq(self.game, self.paDepth, sprite.linkedWarp) # warp out fx

    def newDirection(self, sprite, targetCenter, axis, floatingDx, floatingDy):
        """ changes the direction of dino based on arrow facing """
        self.requestScreenSnd("bounce")
        if axis == "x":
            self.rect.centerx = targetCenter
        elif axis == "y":
            self.rect.centery = targetCenter

        self.floatingDx = floatingDx
        self.floatingDy = floatingDy
        self.hitArrows.add(sprite)
        sprite.flashBounceMask() ## bouncing highlight animation

    def distanceToCenter(self, sprite):
        """ gets distance of center of moving object to center of
            target object and returns speed as dx or dy """
        abs = math.fabs

        if self.floatingDx != 0:
            distanceToCenter = abs(self.rect.centerx - sprite.rect.centerx)
            speed = self.floatingDx
            targetCenter = sprite.rect.centerx
            axis = "x"
        elif self.floatingDy != 0:
            distanceToCenter = abs(self.rect.centery - sprite.rect.centery)
            speed = self.floatingDy
            targetCenter = sprite.rect.centery
            axis = "y"

        return distanceToCenter, speed, targetCenter, axis

    def checkHitArrows(self):
        """ remove arrows from hitArrows group if not colliding """
        if self.hitArrows:
            for a in self.hitArrows:
                if not pygame.sprite.collide_rect(self, a):
                    self.hitArrows.remove(a)

    def requestScreenSnd(self, sound):
        """ only play these sounds if on screen """
        if self.rect.right > 0 \
            and self.rect.left < self.game.screen.get_width() \
            and self.rect.bottom > 0 \
            and self.rect.top < self.game.screen.get_height():

            soundFx56.GameSoundManager.registerSound(sound)

    def spin(self):
        """ rotate image """
        self.spinDistance += self.spinStep
        if self.spinStep > 0:
            if self.spinDistance >= 360:
                startHere = self.spinDistance - 360
                self.spinDistance = startHere   # reset spinDistance
        else:
            if self.spinDistance <= -360:
                starHere = self.spinDistance + 360
                self.spinDistance = starHere

        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.spinDistance)

class DinoStandard(Dino):
    """ a big-sized spinning velociraptor """

    colors = None # [ [ frame1, frame2 ] etc ] ]
    colorsWithHat = None # same as above but with hat images for bonus mode


    def __init__(self, game, floatingSpeed, spawnKey, delay, objColor, _fps):
        Dino.__init__(self, game, floatingSpeed, spawnKey, delay)

        self.frame = 0
        self.frameDelay = FRAME_DELAY
        self.bounceDelay = BOUNCE_DELAY
        self.inertiaSpinStep = INERTIA_SPIN_STEP
        self.inertiaSpinJump = INERTIA_SPIN_JUMP
        self.inertiaSpinDelay = INERTIA_SPIN_DELAY

        if _fps == 60:
            self.frameDelay *= 2
            self.bounceDelay *= 2
            self.inertiaSpinStep /= 2
            self.inertiaSpinJump /= 2
            self.inertiaSpinDelay *= 2

        self.maxSpin = self.spinRange + self.inertiaSpinJump

        self.frameTick = self.frameDelay
        self.bounceTime = self.bounceDelay
        self.isBouncing = False
        self.hasSpinInertia = False
        self.inertiaSpinTime = self.inertiaSpinDelay

        self.colorIndex = self.setColor(objColor)  # color attr and colorIndex
        self.loadImages()
        self.rect = pygame.Rect(0,0,20,20)
        self.rect.center = Dino.OFFSCREEN

    def update(self):
        Dino.update(self)

        self.frameTick -= 1
        if self.frameTick < 1:
            self.changeFrame()
            self.frameTick = self.frameDelay
        if self.isBouncing:
            self.bounce()
        if self.hasSpinInertia:
            self.tickSpinInertia("d")

    @staticmethod
    def wipe():

        Dino.wipe()
        DinoStandard.colors = None

    def setColor(self, objColor):
        self.objColor = objColor # green, blue, red, yellow

        if objColor == "green":
            colorIndex = 0
        elif objColor == "blue":
            colorIndex = 1
        elif objColor == "red":
            colorIndex = 2
        elif objColor == "yellow":
            colorIndex = 3
        else:
            print "color not recognized\n"

        return colorIndex

    def loadImages(self):
        """ load images for color change """

        if not DinoStandard.colors:

            DinoStandard.colors = []
            DinoStandard.colorsWithHat = []
            fileName = ""

            for i in range(4):
                frames = []
                framesWithHat = []
                if i == 0:
                    fileName = "dCG"
                elif i == 1:
                    fileName = "dCB"
                elif i == 2:
                    fileName = "dCR"
                elif i == 3:
                    fileName = "dCY"

                for j in range(2):
                    imageFile = fileName + str(j + 1) +  ".png" # generate a unique file name
                    imageFileWithHat = fileName + str(j + 1) + HAT_MODE + ".png" # for hats mode
                    image = dinosInSpace.loadImage(imageFile, DINOSCALE, (0,0))
                    imageWithHat = dinosInSpace.loadImage(imageFileWithHat, DINOSCALE, (0,0))
                    frames.append(image)
                    framesWithHat.append(imageWithHat)

                DinoStandard.colors.append(frames)
                DinoStandard.colorsWithHat.append(framesWithHat)

        if modeSwitch.ModeSwitch.modes["HATS"]:
            self.image = DinoStandard.colorsWithHat[self.colorIndex][self.frame]
            self.original = self.image.copy()
            self.myFrames = DinoStandard.colorsWithHat # added for hats mode
        else:
            self.image = DinoStandard.colors[self.colorIndex][self.frame]
            self.original = self.image.copy()  # might not be needed - could be used to simplify spin() method ...
            self.myFrames = DinoStandard.colors # added for hats mode

    def changeFrame(self):
        self.frame += 1
        if self.frame > len(self.myFrames[self.colorIndex]):
            self.frame = 1

    def newDirection(self, sprite, targetCenter, axis, floatingDx, floatingDy):
        """ extend parent method to make graphic 'bounce' """
        Dino.newDirection(self, sprite, targetCenter, axis, floatingDx, floatingDy)
        self.boing()

    def boing(self):
        """ graphical effect of dino hitting an arrow """
        self.isBouncing = True
        self.hasSpinInertia = True
        self.spinStep += self.inertiaSpinJump
        self.bounce()
        self.tickSpinInertia("d")

    def activate(self):
        """ bring the object into the game """  # todo: modify so doesn't have to have spawn...
        soundFx56.GameSoundManager.registerSound("appear")
        self.rect.center = static56.Spawn.spawnDict[self.spawnKey].rect.center
        self.setSpin(-5,5)
        self.active = True

        Dino.activeGroup.add(self)

    def bounce(self):
        """ enlarge the graphic for a short time """
        self.image = DinoStandard.colors[self.colorIndex][self.frame - 1]
        self.image = pygame.transform.scale(self.image, (125,125))
        self.image = pygame.transform.rotate(self.image, self.spinDistance)
        self.bounceTime -= 1

        if self.bounceTime < 1:
            self.isBouncing = False
            self.bounceTime = self.bounceDelay

    def tickSpinInertia(self, iMode):
        """ modify spin step by accel ('a') or deccel ('d') """

        if iMode == "d":
            self.inertiaSpinTime -= 1
            if self.inertiaSpinTime < 1:
                self.inertiaSpinTime = self.inertiaSpinDelay
                self.spinStep -= self.inertiaSpinStep
                if math.fabs(self.spinStep) <= math.fabs(self.defaultSpinStep):
                    self.spinStep = self.defaultSpinStep
                    self.hasInertia = False

    def spin(self): #### just re-wrote the whole method for now... todo: clean this up!
        """ rotate image -- now with colors """

        if math.fabs(self.spinStep) > self.maxSpin:
            if self.spinStep < 0:
                self.spinStep = -self.maxSpin
            else:
                self.spinStep = self.maxSpin

        self.spinDistance += self.spinStep

        if self.spinStep > 0:
            if self.spinDistance >= 360:
                startHere = self.spinDistance - 360
                self.spinDistance = startHere   # reset spinDistance
        else:
            if self.spinDistance <= -360:
                starHere = self.spinDistance + 360
                self.spinDistance = starHere

        image = self.myFrames[self.colorIndex][self.frame - 1]    # get the colored image
        self.image = pygame.transform.rotate(image, self.spinDistance)

        ### alpha fading if running into station
        if self.alpha < 255 and self.alpha >= 0: # and not self.isFlashing for death animation
            self.image.set_alpha(self.alpha)



class DinoDelux(DinoStandard):
    """ takes launchSpeed which is ONE int that will be converted to
        floatingSpeed tuple """
    REF_TOTAL = 0
    REF_DATA = []

    def __init__(self, game, launchSpeed, spawnKey, delay, objColor, _fps):
        DinoDelux.REF_DATA.append((game, launchSpeed, spawnKey, delay, objColor, _fps))
        DinoStandard.__init__(self, game, None, spawnKey, delay, objColor, _fps)
        self.launchSpeed = launchSpeed # this time it's ONE number

    @staticmethod
    def wipe():
        DinoStandard.wipe()
        DinoDelux.REF_TOTAL = 0
        DinoDelux.REF_DATA = []

    @staticmethod
    def setREF_TOTAL():
        DinoDelux.REF_TOTAL = Dino.totalCount

    @staticmethod
    def quickReset():
        for d in Dino.dinoGroup:
            d.killMe()
        Dino.lost = 0
        Dino.totalCount = 0
        Dino.packetGroup.empty()

        for i in range(DinoDelux.REF_TOTAL):
            game, launchSpeed, spawnKey, delay, objColor, _fps = DinoDelux.REF_DATA[i]
            DinoDelux(game, launchSpeed, spawnKey, delay, objColor, _fps)
        Dino.setPaDepth(Dino.PA_DEPTH)

    def activate(self):
        """ bring the object into the game """
        soundFx56.GameSoundManager.registerSound("appear")
        spawn = static56.Spawn.spawnDict[self.spawnKey]
        self.rect.center = spawn.rect.center
        #####################################################################################
        self.setSpin(-self.spinRange, self.spinRange)
        if self.spinStep < 0:
            self.inertiaSpinJump *= -1
            self.inertiaSpinStep *= -1

        #####################
        self.active = True

        floatingSpeed = self.getFloatingSpeed(spawn)
        self.setFloatingSpeed(floatingSpeed)

        Dino.activeGroup.add(self)

        # remove spawn slot from my spawn
        spawn.hideSlot() # spawn keeps track of which slot

    def getFloatingSpeed(self, spawn):

        d = spawn.getDirection()

        if d == Dino.NORTH:
            floatingSpeed = (0, (-self.launchSpeed))
        elif d == Dino.EAST:
            floatingSpeed = ((self.launchSpeed), 0)
        elif d == Dino.SOUTH:
            floatingSpeed = (0, (self.launchSpeed))
        elif d == Dino.WEST:
            floatingSpeed = ((-self.launchSpeed), 0)
        return floatingSpeed

def buildDinoSet(game, setData, _fps):
    """ returns set of dinos """
    dType, num, color, speed, spawn, delayStart, delayStep = setData

    if _fps == 30:
        speed*=2
    if dType == "standard":
        clas = DinoStandard
    if dType == "delux":
        clas = DinoDelux

    dinos = []
    for n in range(num):
        delayStart += delayStep
        d = clas(game, speed, spawn, delayStart, color, _fps)
        dinos.append(d)

    return dinos

def wipe():
    Dino.wipe()
    DinoStandard.wipe()
    DinoDelux.wipe()
