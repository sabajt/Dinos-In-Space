""" tracer56.py """

import pygame
import math
import interface56


class SwitchTracer(pygame.sprite.Sprite):
    """ draws line b/w switch and their dependants """
    
    switchTracerGroup = pygame.sprite.RenderUpdates()
    color = (0,0,255)
    size = 1
    
    def __init__(self, traceFrom, linkedObj):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.traceFrom = traceFrom
        self.linkedObj = linkedObj
        self.active = False
        self.clearImage()
        SwitchTracer.switchTracerGroup.add(self)
        
    def update(self):
        
        if self.active:
            
            if interface56.Cursor.testSwitchDown:
                
                self.tracePath()
            
            else:
        
                self.traceFrom = None
                self.linkedObj = None
                self.clearImage()
                 
    @staticmethod
    def wipe():
     
        SwitchTracer.switchTracerGroup = pygame.sprite.RenderUpdates()   
        
    def activate(self):
        
        self.active = True
        
    def deactivate(self):
        
        self.active = False
        self.clearImage()
            
    def getLinkedCoord(self):
        """ return linkedX, linkedY """
        
        x, y = self.linkedObj.rect.centerx, self.linkedObj.rect.centery
        
        return x, y
    
    def tracePath(self): 
        """ draw a line from switch to linked objects """
        
        abs = math.fabs
        
        linkedX, linkedY = self.getLinkedCoord()
        
        traceX, traceY = self.traceFrom.rect.center
        
        w = abs(linkedX- traceX)
        h = abs(linkedY - traceY)
        
        if w < 100:
            
            w = 100
            
        if h < 100:
            
            h = 100
        
        self.image = pygame.Surface((w, h))
        self.image.fill((255,255,255))
        transparent = self.image.get_at((0,0))
        self.image.set_colorkey(transparent, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        imgW = self.image.get_width()
        imgH = self.image.get_height()
        c = SwitchTracer.color
        s = SwitchTracer.size
        
        if linkedX > traceX:
            
            if linkedY < traceY:
                
                self.rect.bottomleft = (traceX, traceY)
                pygame.draw.line(self.image, c, (0, imgH), (imgW, 0), s)
                
            elif linkedY > traceY:
                
                self.rect.topleft = (traceX, traceY)
                pygame.draw.line(self.image, c, (0,0), (imgW, imgH), s)
            
            elif linkedY == traceY:
                
                self.rect.midleft = (traceX, traceY)
                pygame.draw.line(self.image, c, (0, 50), (imgW, 50), s)
                
        elif linkedX < traceX:
            
            if linkedY < traceY:
                
                self.rect.bottomright = (traceX, traceY)
                pygame.draw.line(self.image, c, (imgW, imgH), (0,0), s)
                
            elif linkedY > traceY:
                
                self.rect.topright = (traceX, traceY)
                pygame.draw.line(self.image, c, (imgW, 0), (0, imgH), s)
                
            elif linkedY == traceY:
                
                self.rect.midright = (traceX, traceY)
                pygame.draw.line(self.image, c, (imgW, 50,), (0, 50))
        
        elif linkedX == traceX:
            
            if linkedY > traceY:
                
                self.rect.midtop = (traceX, traceY)
                pygame.draw.line(self.image, c, (50, imgH), (50, 0))
                
            elif linkedY < traceY:
                
                self.rect.midbottom = (traceX, traceY)
                pygame.draw.line(self.image, c, (50, 0), (50, imgH))
          
    def clearImage(self):
        
        self.image = pygame.Surface((2,2)) 
        self.rect = self.image.get_rect()
        
def wipe():
    
    SwitchTracer.wipe()
        