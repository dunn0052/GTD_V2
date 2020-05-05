import pygame as pg
import pyglet as pl 

class LevelTile(pl.sprite.Sprite):

    _images = dict()
    _plImages = dict()
    _moved = True

    def __init__(self, x, y, image, key):
        super().__init__(image, x, y)
        self.key = key
        self._images[self.key] = image
        self.rect = self.getRect(image)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def getRect(self, image):
        return pg.Rect(image.x, image.y, image.width, image.height)

    def glLoad(self, image):
        self.glimage = pl.image.load(image)


    def drawGl(self):
        self.glimage.draw()