""" textInput56.py """

import pygame
import dinosInSpace

class TextInputBox(pygame.sprite.Sprite):
    """ textbox that takes user input - makes slave cursor object (must pair w/ class) """

    def __init__(self, boxSize, boxColor, textSize, textColor, cursorWidth, cursorColor, endBuffer=10, text_offset_x=0, text_offset_y=0, editorFont=False):
        pygame.sprite.Sprite.__init__(self)

        self.boxWidth, self.boxHeight = boxSize
        self.box = pygame.Surface(boxSize)
        self.box.fill(boxColor)
        self.font = dinosInSpace.FontBank.getFont(textSize, editorFont)
        self.textBlitX = 2 + text_offset_x
        self.textBlitY = (self.boxHeight - textSize)/2 + text_offset_y
        self.textBlitPos = (self.textBlitX, self.textBlitY)
        self.textColor = textColor
        self.image = self.box
        self.rect = self.image.get_rect()
        self.message = "" # displayed text
        self.cursorWidth = cursorWidth
        self.cursorColor = cursorColor
        self.cursor = InputCursor(self)
        self.textWidth = 0 # track to stop text from going out of bounds
        self.ENDBUFFER = endBuffer

    def render(self, chr):
        if chr:
            if chr == "BACK":
                self.message = self.message[:-1]
            else:
                if (self.textWidth + self.ENDBUFFER) < self.image.get_width():
                    self.message += chr

            box = self.box.copy()
            text = self.font.render(self.message, True, self.textColor)
            self.textWidth = text.get_width()
            box.blit(text, self.textBlitPos)
            self.image = box

    def getCursorPos(self):
        """ return cursor pos relative to textbox """
        text = self.font.render(self.message, True, self.textColor)
        width = text.get_width()
        x = width + self.textBlitX
        y = self.textBlitY
        return x, y

class InputCursor(pygame.sprite.Sprite):

    def __init__(self, masterText):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((masterText.cursorWidth, masterText.boxHeight))
        self.image.fill(masterText.cursorColor)
        self.rect = self.image.get_rect()
        self.masterText = masterText

        self.BLINKSTEP = 10
        self.blinkTick = self.BLINKSTEP
        self.visible = True

    def update(self):
        """ position """
        rel_x, rel_y = self.masterText.getCursorPos()
        x = self.masterText.rect.left + rel_x
        y = self.masterText.rect.top
        self.rect.left = x
        self.rect.top = y
        self.blink()

    def blink(self):
        self.blinkTick -= 1

        if self.blinkTick < 1:

            if self.visible:
                self.image.set_alpha(0, pygame.RLEACCEL)
                self.visible = False
            else:
                self.image.set_alpha(255)
                self.visible = True

            self.blinkTick = self.BLINKSTEP



# ----------------------------------------- spinner / spinner button

class Spinner(pygame.sprite.Sprite):
    """ displays a number controlled by spinner button which points to this """

    def __init__(self, topLeft, boxSize, boxColor, fontSize, numColor, minValue, maxValue, defaultValue, editorFont=False):
        pygame.sprite.Sprite.__init__(self)

        self.box = pygame.Surface(boxSize)
        self.box.fill(boxColor)
        self.font = dinosInSpace.FontBank.getFont(fontSize, editorFont)
        self.fontSize = fontSize
        self.numColor = numColor
        self.minValue = minValue
        self.maxValue = maxValue
        self.defaultValue = defaultValue
        self.currentValue = self.defaultValue
        self.image = self.box.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft
        self.numBlit_y = (boxSize[1] - fontSize)/2 # used for positioning when rendering
        self.renderValue()
        self.SPIN_STEP = 1

    def spin(self, operation):
        if operation == "ADD" and self.currentValue < self.maxValue:
            self.currentValue += self.SPIN_STEP
        elif operation == "SUBTRACT" and self.currentValue > self.minValue:
            self.currentValue -= self.SPIN_STEP

        self.renderValue()

    def renderValue(self):
        number = self.font.render(str(self.currentValue), True, self.numColor)
        numWidth = number.get_width()
        numBlit_x = (self.box.get_width() - numWidth)/2
        self.image = self.box.copy()
        self.image.blit(number, (numBlit_x, self.numBlit_y))

    def getCurrentValue(self):
        return self.currentValue

class SpinnerButton(pygame.sprite.Sprite):
    """ operation 'ADD' or 'SUBTRACT' on slave spinner : can be subclassed as function button """

    def __init__(self, surf, topLeft, slave, operation, specialHL=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = surf
        self.imgOff = surf
        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft
        self.slave = slave # points to a spinner
        self.operation = operation # add or subtract
        self.mouseOver = False
        self.specialHL = specialHL

        self.makeOverImg()

    def update(self):
        if pygame.sprite.collide_rect(self, self.cursor):
            self.image = self.imgOn
            self.mouseOver = True
        else:

            self.image = self.imgOff
            self.mouseOver = False

    def setLocalCursor(self, cursor):
        self.cursor = cursor

    def makeOverImg(self):
        bkgColor = (10,110,200)
        size = self.image.get_size()
        newSurf = pygame.Surface(size)
        newSurf.fill(bkgColor)
        origSurf = self.image.copy()
        newSurf.blit(origSurf, (0,0), None, pygame.BLEND_ADD)
        newSurf.set_colorkey((255,255,255), pygame.RLEACCEL)
        if self.specialHL:
            newSurf = newSurf.copy()
            newSurf.set_colorkey(newSurf.get_at((0,0)), pygame.RLEACCEL)
        self.imgOn = newSurf

    def pressMe(self):
        """ send operation to slave """
        self.slave.spin(self.operation)




