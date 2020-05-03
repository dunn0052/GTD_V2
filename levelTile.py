import pygame as pg
import pyglet as pl 

class LevelTile(pg.sprite.DirtySprite):

    _images = dict()
    _plImages = dict()
    _moved = True

    def __init__(self, x, y, image, key):
        super().__init__()
        self.key = key
        self._images[self.key] = image
        self.rect = self._images[self.key].get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface, offset = (0,0)):
        surface.blit(self._images[self.key], \
        (self.rect.x + offset[0], self.rect.y + offset[1]))
