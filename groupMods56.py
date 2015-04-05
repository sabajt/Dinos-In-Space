""" groupMods56.py
    modifcation of pygame sprite module
    autocenters rects that are smaller or equal to image - makes clean spin """

import pygame

class SmallRectGroup(pygame.sprite.Group):

    """ -extends pygame group
        -overrides draw method to blit image at center, not (0,0)
        -WARNING: sprite.image MUST BE LARGER THAN sprite.rect! """

    def draw(self, surface):
        """ modification of pygame.Group.draw method
            blits image at imageOffset instead of rect """

        sprites = self.sprites()
        surface_blit = surface.blit

        for spr in sprites:

            # gets point for blitting offsetted image
            rectWidth = spr.rect.right - spr.rect.left
            squareOffset = (spr.image.get_width() - rectWidth)/2
            imageOffsetPoint = (spr.rect.left - squareOffset,
                                spr.rect.top - squareOffset)

            # does what the normal group.draw does, but with imageOffset
            self.spritedict[spr]    = surface_blit(spr.image, imageOffsetPoint)

        self.lostsprites = []

class SR_OrderedUpdates(pygame.sprite.OrderedUpdates):
    """ adds small rect blitting (see above) to pygame OrderedUpdates """

    def draw(self, surface):

        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append

        for s in self.sprites():

            r = spritedict[s]

            # gets point for blitting offsetted image

            rectWidth = s.rect.right - s.rect.left
            squareOffset = (s.image.get_width() - rectWidth)/2
            imageOffsetPoint = (s.rect.left - squareOffset,
                                s.rect.top - squareOffset)

            # does what the normal OrderedUpdates.draw does, but with imageOffset

            newrect = surface_blit(s.image, imageOffsetPoint)

            if r is 0:
               dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty


if __name__ == "__main__":

    print "module for import only"