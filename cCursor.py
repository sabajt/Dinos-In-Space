"""
    cCursor.py
    cursor utility
    John Saba 2012
"""

import pygame
import dinosInSpace

OFFSCREEN = (1000,1000)

class Cursor(pygame.sprite.Sprite):
    """ importable cursor object """
    me = None
    DEFAULT_IMG = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if not Cursor.DEFAULT_IMG:
            Cursor.DEFAULT_IMG = dinosInSpace.loadImage("controlCursor.png", "2X", (21,21))

        self.image = Cursor.DEFAULT_IMG.copy()
        self.rect = pygame.Rect((0,0,1,1))
        self.firstCycle = True

        Cursor.me = self

    def update(self):
        if not self.firstCycle:
            self.rect.topleft = pygame.mouse.get_pos()
        else:
            self.rect.topleft = OFFSCREEN
            self.firstCycle = False

    @staticmethod
    def wipe():
        Cursor.me = None