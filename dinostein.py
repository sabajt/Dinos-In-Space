""" dinostein.py
    the animated tween sprite that accompaines the end message
"""
import dinosInSpace
import tween

CLOSING_FRAME_ROOT = "dinosteinFrameSeq"
TOTALCLOSING = 18

DINO_FRAMENAMES = [
    "dinostein0000.png",
    "dinostein0001.png",
    "dinostein0002.png",
    "dinostein0003.png"
]

#FRAME_FRAMENAMES = [
#    "dinosteinFrame0000.png",
#    "dinosteinFrame0001.png"
#]
FRAME_IMAGE_FILE = "dinosteinFrame0000.png"

CLOSING_FRAME_ROOT  = "dinosteinFrameSeq"
TOTALCLOSING        = 18

ALPHA               = 200 # sync with automessage and endMessage ALPHA

TWEEN_Y             = 450
TWEEN_XSTART        = -130
TWEEN_XEND          = 100
TWEEN_SPEED         = 25
TWEEN_DCLVAL        = 1
TWEEN_LIMVAR        = 1

DINO_DELAY          = 5
DINO_ARMDELAY       = 35
DINO_HOLDLEN        = 10

FRAME_DELAY         = 4


class Dinostein(tween.TweenMenu):
    """ Dr. Dinostein himself """
    FRAMES = []

    def __init__(self, _fps):
        tween.TweenMenu.__init__(self)
        self._fps = _fps

        if not Dinostein.FRAMES:
            for f in DINO_FRAMENAMES:
                Dinostein.FRAMES.append(dinosInSpace.loadImage(f, "2X", (0,0), ALPHA))

        self.frames = Dinostein.FRAMES
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        self.frameDelay = DINO_DELAY
        self.armDelay = DINO_ARMDELAY
        self.holdDelay = DINO_HOLDLEN

        if self._fps == 60:
            self.frameDelay *= 2
            self.armDelay *= 2
            self.holdDelay *= 2
        self.frameTick = self.frameDelay
        self.armTick = self.armDelay
        self.holdTick = self.holdDelay

        self.mouthOpen = False
        self.armUp = False
        self.firstCycle = True

    def setAndStartTween(self):
        # set and start tween
        speed = TWEEN_SPEED
        val = TWEEN_DCLVAL
        lim = TWEEN_LIMVAR
        if self._fps == 30:
            speed *= 2

        self.setTween((TWEEN_XSTART, TWEEN_Y), (TWEEN_XEND, TWEEN_Y), speed, "EXP", val, lim)
        self.startTween()

    def update(self):
        if not self.firstCycle:
            tween.TweenMenu.update(self)
            self.animateTalk()
            self.animateArm()
        else:
            self.firstCycle = False

    def updateEnding(self):
        """ for functionality with endMessage.py """
        pass


    def updateMessage(self):
        """ callback for functionality with autoMessage """
        pass

    def animateTalk(self):
        self.frameTick -= 1
        if self.frameTick <= 0:
            if self.mouthOpen:
                self.mouthOpen = False
                self.image = self.frames[0]
            else:
                self.mouthOpen = True
                self.image = self.frames[1]
            self.frameTick = self.frameDelay

    def animateArm(self):
        if not self.armUp:
            self.armTick -= 1
            if self.armTick <= 0:
                self.armTick = self.armDelay
                self.armUp = True
                if self.mouthOpen:
                    self.image = self.frames[3]
                else:
                    self.image = self.frames[2]
        else:
            self.holdTick -= 1
            if self.holdTick <= 0:
                self.holdTick = self.holdDelay
                self.armUp = False
                if self.mouthOpen:
                    self.image = self.frames[1]
                else:
                    self.image = self.frames[0]


class Frame(tween.TweenFollower):
    """ Dinostein's animated 'video box'
        -intended to be added to Dinostein as follower outside of class
    """
#    FRAMES = []
    IMAGE = None
    FRAMES_CLOSING = []

    def __init__(self, _fps):
        tween.TweenFollower.__init__(self, (0,0))

        self._fps = _fps

#        if not Frame.FRAMES:
#            for f in FRAME_FRAMENAMES:
#                Frame.FRAMES.append(dinosInSpace.loadImage(f, "2X", (0,0), ALPHA))
        if not Frame.IMAGE:
            Frame.IMAGE = dinosInSpace.loadImage(FRAME_IMAGE_FILE, "2X", (0,0), ALPHA)

        if not Frame.FRAMES_CLOSING:
            frameCount = 0
            for f in range(TOTALCLOSING):
                prefix = "000"
                if frameCount >= 10:
                    prefix = "00"
                fileName = CLOSING_FRAME_ROOT + prefix + str(frameCount) + ".png"
                Frame.FRAMES_CLOSING.append(dinosInSpace.loadImage(fileName, "2X", (0,0), ALPHA))
                frameCount += 1

#        self.image = Frame.FRAMES[0]
        self.image = Frame.IMAGE.copy()
        self.rect = self.image.get_rect()

#        self.frameDelay = FRAME_DELAY
#        if self._fps == 60:
#            self.frameDelay *= 2
#        self.frameTick = self.frameDelay
        self.closingFrameIndex = 0
        self.closing = False

    def update(self):
        tween.TweenFollower.update(self)
        if self.closing:
            self.animateClosing()
#        else:
#            self.animate()

    def updateEnding(self):
        pass

    def updateMessage(self):
        pass

#    def animate(self):
#        self.frameTick -= 1
#        if self.frameTick <= 0:
#            self.frameTick = self.frameDelay
#            if self.image == Frame.FRAMES[0]:
#                self.image = Frame.FRAMES[1]
#            else:
#                self.image = Frame.FRAMES[0]

    def animateClosing(self):
        if self.closingFrameIndex < TOTALCLOSING:
            self.image = Frame.FRAMES_CLOSING[self.closingFrameIndex]
            if self._fps == 60:
                self.closingFrameIndex += 1
            else:
                self.closingFrameIndex += 2

if __name__ == '__main__':
    print "module for import only"
