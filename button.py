""" button.py

    button utilities
    John Saba
"""

import pygame
import dinosInSpace
import gfx56

class Button(pygame.sprite.Sprite):
    """
        basic button with mouse over recognition and image change
    """

    def __init__(self, dest, framesOrSize, center=None, fillColor=None, text=None, fontSize=None, fontColor=None):
        """
            * using images *
            -framesOrSize may be a pair of surfaces or dimensions of a rectangle
                > (img0, img1) or (width, height)

            * using generated surfaces *
            -fillColor, text, fontSize, fontColor may be either one or two values
            -first value is for the the off state, second is for mouseover state
        """
        pygame.sprite.Sprite.__init__(self)

        self.dest = dest
        self.frames = makeButtonFrames(framesOrSize, fillColor, text, fontSize, fontColor)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.mouseOver = False

        if center:
            self.rect.center = center

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.frames[1]
            self.mouseOver = True
        else:
            self.image = self.frames[0]
            self.mouseOver = False

    def checkPressed(self):
        """ called upon mouse click"""
        if self.mouseOver:
            return self.dest


class ImageToggler(Button):
    """
        image only button that toggles between on and off states
    """

    def __init__(self, dest, frameSet, center=None):
        """
            -frameSet must be 2 pair:
                > ((img0_a, img1_a), (img0_b, img1_b))
        """

        Button.__init__(self, dest, frameSet[0], center)
        self.frames.extend(makeButtonFrames(frameSet[1]))

        self.off = 0
        self.over = 1

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.frames[self.over]
            self.mouseOver = True
        else:
            self.image = self.frames[self.off]
            self.mouseOver = False

    def checkPressed(self):
        """ called upon mouse click"""
        if self.mouseOver:
            self.toggle()

    def toggle(self):
        """ turn on or off """
        if self.off == 0:
            self.off = 2
            self.over = 3
        else:
            self.off = 0
            self.over = 1


def makeButtonFrames(framesOrSize, fillColor=None, text=None, fontSize=None, fontColor=None):
    """ -creates and returns 2 buttons frames with centered text
        -handles loaded image or primative generation
        -accepts 1 or 2 values for fillColor, text, fontSize and fontColor
    """

    # create images for off and over states
    if type(framesOrSize[0]) == int:
        frame0 = pygame.Surface(framesOrSize)
        frame1 = frame0.copy()
    else:
        frame0, frame1 = framesOrSize


    # colors frames if needed
    if fillColor:
        if len(fillColor) == 3:
            frame0.fill(fillColor)
            frame1.fill(fillColor)
        else:
            frame0.fill(fillColor[0])
            frame1.fill(fillColor[1])


    # set font size(s)
    if fontSize:
        if type(fontSize) == int:
            font0 = dinosInSpace.FontBank.getFont(fontSize)
            font1 = font0
        else:
            font0 = dinosInSpace.FontBank.getFont(fontSize[0])
            font1 = dinosInSpace.FontBank.getFont(fontSize[1])


    # set font color(s)
    if fontColor:
        if len(fontColor) == 3:
            col0 = fontColor
            col1 = col0
        else:
            col0 = fontColor[0]
            col1 = fontColor[1]


    # make text(s)
    if text:
        if type(text) == str:
            text0 = font0.render(text, True, fontColor)
            text1 = text0
        else:
            text0 = font0.render(text[0], True, fontColor)
            text1 = font1.render(text[1], True, fontColor)

        frame0 = gfx56.centerBlit(frame0, text0)
        frame1 = gfx56.centerBlit(frame1, text1)


    return [frame0, frame1]

