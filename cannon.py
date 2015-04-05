""" cannon.py """

import pygame
import random

# default cannon vales
D_POS = (100,100)   # starting position
D_STEP = 30         # fps b/w shots
D_STEPVAR = 10      # variation range of step
D_FLSPEED = (10,0)  # speed of flyers (pixels per frame)
D_FLSPIN = 5        # spin step of flyers (deg rotation per frame)
D_FLEDGE = "R"

class Cannon(object):
    """ 'launches' Flyer objects across screen """

    def __init__(self, group, flyers, pos=D_POS, step=D_STEP, var=D_STEPVAR, speed=D_FLSPEED, spin=D_FLSPIN, edge=D_FLEDGE, customBounds=None, terminal=False):

        self.group = group # pygame group
        self.flyers = flyers # list of flyer surfaces, if list > 1, animate list
        self.flyerSize = self.flyers[0].get_size()
        self.pos = pos
        self.step = step # int
        self.stepVar = var # int
        self.flyerSpeed = speed # (int_x, int_y)
        self.flyerSpin = spin # int
        self.flyerEdge = edge # "L" | "R" | "T" | "B"
        self.customBounds = customBounds
        self.terminal = terminal
        self.inactive = False

        self.screen = pygame.display.get_surface()

        self.countDown = 0
        self.frameStep = 1 # override default by setter
        self.jumpX = False # override default by setter
        self.jumpY = False # override default by setter

    def update(self):
        if self.countDown <= 0:
            self.launch()
            self.setCount()

        self.tick()

    # --------------- setters default (call to override init values)

    def setPos(self, pos):
        self.pos = pos

    def setStep(self, pos):
        self.pos = pos

    def setStepVar(self, stepVar):
        self.stepVar = stepVar

    def setFlyerSpeed(self, flyerSpeed):
        self.flyerSpeed = flyerSpeed

    def setFlyerSpin(self, flyerSpin):
        self.flyerSpin = flyerSpin

    def setFrameStep(self, frameStep):
        self.frameStep = frameStep

    def setCountDown(self, countDown):
        self.countDown = countDown

    def setJump(self, axis):
        if axis == "x":
            self.jumpX = True
        elif axis == "y":
            self.jumpY = True
        elif axis == "xy":
            self.jumpX = True
            self.jumpY = True

    # --------------- setters internal

    def setCount(self):
        if self.stepVar:
            self.countDown = self.step + random.randrange(-self.stepVar, self.stepVar)
        else:
            self.countDown = self.step

    # --------------- other methods

    def tick(self):
        self.countDown -= 1

    def launch(self):
        if not self.inactive:
            f = Flyer(self.group, self.flyers, self.flyerSpeed, self.flyerSpin, self.pos)

            if self.flyerEdge:
                f.setEdge(self.flyerEdge, self.customBounds)

            if len(self.flyers) > 1:
                f.setFrameStep(self.frameStep)

            if self.jumpX:
                self.pos[0] = random.randrange(0,self.screen.get_width() - self.flyerSize[0])

            if self.jumpY:
                self.pos[1] = random.randrange(0,self.screen.get_height() - self.flyerSize[1])

            if self.terminal:
                self.inactive = True

class Flyer(pygame.sprite.Sprite):
    """ object to be launched out of cannon """

    def __init__(self, group, frames, speed, spin, launchFrom):
        pygame.sprite.Sprite.__init__(self, group)

        self.frames = frames
        self.image = self.frames[0]
        self.currentFrame = 0
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.center = launchFrom

        self.spinStep = spin
        self.spinDistance = 0

        self.edge = None  # set by caller
        self.bound = None # set in edge setter
        self.frameStep = None # set by caller
        self.FRAMEDELAY = None # set in frameStep setter
        self.animate = False

    def update(self):
        self.move()
        if self.edge:
            self.checkEdge()
        if self.animate:
            self.tickFrameStep()
        if self.spinStep:
            self.spin()

    def setEdge(self, edge, customBounds):
        if edge == "L":
            self.bound = 0
        elif edge == "R":
            self.bound = pygame.display.get_surface().get_width()
        elif edge == "T":
            self.bound = 0
        elif edge == "B":
            self.bound = pygame.display.get_surface().get_height()

        if customBounds:
            self.bound = customBounds

        self.edge = edge

    def setFrameStep(self, frameStep):
        self.frameStep = frameStep
        self.FRAMEDELAY = self.frameStep
        self.animate = True

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]

    def tickFrameStep(self):
        if self.frameStep < 1:
            self.frameStep = self.FRAMEDELAY
            self.changeFrame()

        self.frameStep -= 1

    def changeFrame(self):
        self.currentFrame += 1
        if self.currentFrame >= len(self.frames):
            self.currentFrame = 0

    def checkEdge(self):
        if self.edge == "L":
            if self.rect.right < self.bound:
                self.destroy()
        elif self.edge == "R":
            if self.rect.left > self.bound:
                self.destroy()
        elif self.edge == "T":
            if self.rect.bottom < self.bound:
                self.destroy()
        elif self.edge == "B":
            if self.rect.top > self.bound:
                self.destroy()

    def spin(self):
        """ rotate image """
        self.spinDistance += self.spinStep

        if self.spinStep > 0:
            if self.spinDistance >= 360:
                self.spinDistance -= 360
        else:
            if self.spinDistance <= -360:
                self.spinDistance += 360

        self.image = pygame.transform.rotate(self.frames[self.currentFrame], self.spinDistance)

    def destroy(self):
        self.kill()

if __name__ == '__main__':
    print "module meant for import only"