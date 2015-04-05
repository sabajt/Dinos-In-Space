"""
    snack.py
    defines Snack class - collectible objects in puzzles
"""

import pygame
import static56
import groupMods56
import dinosInSpace
import scroller56
import endMessage
import soundFx56

SPIN_STEP = -1
DEFAULT_ALPHA = 190
HIDE_ALPHA = 90

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:

            ImgLib.imgDict = {

                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
                # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| add snax ||||||||||||||||||||||||||||||||||||||||
                # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

##                "TESTSNACK" : dinosInSpace.loadImage("blueSquare.png", (50,50)),
##                "BLUESNAX" : dinosInSpace.loadImage("blueSquare.png", (50,50)),
##                "GREENSNAX" : dinosInSpace.loadImage("greenSquare.png", (50,50)),
##                "PINKSNAX" : dinosInSpace.loadImage("pinkSquare.png", (50,50)),
##                "REDSNAX" : dinosInSpace.loadImage("redSquare.png", (50,50)),
##                "PURPLESNAX" : dinosInSpace.loadImage("purpleSquare.png", (50,50)),

#                "S_PIZZA" : dinosInSpace.loadImage("s_pizza.png", "2X", (0,0)),
#                "S_SALAMI" : dinosInSpace.loadImage("s_salami.png", "2X", (0,0)),
#                "S_SHRIMP" : dinosInSpace.loadImage("s_shrimp.png", "2X", (0,0)),
#                "S_BROCCOLI" : dinosInSpace.loadImage("s_broc.png", "2X", (0,0)),
#                "S_MAC_N'_CHEESE" : dinosInSpace.loadImage("s_mac.png", "2X", (0,0)),
#                "S_CORN_CRUNCHIES" : dinosInSpace.loadImage("s_corn_crunchies.png", "2X", (0,0)),
#                "S_SUGAR_PUFZ" : dinosInSpace.loadImage("s_sugar_pufz.png", "2X", (0,0)),
#                "S_PB_CUBES" : dinosInSpace.loadImage("s_pb_cubes.png", "2X", (0,0)),
#                "S_BBQ_TWISTS" : dinosInSpace.loadImage("s_bbq_twists.png", "2X", (0,0))

                "barbequarks" : dinosInSpace.loadImage("s_barbequarks.png", "2X", (0,0)),
                "broccolibanana" : dinosInSpace.loadImage("s_broccolibanana.png", "2X", (0,0)),
                "candydough" : dinosInSpace.loadImage("s_candydough.png", "2X", (0,0)),
                "cheese zees" : dinosInSpace.loadImage("s_cheese_zees.png", "2X", (0,0)),
                "chocobeanz" : dinosInSpace.loadImage("s_chocobeanz.png", "2X", (0,0)),
                "fizzy beerwafers" : dinosInSpace.loadImage("s_fizzy_beerwafers.png", "2X", (0,0)),
                "funtarts" : dinosInSpace.loadImage("s_funtarts.png", "2X", (0,0)),
                "grade a milk" : dinosInSpace.loadImage("s_grade_a_milk.png", "2X", (0,0)),
                "hexberries" : dinosInSpace.loadImage("s_hexberries.png", "2X", (0,0)),
                "joybacon" : dinosInSpace.loadImage("s_joybacon.png", "2X", (0,0)),
                "lazercut fries" : dinosInSpace.loadImage("s_lazercut_fries.png", "2X", (0,0)),
                "lucky coffee" : dinosInSpace.loadImage("s_lucky_coffee.png", "2X", (0,0)),
                "marshmelons" : dinosInSpace.loadImage("s_marshmelons.png", "2X", (0,0)),
                "monster biscuits" : dinosInSpace.loadImage("s_monster_biscuits.png", "2X", (0,0)),
                "munchzilla" : dinosInSpace.loadImage("s_munchzilla.png", "2X", (0,0)),
                "nanocorn" : dinosInSpace.loadImage("s_nanocorn.png", "2X", (0,0)),
                "penutbutter cubes" : dinosInSpace.loadImage("s_penutbutter_cubes.png", "2X", (0,0)),
                "picklesicle" : dinosInSpace.loadImage("s_picklesicle.png", "2X", (0,0)),
                "pizzaballoon" : dinosInSpace.loadImage("s_pizzaballoon.png", "2X", (0,0)),
                "shrimp nuggets" : dinosInSpace.loadImage("s_shrimp_nuggets.png", "2X", (0,0)),
                "sugar pufz" : dinosInSpace.loadImage("s_sugar_pufz.png", "2X", (0,0)),
                "sushi yumyum cone" : dinosInSpace.loadImage("s_sushi_yumyum_cone.png", "2X", (0,0)),
                "xtremophile gummies" : dinosInSpace.loadImage("s_xtremophile_gummies.png", "2X", (0,0)),
                "yumzingers" : dinosInSpace.loadImage("s_yumzingers.png", "2X", (0,0)),

            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image, " + name + " not found"

def initImgLib():
    ImgLib()

class Snack(pygame.sprite.Sprite):
    """ collectable that unlocks features in profile """
    snaxGroup = groupMods56.SR_OrderedUpdates()
    registered = {} # holds init data for snax: used for re-creation (quick reset)

    def __init__(self, imageKey, gridPos, index, linkedStateDefault=None):
        pygame.sprite.Sprite.__init__(self)

        self.minSpeed           = dinosInSpace.Game.getMinSpeed()
        self.image              = ImgLib.getImage(imageKey)
        self.image.set_alpha(DEFAULT_ALPHA, pygame.RLEACCEL)
        self.original           = self.image.copy()
        self.rect               = self.image.get_rect()
        centerFix               = (100 - self.image.get_size()[0])/2
        xBottomR                = static56.gridToCoord(gridPos)[0] - centerFix
        yBottomR                = static56.gridToCoord(gridPos)[1] - centerFix
        self.rect.bottomright   = (xBottomR, yBottomR)
        self.index              = index
        self.imageKey           = imageKey
        self.gridPos            = gridPos
        self.avaliable          = True
        self.spinStep           = SPIN_STEP
        self.spinDistance       = 0
        self.linkedStateDefault = linkedStateDefault
        if self.linkedStateDefault:
            self.setState(1)

        Snack.snaxGroup.add(self)

    def update(self):
        self.setSpeed()
        self.spin()

    def register(self):
        """ register for re-creation """
        Snack.registered[self] = [self.imageKey, self.gridPos, self.index, self.linkedStateDefault]

    def unregister(self):
        """ unregister if player wins and has collected snack
            so if player quick resets snack won't reappear """
        if Snack.registered[self]:
            del Snack.registered[self]

    def setSpeed(self):
        xSpeedRatio, ySpeedRatio = scroller56.Scroller.speedData
        dx = xSpeedRatio * self.minSpeed
        dy = ySpeedRatio * self.minSpeed
        self.rect.centerx += dx
        self.rect.centery += dy

    def collect(self):
        """ collects snack if avaliable, returns True or False for success
            - called by dino.Dino instance during collision
        """
        if self.avaliable:
            soundFx56.GameSoundManager.registerSound("snack")
            endMessage.BonusDelegate.snax.append(self)
            self.kill()
            return True
        else:
            return False

    ### set state for linked snax -- called by switch ###
    def setState(self, state):
        if state == 1:
            if self.linkedStateDefault == "ON":
                self.show()
            else:
                self.hide()
        else:
            if self.linkedStateDefault == "OFF":
                self.show()
            else:
                self.hide()
    #####################################################

    def hide(self):
        self.image.set_alpha(HIDE_ALPHA, pygame.RLEACCEL)
        self.avaliable = False

    def show(self):
        self.image.set_alpha(DEFAULT_ALPHA, pygame.RLEACCEL)
        self.avaliable = True

    def spin(self):
        if self.avaliable:
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


    @staticmethod
    def wipe():
        Snack.snaxGroup = groupMods56.SR_OrderedUpdates()
        Snack.registered = {}

    @staticmethod
    def quickReset():
        for s in Snack.snaxGroup:
            s.kill()

        reSnax = []
        for s in Snack.registered:
            newSnack = Snack(
                Snack.registered[s][0],
                Snack.registered[s][1],
                Snack.registered[s][2],
                Snack.registered[s][3]
            )
            reSnax.append(newSnack)
        Snack.registered = {}

        for s in reSnax:
            s.register()

#def buildSnack(imageKey, gridPos):
#    loc = static56.gridToCoord(gridPos)
#    Snack(imageKey, loc)

def wipe():
    Snack.wipe()


