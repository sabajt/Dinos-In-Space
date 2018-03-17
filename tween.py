"""
    tween.py

    classes for sprites that can be programmed to travel between points
"""

import pygame
import math
import infoGraphic56

class TweenSprite(pygame.sprite.Sprite):
    """
        basic sprite that travels between to points
        - uses center of rect as node
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.startPoint         = None
        self.endPoint           = None
        self.dx                 = None
        self.dy                 = None
        self.xDirection         = None
        self.yDirection         = None
        self.xSubStep           = None
        self.ySubStep           = None
#        self.speed              = 1
#        self.skipStep           = 1
#        self.stepCycle          = 0
        self.reached_x          = False
        self.reached_y          = False
        self.reached_dest       = False
        self.hasStartedTween    = False

        self.subNumber = 1

    def update(self):
        if self.hasStartedTween:
            if not self.reached_dest:
                self.move()
                self.checkReachedDest()

    def clearVals(self):
        self.startPoint         = None
        self.endPoint           = None
        self.dx                 = None
        self.dy                 = None
        self.xDirection         = None
        self.yDirection         = None
        self.xSubStep           = None
        self.ySubStep           = None
        #        self.speed              = 1
        #        self.skipStep           = 1
        #        self.stepCycle          = 0
        self.reached_x          = False
        self.reached_y          = False
        self.reached_dest       = False
        self.hasStartedTween    = False
        self.subNumber = 1

    def setTween(self, startPoint, endPoint, speed):
        """ shortcut for calling setStartPoint, setEndPoint and calculate movement """
        self.setStartPoint(startPoint)
        self.setEndPoint(endPoint)
        self.calculateMovement()
    #self.calculateSpeed(speed)

    def move(self):
        addToX, addToY = self.checkSubPoints()

        if not self.reached_x:
            self.rect.centerx += (self.dx + addToX)
        if not self.reached_y:
            self.rect.centery += (self.dy + addToY)

#        if not self.reached_x:
#            if self.skipAxis == "x":
#                if self.checkSkipStep():
#                    self.rect.centerx += self.dx
#            else:
#                self.rect.centerx += self.dx
#            self.rect.centerx += addToX
#
#        if not self.reached_y:
#            if self.skipAxis == "y":
#                if self.checkSkipStep():
#                    self.rect.centery += self.dy
#            else:
#                self.rect.centery += self.dy
#            self.rect.centery += addToY

    def jumpTo(self, point):
        self.rect.center = point

    def setStartPoint(self, point):
        self.startPoint = point

    def setEndPoint(self, point):
        self.endPoint = point

    def calculateMovement(self):

        # calculate direction moving and direction multiplier (dx/dyCorrection)
        self.dxCorrection = 0
        self.dyCorrection = 0

        if self.endPoint[0] > self.startPoint[0]:
            self.xDirection = "right"
            self.dxCorrection = 1
        elif self.endPoint[0] < self.startPoint[0]:
            self.xDirection = "left"
            self.dxCorrection = -1

        if self.endPoint[1] > self.startPoint[1]:
            self.yDirection = "down"
            self.dyCorrection = 1
        elif self.endPoint[1] < self.startPoint[1]:
            self.yDirection = "up"
            self.dyCorrection = -1

        # calculate distance to move, relative speed, and substep movement if needed
        xDist = int(math.fabs(self.endPoint[0] - self.startPoint[0]))
        yDist = int(math.fabs(self.endPoint[1] - self.startPoint[1]))

        if xDist > yDist:
            if yDist != 0:
                self.dx = xDist / yDist
                self.dy = 1
                self.xSubStep = self.getSubStep(xDist, yDist)
            else:
                self.dx = 1
                self.dy = 0
        elif yDist > xDist:
            if xDist != 0:
                self.dx = 1
                self.dy = yDist / xDist
                self.ySubStep = self.getSubStep(yDist, xDist)
            else:
                self.dx = 0
                self.dy = 1
        else:
            self.dx = 1
            self.dy = 1

        self.dx *= self.dxCorrection
        self.dy *= self.dyCorrection

        if self.xSubStep:
            self.xSubStep *= self.dxCorrection
        if self.ySubStep:
            self.ySubStep *= self.dyCorrection

#    def calculateSpeed(self, speed):
#        if math.fabs(self.dx) > math.fabs(self.dy):
#            self.skipStep = self.dx
#            self.skipAxis = "y"
#        else:
#            self.skipStep = self.dy
#            self.skipAxis = "x"
#
#        self.dx = 1
#        self.dy = 1
#
#    def checkSkipStep(self):
#        canMove = False
#
#        if self.skipAxis == "y":
#            if self.rect.centerx >= self.startPoint[0] + (self.stepCycle * self.skipStep):
#                canMove = True
#                self.stepCycle += 1
#
#        elif self.skipAxis == "x":
#            if self.rect.centery >= self.startPoint[1] + (self.stepCycle * self.skipStep):
#                canMove = True
#                self.stepCycle += 1
#
#        return canMove

    def getSubStep(self, greaterDist, lesserDist):
        """
            - creates distance-step for slope ratios with remainders
            - substep made by evenly dividing distance by remainder
            - results in even and accurate tween movement for nasty slope ratios
        """
        subStep = None
        rmdr = greaterDist % lesserDist

        if rmdr != 0:
            subStep = float(greaterDist) / rmdr

#         --------- added for speed control
#        cleanDist = greaterDist - rmdr

        return subStep

    def startTween(self):
        self.jumpTo(self.startPoint)
        self.hasStartedTween = True

    def checkReachedDest(self):
        """ object when end of path is reached """
        if self.xDirection == "right":
            if self.rect.centerx >= self.endPoint[0]:
                self.reached_x = True
        elif self.xDirection == "left":
            if self.rect.centerx <= self.endPoint[0]:
                self.reached_x = True

        if self.yDirection == "down":
            if self.rect.centery >= self.endPoint[1]:
                self.reached_y = True
        elif self.yDirection == "up":
            if self.rect.centery <= self.endPoint[1]:
                self.reached_y = True

        if self.reached_x and self.reached_y:
            self.reached_dest = True

    def checkSubPoints(self):
        addToX = 0
        addToY = 0

        if self.xSubStep:
            if self.xDirection == "right":
                if self.rect.centerx >= self.startPoint[0] + (self.subNumber * self.xSubStep):
                    addToX = 1 # replace 1 later with some var
                    self.subNumber += 1
            elif self.xDirection == "left":
                if self.rect.centerx <= self.startPoint[0] + (self.subNumber * self.xSubStep):
                    addToX = -1
                    self.subNumber += 1

        if self.ySubStep:
            if self.yDirection == "down":
                if self.rect.centery >= self.startPoint[1] + (self.subNumber * self.ySubStep):
                    addToY = 1 # replace 1 later with some var
                    self.subNumber += 1
            elif self.yDirection == "up":
                if self.rect.centery <= self.startPoint[1] + (self.subNumber * self.ySubStep):
                    addToY = -1
                    self.subNumber += 1

        return addToX, addToY

#           startpoint = (0,0),         endpoint = (100,500),

class TweenLeader(TweenSprite):
    """
        adds follower functionality to TweenSprite
        - followers mimic every movement of leader
        - followers must be subclass of TweenFollower
    """

    def __init__(self):
        TweenSprite.__init__(self)

        self.followers = []

    def update(self):
        """ overrides to replace move() with moveAndBroadcast() """
        if self.hasStartedTween:
            if not self.reached_dest:
                self.moveAndBroadcast()
                self.checkReachedDest()

    def startTween(self):
        """ overrides to position followers """
        TweenSprite.startTween(self)
        for f in self.followers:
            f.jumpTo(self.startPoint)

    def addFollower(self, f):
        self.followers.append(f)

    def moveAndBroadcast(self):
        """ moves self and broadcasts moves to followers """
        addToX, addToY = self.checkSubPoints()

        if not self.reached_x:
            self.rect.centerx += (self.dx + addToX)
            for f in self.followers:
                f.moveFollower("x", self.dx + addToX)

        if not self.reached_y:
            self.rect.centery += (self.dy + addToY)
            for f in self.followers:
                f.moveFollower("y", self.dy + addToY)

#        if not self.reached_x:
#            if self.skipAxis == "x":
#                if self.checkSkipStep():
#                    self.rect.centerx += self.dx
#                    for f in self.followers:
#                        f.moveFollower("x", self.dx)
#            else:
#                self.rect.centerx += self.dx
#                for f in self.followers:
#                    f.moveFollower("x", self.dx)
#            self.rect.centerx += addToX
#            for f in self.followers:
#                f.moveFollower("x", addToX)
#
#        if not self.reached_y:
#            if self.skipAxis == "y":
#                if self.checkSkipStep():
#                    self.rect.centery += self.dy
#                    for f in self.followers:
#                        f.moveFollower("y", self.dy)
#            else:
#                self.rect.centery += self.dy
#                for f in self.followers:
#                    f.moveFollower("y", self.dy)
#            self.rect.centery += addToY
#            for f in self.followers:
#                f.moveFollower("y", addToY)

    def clearFollowers(self):
        for f in self.followers:
            f.kill()

        self.followers = []


class TweenFollower(pygame.sprite.Sprite):
    """ superclass for followers of a TweenLeader """

    def __init__(self, relPos):
        pygame.sprite.Sprite.__init__(self)

        self.relPos = relPos

    def moveFollower(self, axis, distance):
        """ meant to be called by leader to mimic motion """
        if axis == "x":
            self.rect.centerx += distance
        elif axis == "y":
            self.rect.centery += distance

    def jumpTo(self, relToPoint):
        self.rect.center = (relToPoint[0] + self.relPos[0], relToPoint[1] + self.relPos[1])


# ********************* targeted classes ************************

class TweenMenu(TweenLeader):
    """
        TweenLeader meant to be used as swoop in menu
        - can only move left, right, up and down
        - setTween takes 3 additional args used for deceleration:
            dclMode -> str 'EXP' or 'LIN' determines type of deceleration
            dclVal  -> float between 0 and 1 or int > 1 depending on mode
            limVar  -> int multiplier that determines how close to edge decel starts
    """

    def update(self):
        """ overrides to include deceleration """
        if self.hasStartedTween:
            if not self.reached_dest:
                if self.isDecelerating:
                    self.decel()
                else:
                    self.checkDclLim()

                self.moveAndBroadcast()
                self.checkReachedDest()
       

    def setTween(self, startPoint, endPoint, speed, dclMode, dclVal, limVar):
        """ overrides to include speed, deceleration and asserts l,r,u,d movement """
        assert((endPoint[0] - startPoint[0] == 0) or (endPoint[1] - startPoint[1] == 0))

        # -- new attributes
        self.speed          = speed
        self.isDecelerating = False
        self.dclMode        = dclMode
        self.dclVal         = dclVal
        self.limVar         = limVar
        self.movingAxis     = None
        self.dclLim         = None

        self.setStartPoint(startPoint)
        self.setEndPoint(endPoint)
        self.calculateMovement()
        self.calculateAndSetSpeed()
        self.calculateDcl()

    def calculateAndSetSpeed(self):
        if self.dx != 0:
            self.dx *= self.speed
            self.movingAxis = "x"
        if self.dy != 0:
            self.dy *= self.speed
            self.movingAxis = "y"

    def calculateDcl(self):
        if self.dclMode == "LIN":
            assert(self.dclVal > 0)
        elif self.dclMode == "EXP":
            assert(self.dclVal > 0)
            self.dclLim = self.speed * self.limVar
        else:
            print("dclMode must be 'LIN' or 'EXP'")

    def decel(self):
        if self.dclMode == "EXP":
            self.dx *= self.dclVal
            self.dy *= self.dclVal

        if self.movingAxis == "x":
            if math.fabs(self.dx) < 1:
                self.dx = self.dxCorrection
        else:
            if math.fabs(self.dy) < 1:
                self.dy = self.dyCorrection

    def checkDclLim(self):
        if self.movingAxis == "x":
            loc = self.rect.centerx
            end = self.endPoint[0]
        else:
            loc = self.rect.centery
            end = self.endPoint[1]

        if self.dclMode == "EXP":
            if end < 0: # bug fix for flying offscreen to the left or up
                dif = math.fabs(math.fabs(loc) + math.fabs(end))
            else:
                dif = math.fabs(math.fabs(loc) - math.fabs(end))

            if dif <= self.dclLim:
                self.isDecelerating = True

    def reset(self):
        self.clearFollowers()
        self.clearVals()

class TweenYN(TweenMenu):

    def __init__(self, boxSize, boxColor, fontSize, fontColor, alpha=None):
        TweenMenu.__init__(self)

        self.textSurf1  = infoGraphic56.TextObject("DELETE DATA?", fontSize, fontColor).image
        self.textSurf2  = infoGraphic56.TextObject("Y / N", fontSize, fontColor).image
        self.image      = pygame.Surface(boxSize)
        self.rect       = self.image.get_rect()

        t1_w            = self.textSurf1.get_width()
        t2_w            = self.textSurf2.get_width()
        text_h          = self.textSurf1.get_height()
        box_xMid        = self.image.get_width()/2
        box_h           = self.image.get_height()

        self.image.fill(boxColor)
        self.image.blit(self.textSurf1, (box_xMid - t1_w/2, box_h/3 - text_h/2))
        self.image.blit(self.textSurf2, (box_xMid - t2_w/2, 2*box_h/3 - text_h/2))

        if alpha:
            self.image.set_alpha(alpha, pygame.RLEACCEL)

        # set and start tween

        self.setTween((1000,300), (400,300), 45, "EXP", 0.55, 3)
        self.startTween()


























