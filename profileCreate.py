"""
        profileCreate.py
        - player selects or creates new profile
"""

import pygame
import textInput56
import dinosInSpace
import spriteBasic
import infoGraphic56
import tween
import dataStorage56
import gfx56
import screenWipe
import soundFx56

OLIVE   = (110,139,61)
KHAKI   = (189,183,107)
BROWN   = (92,64,51)
ORCHID  = (139,71,137)
DORCHID = (109,31,107)
MAROON  = (176,48,96)
PURPLE  = (93,71,139)
GOLD    = (205,155,29)

DGREEN = (0,180,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (150,150,150)
RED = (255,0,0)
BLUE = (0,0,255)

PROFILE_DINO_CENTER = (200, 450)
PLANET_TOPLEFT = (400,100)
NEW_PROFILE_BUTTON_CENTER = (200,150)
INPUTBOX_CENTER = (200,300)
INPUT_TEXT_OFFSET_X = 20
INPUT_TEXT_OFFSET_Y = -8
INPUT_END_BUFFER = 60
BTTN_FONTSIZE = 20
BTTN_H = 40
NON_LETTER  = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_")

HLP_NAME    = "<< Enter your name"
HLP_NONLET  = "<< Must start with a letter"
HLP_TAKEN   = "<< Profile already exists"

class ImgLib(object):
    """ image library to load and access local images """
    imgDict = None

    def __init__(self):
        if not ImgLib.imgDict:

            ImgLib.imgDict = {
                "CURSORSTD"     :   dinosInSpace.loadImage("controlCursor.png", "2X", (21,21)),
                "BTTN1"         :   spriteBasic.BasicRect((pygame.display.get_surface().get_width()/2,300), RED, None, 2).image,
                "BTTN2"         :   spriteBasic.BasicRect((pygame.display.get_surface().get_width()/2,300), RED).image,
                "FOLDER0" : dinosInSpace.loadImage("folderButton0.png", "2X", (0,0)),
                "FOLDER1" : dinosInSpace.loadImage("folderButton1.png", "2X", (0,0)),
                "EXIT1"         :   spriteBasic.BasicRect((pygame.display.get_surface().get_width()/2,40), GREY).image,
                "EXIT2"         :   spriteBasic.BasicRect((pygame.display.get_surface().get_width()/2,40), DGREEN).image,
                "PLANET" : dinosInSpace.loadImage("nPlanet2.png", "2X", (0,0)),
                "PDINO0" : dinosInSpace.loadImage("profileDino0.png", "4X", (0,0)),
                "PDINO1" : dinosInSpace.loadImage("profileDino1.png", "4X", (0,0))
            }

    @staticmethod
    def getImage(name):
        if name in ImgLib.imgDict:
            return ImgLib.imgDict[name].copy()
        else:
            print "image, " + name + " not found"


class NewProfileScreen(object):
    """ running state """
    me = None

    def __init__(self):
        NewProfileScreen.me = self

        self.keepGoing      = True

        self.bkgGroup       = pygame.sprite.OrderedUpdates()    # bottom level gfx
        self.hTextGroup     = pygame.sprite.RenderUpdates()             # tween helper text (input error messages)
        self.rhBkgGroup     = pygame.sprite.RenderUpdates()             # right hand side background (above all previous groups)
        self.buttonGroup    = pygame.sprite.RenderUpdates()             # buttons that return a dest
        self.inputGroup     = pygame.sprite.OrderedUpdates()    # input box and cursor
        self.cursorGroup    = pygame.sprite.RenderUpdates()       # mouse cursor

        self.screen         = pygame.display.get_surface()
        self.background     = pygame.Surface(self.screen.get_size())

        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))

    @staticmethod
    def wipe():
        NewProfileScreen.me = None

    def runMe(self, _fps, imageFrom):
        clock = pygame.time.Clock()
        self.keepGoing = True
        dest = None

        while self.keepGoing:

            clock.tick(_fps)
            dest = self.getInput()

#            self.bkgGroup.clear(screen, background)
            self.rhBkgGroup.clear(self.screen, self.background)
            self.hTextGroup.clear(self.screen, self.background)
            self.buttonGroup.clear(self.screen, self.background)
            self.inputGroup.clear(self.screen, self.background)
            self.cursorGroup.clear(self.screen, self.background)

#            self.bkgGroup.update()
            self.rhBkgGroup.update()
            self.hTextGroup.update()
            self.buttonGroup.update()
            self.inputGroup.update()
            self.cursorGroup.update()

#            self.bkgGroup.draw(screen)
            self.rhBkgGroup.draw(self.screen)
            self.hTextGroup.draw(self.screen)
            self.buttonGroup.draw(self.screen)
            self.inputGroup.draw(self.screen)
            self.cursorGroup.draw(self.screen)

            gfx56.drawBorder(self)

            # ************************************************* #
            # *** screen transition / destroy covered image *** #
            # ************************************************* #
            screenWipe.wipe(_fps, imageFrom, self.screen.copy(), "left")
            imageFrom = None
            # ************************************************* #
            # ************************************************* #
            # ************************************************* #

            pygame.display.update()

            if dest:
                soundFx56.SoundPlayer.requestSound("woosh_b")
                self.keepGoing = False

        # ************************************ #
        # *** clear cursor / take snapshot *** #
        # ************************************ #
        self.cursorGroup.clear(self.screen, self.background)

        self.rhBkgGroup.draw(self.screen)
        self.hTextGroup.draw(self.screen)
        self.buttonGroup.draw(self.screen)
        self.inputGroup.draw(self.screen)

        gfx56.drawBorder(self)
        snapshot = self.screen.copy()
        # ************************************ #
        # ************************************ #
        # ************************************ #

        return dest, snapshot

    def getInput(self):
        dest        = None
        chr         = None
        inputText   = None
        error       = None

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                dest = self.checkButtonPressed()
                if dest == "NP":
                    inputText, error = ProfileInputBox.me.getMessageIfValid()
                    if error:
                        HelperText.pushOver(error)
                        self.addSpriteToGroup(HelperText.curText, "HELPER")
                        dest = None
                    else:
                        dest = inputText

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    dest = "_EXIT"

                elif event.key == pygame.K_RETURN:
                    inputText, error = ProfileInputBox.me.getMessageIfValid()
                    if error:
                        HelperText.pushOver(error)
                        self.addSpriteToGroup(HelperText.curText, "HELPER")
                        dest = None
                    else:
                        dest = inputText

                # ---------- text box input key bindings

                if event.key == pygame.K_BACKSPACE:
                    chr = "BACK"
                elif event.key == pygame.K_q:
                    chr = "Q"
                elif event.key == pygame.K_w:
                    chr = "W"
                elif event.key == pygame.K_e:
                    chr = "E"
                elif event.key == pygame.K_r:
                    chr = "R"
                elif event.key == pygame.K_t:
                    chr = "T"
                elif event.key == pygame.K_y:
                    chr = "Y"
                elif event.key == pygame.K_u:
                    chr = "U"
                elif event.key == pygame.K_i:
                    chr = "I"
                elif event.key == pygame.K_o:
                    chr = "O"
                elif event.key == pygame.K_p:
                    chr = "P"
                elif event.key == pygame.K_a:
                    chr = "A"
                elif event.key == pygame.K_s:
                    chr = "S"
                elif event.key == pygame.K_d:
                    chr = "D"
                elif event.key == pygame.K_f:
                    chr = "F"
                elif event.key == pygame.K_g:
                    chr = "G"
                elif event.key == pygame.K_h:
                    chr = "H"
                elif event.key == pygame.K_j:
                    chr = "J"
                elif event.key == pygame.K_k:
                    chr = "K"
                elif event.key == pygame.K_l:
                    chr = "L"
                elif event.key == pygame.K_z:
                    chr = "Z"
                elif event.key == pygame.K_x:
                    chr = "X"
                elif event.key == pygame.K_c:
                    chr = "C"
                elif event.key == pygame.K_v:
                    chr = "V"
                elif event.key == pygame.K_b:
                    chr = "B"
                elif event.key == pygame.K_n:
                    chr = "N"
                elif event.key == pygame.K_m:
                    chr = "M"
                elif event.key == pygame.K_1:
                    chr = "1"
                elif event.key == pygame.K_2:
                    chr = "2"
                elif event.key == pygame.K_3:
                    chr = "3"
                elif event.key == pygame.K_4:
                    chr = "4"
                elif event.key == pygame.K_5:
                    chr = "5"
                elif event.key == pygame.K_6:
                    chr = "6"
                elif event.key == pygame.K_7:
                    chr = "7"
                elif event.key == pygame.K_8:
                    chr = "8"
                elif event.key == pygame.K_9:
                    chr = "9"
                elif event.key == pygame.K_0:
                    chr = "0"
                elif event.key == pygame.K_MINUS or event.key == pygame.K_SPACE:
                    chr = "_"

        if chr:
            ProfileInputBox.me.render(chr)

        return dest

    def addSpriteToGroup(self, sprite, group):
        if group == "BKG":
            self.bkgGroup.add(sprite)
        elif group == "RHBKG":
            self.rhBkgGroup.add(sprite)
        elif group == "HELPER":
            self.hTextGroup.add(sprite)
        elif group == "BUTTON":
            self.buttonGroup.add(sprite)
        elif group == "INPUT":
            self.inputGroup.add(sprite)
        elif group == "CURSOR":
            self.cursorGroup.add(sprite)

    def addSpriteListToGroup(self, spriteList, group):
        for s in spriteList:
            self.addSpriteToGroup(s, group)

    def checkButtonPressed(self):
        dest = None
        for b in self.buttonGroup:
            dest = b.requestDest()
            if dest:
                break

        return dest

class ProfileInputBox(textInput56.TextInputBox):
    me = None

    def __init__(self, boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, endBuffer, off_x=None, off_y=None):
        textInput56.TextInputBox.__init__(self, boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, endBuffer, off_x, off_y)
        ProfileInputBox.me = self

    @staticmethod
    def wipe():
        ProfileInputBox.me = None

#    def render(self, chr):
#        textInput56.TextInputBox.render(self, chr)
#        FB_SaveMap.setFileSafety()
#

    def setCenter(self, center):
        self.rect.center = center

    @staticmethod
    def getMessageIfValid():
        """ returns message if valid; returns None if not valid """
        msg = None
        error = None
        myMsg = ProfileInputBox.me.message

        if len(myMsg) < 1:
            error = HLP_NAME
        elif myMsg[0] in NON_LETTER:
            error = HLP_NONLET
        elif dataStorage56.checkForProfile(myMsg):
            error = HLP_TAKEN
        else:
            msg = ProfileInputBox.me.message

        return msg, error


class Button(pygame.sprite.Sprite):

    def __init__(self, topLeft, imageOff, imageOver, text, textSize, textColor, dest, center=None):
        pygame.sprite.Sprite.__init__(self)

        self.imageOff       = self.makeButton(imageOff, text, textSize, textColor)
        self.imageOver      = self.makeButton(imageOver, text, textSize, textColor)
        self.image          = self.imageOff
        self.rect           = self.image.get_rect()
        if topLeft:
            self.rect.topleft = topLeft
        if center:
            self.rect.center = center
        self.dest           = dest
        self.firstCycle     = True
        self.mouseOver = False

    def update(self):
        if not self.firstCycle:
            self.checkCursorOver()
        else:
            self.firstCycle = False

    def makeButton(self, image, text, textSize, textColor):

        textSurf = infoGraphic56.TextObject(text, textSize, textColor).image
        xBlit = (image.get_width() - textSurf.get_width())/2
        yBlit = (image.get_height() - textSurf.get_height())/2
        image.blit(textSurf, (xBlit, yBlit))

        return image

    def checkCursorOver(self):
        """ if cursor over button set respective image and mouseOver """
        if pygame.sprite.collide_rect(self, MouseCursor.me):
            self.image = self.imageOver
            self.mouseOver = True
        else:
            self.image = self.imageOff
            self.mouseOver = False

    def requestDest(self):
        """ returns dest if mouseOver """
        dest = None
        if self.mouseOver:
            dest = self.dest

        return dest


class MouseCursor(pygame.sprite.Sprite):
    me = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image  = ImgLib.getImage("CURSORSTD")
        self.rect   = pygame.rect.Rect((0,0,1,1))
        self.firstCycle = True

        MouseCursor.me = self

    def update(self):
        if self.firstCycle:
            self.rect.center = (2000,2000)
            self.firstCycle = False
        else:
            self.rect.center = pygame.mouse.get_pos()

    @staticmethod
    def wipe():
        MouseCursor.me = None

class HelperText(tween.TweenMenu):
    """ text specific tween sprite -- only one instance held as class var at a time """
    curText     = None
    textSize    = 20
    textColor   = (255,255,255)

    def __init__(self, message):
        tween.TweenMenu.__init__(self)
        HelperText.curText  = self

        self.image          = infoGraphic56.TextObject(message, HelperText.textSize, HelperText.textColor).image
        self.rect           = self.image.get_rect()
        self.leavingScreen  = False
        self.firstCycle     = True

    def update(self):
        """ modify to kill text after leaving screen """
        if not self.firstCycle:
            if self.leavingScreen:
                if self.rect.right < 1:
                    self.kill()

            tween.TweenMenu.update(self)
        else:
            self.firstCycle = False

    @staticmethod
    def setTween(isEntering):
        speed       = 50
        mode        = "EXP"
        dcl         = 0.89
        lim         = 6
        screen      = pygame.display.get_surface()
        x           = 3*screen.get_width()/4


        if isEntering:
            startPoint  = (x,-HelperText.curText.image.get_height()/2)
            endPoint    = (x, 300)
        else:
            startPoint  = (x, screen.get_height()/2)
            endPoint    = (x, screen.get_height() + HelperText.curText.image.get_height()/2)
            HelperText.curText.leavingScreen = True

        tween.TweenMenu.setTween(HelperText.curText, startPoint, endPoint, speed, mode, dcl, lim)

    @staticmethod
    def startTween():
        tween.TweenSprite.startTween(HelperText.curText)

    @staticmethod
    def pushOver(msg):
        HelperText.curText.clearVals()
        HelperText.setTween(False)
        HelperText.startTween()

        HelperText.curText = HelperText(msg)
        HelperText.setTween(True)
        HelperText.startTween()

    @staticmethod
    def wipe():
        HelperText.curText = None

class ImageLinkedToButton(pygame.sprite.Sprite):

    def __init__(self, masterButton, imageOff, imageOver, center):
        pygame.sprite.Sprite.__init__(self)

        self.masterButton = masterButton
        self.imageOff = imageOff
        self.imageOver = imageOver

        self.image = self.imageOff
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.masterButton.mouseOver:
            self.image = self.imageOver
        else:
            self.image = self.imageOff


def launchProfileCreate(_fps, snapshot):

    screen      = pygame.display.get_surface()
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    ImgLib()
    img = ImgLib.getImage

    newProfileScreen = NewProfileScreen()

    # rhs background

#    rhSize      = (screenWidth/2, screenHeight)
    rhColor     = (0,0,0)
#    rhTopLeft   = (screenWidth/2, 0)
    rhRadius    = 700
    rhCenter    = (screenWidth + 200, screenHeight/2)
    planet      = spriteBasic.BasicImg(img("PLANET"), PLANET_TOPLEFT)

#    rhBkg = spriteBasic.BasicRect(rhSize, rhColor, rhTopLeft)
#    rhBkg = spriteBasic.BasicCircle(rhRadius, rhColor, rhCenter)
    newProfileScreen.addSpriteToGroup(planet, "RHBKG")

    # lhs box
    lhsBox = spriteBasic.BasicRect((400,600), WHITE, (0,0), 2)
    newProfileScreen.addSpriteToGroup(lhsBox, "RHBKG")

    # input box
    boxBuffer   = 150
    boxSize     = (screenWidth/2 - boxBuffer, 40)
    boxColor    = DGREEN
    textSize    = BTTN_FONTSIZE
    textColor   = BLACK
    cursorWidth = 7
    cursorColor = BLACK

    inputBox = ProfileInputBox(boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, INPUT_END_BUFFER, INPUT_TEXT_OFFSET_X, INPUT_TEXT_OFFSET_Y)
    inputBox.setCenter(INPUTBOX_CENTER)

    newProfileScreen.addSpriteListToGroup([inputBox, inputBox.cursor], "INPUT")

    # buttons

    bHeight     = img("BTTN1").get_height()

    createBttn = Button(None, img("FOLDER0"), img("FOLDER1"), "new profile", BTTN_FONTSIZE, BLACK, "NP", NEW_PROFILE_BUTTON_CENTER)
    exitBttn = Button((0,screenHeight - 40), img("EXIT1"), img("EXIT2"), "BACK", BTTN_FONTSIZE, BLACK, "_EXIT")
    profileDino = ImageLinkedToButton(createBttn, img("PDINO0"), img("PDINO1"), PROFILE_DINO_CENTER)

    newProfileScreen.addSpriteListToGroup([createBttn, exitBttn],"BUTTON")
    newProfileScreen.addSpriteToGroup(profileDino, "RHBKG")

    # helper text

    htest = HelperText(HLP_NAME)
    newProfileScreen.addSpriteToGroup(htest, "HELPER")

    HelperText.setTween(True)
    HelperText.startTween()

    # cursor

    mouseCursor = MouseCursor()
    newProfileScreen.addSpriteToGroup(mouseCursor, "CURSOR")

    dest, snapshot = newProfileScreen.runMe(_fps, snapshot)
    wipe()

    return dest, snapshot

def wipe():
    NewProfileScreen.wipe()
    ProfileInputBox.wipe()
    MouseCursor.wipe()
    HelperText.wipe()

















