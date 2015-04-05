import pygame
import dinosInSpace
import random
import math
import fpsSwitch

ABSOLUTE_BOUNDS = ((400 + 50, 0), (800 - 50, 600)) # topleft, bottomright
FRAME_DELAY = 10
SPIN_RANGE = 3
SPEED = (0,2)

class TitleDino(pygame.sprite.Sprite):
    """ top to bottom wrapping, regenerating dino sprite specifically for title screen """
    FRAMES_GREEN = None
    FRAMES_BLUE = None
    FRAMES_RED = None
    FRAMES_YELLOW = None
    def __init__(self, delayStart=0):
        pygame.sprite.Sprite.__init__(self)

        if not TitleDino.FRAMES_GREEN:
            TitleDino.FRAMES_GREEN = [dinosInSpace.loadImage("dCG1.png", "2X", (0,0)), dinosInSpace.loadImage("dCG2.png", "2X", (0,0))]
            TitleDino.FRAMES_BLUE = [dinosInSpace.loadImage("dCB1.png", "2X", (0,0)), dinosInSpace.loadImage("dCB2.png", "2X", (0,0))]
            TitleDino.FRAMES_RED = [dinosInSpace.loadImage("dCR1.png", "2X", (0,0)), dinosInSpace.loadImage("dCR2.png", "2X", (0,0))]
            TitleDino.FRAMES_YELLOW = [dinosInSpace.loadImage("dCY1.png", "2X", (0,0)), dinosInSpace.loadImage("dCY2.png", "2X", (0,0))]

        self.boundTop = ABSOLUTE_BOUNDS[0][1]
        self.boundBottom = ABSOLUTE_BOUNDS[1][1]
        self.boundLeft = ABSOLUTE_BOUNDS[0][0]
        self.boundRight = ABSOLUTE_BOUNDS[1][0]

        self.frameDelay = FRAME_DELAY
        self.delayStart = delayStart
        if fpsSwitch.FPSSwitch._fps == 60:
            self.frameDelay *= 2
            self.delayStart *= 2
        self.frameTick = self.frameDelay
        self.currentFrame = 0
        self.speed = SPEED


        self.spinStep = 0
        while self.spinStep == 0:
            self.spinStep = random.randrange(-SPIN_RANGE, SPIN_RANGE)
        self.spinDistance = 0

        self.frames = None # set in regenerate
        self.image = TitleDino.FRAMES_GREEN[0]
        self.rect = self.image.get_rect()
        self.lastSelection = -1
        self.regenerate()

    def update(self):
        if self.delayStart <= 0:
            self.move()
            self.checkBounds()
            self.animate()
            self.spin()
        else:
            self.delayStart -= 1

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]

    def regenerate(self):

        # pick new frame set / image
        newSelection = self.lastSelection
        while newSelection == self.lastSelection:
            newSelection = random.randrange(1,4)
        self.lastSelection = newSelection

        if self.lastSelection == 1:
            self.frames = TitleDino.FRAMES_GREEN
        elif self.lastSelection == 2:
            self.frames = TitleDino.FRAMES_BLUE
        elif self.lastSelection == 3:
            self.frames = TitleDino.FRAMES_RED
        elif self.lastSelection == 4:
            self.frames = TitleDino.FRAMES_YELLOW

        self.image = self.frames[0]


        # set new location / rect
        new_x = self.rect.centerx
        while math.fabs(self.rect.centerx - new_x) < self.rect.width/2:
            new_x = random.randrange(self.boundLeft, self.boundRight)

        self.rect = self.image.get_rect()
        self.rect.bottom = self.boundTop
        self.rect.centerx = new_x

    def checkBounds(self):
        if self.rect.top >= self.boundBottom:
            self.regenerate()

    def animate(self):
        self.frameTick -= 1
        if self.frameTick <= 0:
            self.frameTick = self.frameDelay
            if self.currentFrame == 0:
                self.currentFrame = 1
            else:
                self.currentFrame = 0

    def spin(self):
        self.spinDistance += self.spinStep

        if self.spinStep > 0:
            if self.spinDistance >= 360:
                startHere = self.spinDistance - 360
                self.spinDistance = startHere
        else:
            if self.spinDistance <= -360:
                starHere = self.spinDistance + 360
                self.spinDistance = starHere

        self.image = pygame.transform.rotate(self.frames[self.currentFrame], self.spinDistance)
