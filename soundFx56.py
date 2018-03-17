"""
    soundFx.py

    class
        SoundPlayer
    function
        wipe
"""
import pygame
import os
import random

class SoundPlayer(object):
    player = None # soundPlayer instance (only 1 at a time)
    soundDict = {}

    def __init__(self):
        self.loadSounds()
        SoundPlayer.player = self
        self.mute = False

    @staticmethod
    def wipe():
        pass

    @staticmethod
    def requestSound(sound):
        SoundPlayer.player.playSound(sound)

    def loadSoundFile(self, fileName):
        filePath = os.path.join("sound", fileName)
        sound = pygame.mixer.Sound(filePath)

        return sound

    def getSound(self, sound):
        """ lets instance get sound from class dictionary """
        if sound not in SoundPlayer.soundDict:
            SoundPlayer.soundDict[sound] = self.loadSoundFile(sound)

        return SoundPlayer.soundDict[sound]

    def loadSounds(self):
        """ load sounds files  / adjust volume """
        VOLUME = .35 # b/w 0 and 1 (default .35)
        self.VOLUME = VOLUME

        try:
            self.sndRotate = self.getSound("newRotate.ogg")
            self.sndRotate.set_volume(VOLUME)
            self.sndLost  = self.getSound("lost2.ogg")
            self.sndLost.set_volume(VOLUME - .1)
            self.sndGoal = self.getSound("goal2.ogg")
            self.sndGoal.set_volume(VOLUME)
            self.sndPickUp = self.getSound("pickUp.ogg")
            self.sndPickUp.set_volume(VOLUME)
            self.sndNoPlace = self.getSound("nope.ogg")
            self.sndNoPlace.set_volume(VOLUME)
            self.sndPlace = self.getSound("place.ogg")
            self.sndPlace.set_volume(VOLUME)
            self.sndAppear = self.getSound("cannon4.ogg")
            self.sndAppear.set_volume(VOLUME - .12)
            self.sndSqueal = self.getSound("squeal.ogg")
            self.sndSqueal.set_volume(VOLUME - .2)
            self.sndChain = self.getSound("chain6.ogg")
            self.sndChain.set_volume(VOLUME + .2)
            self.sndOpenWarp = self.getSound("openWarp.ogg")
            self.sndOpenWarp.set_volume(VOLUME - .1)
            self.sndDinoWarp = self.getSound("dinoWarp.ogg")
            self.sndDinoWarp.set_volume(VOLUME)
            self.sndCycle = self.getSound("cycle.ogg")
            self.sndCycle.set_volume(VOLUME)
            self.sndSwitch = self.getSound("switch.ogg")
            self.sndSwitch.set_volume(VOLUME)
            self.sndWin = self.getSound("win.ogg")
            self.sndWin.set_volume(VOLUME - .2)
            self.sndLose = self.getSound("lose.ogg")
            self.sndLose.set_volume(VOLUME - .15)
            self.sndStart = self.getSound("launch.ogg")
            self.sndStart.set_volume(VOLUME)
            self.sndToggle = self.getSound("toggle.ogg")
            self.sndToggle.set_volume(VOLUME)
            self.sndButtonOver = self.getSound("buttonOver.ogg")
            self.sndButtonOver.set_volume(VOLUME)
            self.sndButtonClick = self.getSound("buttonClick.ogg")
            self.sndButtonClick.set_volume(VOLUME - .1)
            self.sndMessage = self.getSound("message.ogg")
            self.sndMessage.set_volume(VOLUME + .2)
            self.sndPause = self.getSound("pause.ogg")
            self.sndPause.set_volume(VOLUME)
            self.sndQRestart = self.getSound("qRestart.ogg")
            self.sndQRestart.set_volume(VOLUME)
            self.sndToggleRecover = self.getSound("toggleRecover.ogg")
            self.sndToggleRecover.set_volume(VOLUME)
            self.sndNoRecover = self.getSound("nope.ogg")
            self.sndNoRecover.set_volume(VOLUME)
            #self.sndResume = self.getSound("resumeGame.ogg")
            #self.sndResume.set_volume(VOLUME)

            self.sndBounce1 = self.getSound("bounce1.ogg")
            self.sndBounce1.set_volume(VOLUME)
            self.sndRadio = self.getSound("radio.ogg")
            self.sndRadio.set_volume(VOLUME + .6)
            self.sndWoosh_a = self.getSound("woosh4.ogg")
            self.sndWoosh_a.set_volume(VOLUME + .2)
            self.sndWoosh_b = self.getSound("woosh5.ogg")
            self.sndWoosh_b.set_volume(VOLUME + .2)
            self.sndSnaxScreen = self.getSound("powerStation.ogg")
            self.sndSnaxScreen.set_volume(VOLUME)
            self.sndSnack = self.getSound("snack.ogg")
            self.sndSnack.set_volume(VOLUME + .2)
            self.sndWinGame = self.getSound("winGame.ogg")
            self.sndWinGame.set_volume(VOLUME + .2)

            self.sndBounceList = [] # bounce sound is pulled randomly from list

            for i in range(4):  # edit amt here - must match files
                file = "b1_" + str(i) + ".ogg"
                sound = self.getSound(file)
                sound.set_volume(VOLUME)
                self.sndBounceList.append(sound)

        except:
            print("ERROR: could not load sounds")

    def playSound(self, sound):
        """ play sounds based on request type """

        if self.mute:
            pass

        elif sound == "bounce":
            self.sndBounce1.play()
##            bounceIndex = random.randrange(len(self.sndBounceList))
##            self.sndBounceList[bounceIndex].play()
        elif sound == "rotate":
            self.sndRotate.play()
        elif sound == "goal":
            self.sndGoal.play()
        elif sound == "lost":
            self.sndLost.play()
        elif sound == "pickUp":
            self.sndPickUp.play()
        elif sound == "noPlace":
            self.sndNoPlace.play()
        elif sound == "place":
            self.sndPlace.play()
        elif sound == "appear":
            self.sndAppear.play()
        elif sound == "squeal":
            self.sndSqueal.play()
        elif sound == "chain":
            self.sndChain.play()
        elif sound == "openWarp":
            self.sndOpenWarp.play()
        elif sound == "dinoWarp":
            self.sndDinoWarp.play()
        elif sound == "cycle":
            self.sndCycle.play()
        elif sound == "switch":
            self.sndSwitch.play()
        elif sound == "win":
            self.sndWin.play()
        elif sound == "lose":
            self.sndLose.play()
        elif sound == "start":
            self.sndStart.play()
        elif sound == "toggle":
            self.sndToggle.play()
        elif sound == "buttonOver":
            self.sndButtonOver.play()
        elif sound == "buttonClick":
            self.sndButtonClick.play()
        elif sound == "message":
            self.sndMessage.play()
        elif sound == "pause":
            self.sndPause.play()
        elif sound == "noRecover":
            self.sndNoRecover.play()
        elif sound == "qRestart":
            self.sndQRestart.play()
        elif sound == "toggleRecover":
            self.sndToggleRecover.play()
        elif sound == "radio":
            self.sndRadio.play()
        elif sound == "woosh_a":
            self.sndWoosh_a.play()
        elif sound == "woosh_b":
            self.sndWoosh_b.play()
        elif sound == "snaxScreen":
            self.sndSnaxScreen.play()
        elif sound == "snack":
            self.sndSnack.play()
        elif sound == "winGame":
            self.sndWinGame.play()


        #elif sound == "resume":
        #
        #    self.sndResume.play()

class GameSoundManager(pygame.sprite.Sprite):
    """ registers sound requests, deletes duplicates per update: game state only """
    me = None

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.soundCue = []
        GameSoundManager.me = self
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()
        myGroup = pygame.sprite.RenderUpdates(self)
        game.addGroup(myGroup)

    def update(self):
        for sound in self.soundCue:
            SoundPlayer.requestSound(sound)

        self.soundCue = []

    @staticmethod
    def wipe():
        GameSoundManager.me = None

    @staticmethod
    def registerSound(sound):
        if sound not in GameSoundManager.me.soundCue:
            GameSoundManager.me.soundCue.append(sound)

    def draw(self, foo):
        pass

    def clear(self, foo, bar):
        pass

def wipe():
    SoundPlayer.wipe()
    GameSoundManager.wipe()

if __name__ == "__main__":
    print("module for import only")