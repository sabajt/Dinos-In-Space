""" spriteBasic - simple sprite objects to extend """

import pygame
import gfx56

class BasicRect(pygame.sprite.Sprite):
    """
        primative rectangle sprite
        -optional parameter width makes rect an outline
    """

    def __init__(self, size, color, topLeft=(0,0), rimSize=None, alpha=None, opaqueCenter=False):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.alpha = None

        if alpha:
            self.image.set_alpha(alpha, pygame.RLEACCEL)
            self.alpha = alpha

        if topLeft:
            self.rect.topleft = topLeft

        if rimSize:
            self.makeRim(color, rimSize, opaqueCenter)

    def makeRim(self, color, width, opaque):
        if color != (0,0,0):
            keyCol = (0,0,0)
        else:
            keyCol = (255,255,255)
        size = (self.image.get_width() - 2 * width, self.image.get_height() - 2 * width)
        keySurf = pygame.Surface(size)
        keySurf.fill(keyCol)
        self.image.blit(keySurf, (width, width))
        if not opaque:
            self.image.set_colorkey(keyCol, pygame.RLEACCEL)

    def resize(self, size):
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        if self.alpha:
            self.image.set_alpha(self.alpha, pygame.RLEACCEL)


class BasicCircle(pygame.sprite.Sprite):
    """
        primative circle sprite
        -optional parameter width makes circle an outline
        -self.rect surrounds the circle
    """

    def __init__(self, radius, color, center, width=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((2*radius, 2*radius))

        if color != (0,0,0):
            keyCol = (0,0,0)
        else:
            keyCol = (255,255,255)

        self.image.fill(keyCol)
        pygame.draw.circle(self.image, color, (radius, radius), radius, width)
        self.image.set_colorkey(keyCol, pygame.RLEACCEL)

        self.rect = self.image.get_rect()
        self.rect.center = center

class BasicImg(pygame.sprite.Sprite):
    """
        makes a sprite out of an image
    """

    def __init__(self, img, topLeft=None):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        if topLeft:
            self.rect.topleft = topLeft

    def setImage(self, img):
        self.image = img
        self.rect = self.image.get_rect()

    def setAlpha(self, val):
        self.image.set_alpha(val, pygame.RLEACCEL)

    def superImpose(self, img, topLeft=(0,0), toCenter=False):
        if not toCenter:
            self.image.blit(img, topLeft)
        else:
            self.image = gfx56.centerBlit(self.image.copy(), img)



