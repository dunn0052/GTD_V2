import pygame as pg 


class SuperSpriteGroup(pg.sprite.Group):

    def draw(self, surface, offset = (0,0)):
        for sprite in self.sprites():
            surface.blit(sprite.image, \
            (sprite.rect.x + offset[0], sprite.rect.y + offset[1]))