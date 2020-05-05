import pygame as pg
import pyglet as pl 
from multiprocessing import Pool, freeze_support
from functools import partial

class SuperSpriteGroup:

    _moved = True
    _batch = pl.graphics.Batch()

    @staticmethod
    def draw():
        SuperSpriteGroup._batch.draw()

    @staticmethod
    def offset(sprite, offset):
        sprite.update(x = sprite.x + offset[0], y = sprite.y + offset[1])

    def __init__(self, order, width = 1920, height = 1024):
        self.sprites = list()
        self.group = pl.graphics.OrderedGroup(order)
        #self.offsetPool = Pool(4)

    def add(self, sprite):
        self.sprites.append(sprite)
        sprite.batch = self._batch
        sprite.group = self.group
        sprite.spriteGroup = self.sprites

    def update(self, dt):
        for sprite in self.sprites:
            sprite.updateTime(dt)

    def updateDrawingOffset(self, offsetCoords):
        '''
        f = partial(offset, offset = offsetCoords)
        self.offsetPool(f, self.sprites)
        '''
        for sprite in self.sprites:
            SuperSpriteGroup.offset(sprite, offsetCoords)

    def __iter__(self):
        for sprite in self.sprites:
            yield sprite

    def sprites(self):
        return self.sprites


    def sound(self):
        pass

    def darken(self, color):

        for sprite in self.sprites:
            sprite.image = self.shaded_image(sprite.image, color)

    def shaded_image(self, image, color):
        m = pg.mask.from_surface(image, 0)
        shader = pg.Surface((image.get_size()), masks=m).convert_alpha()
        shader.fill(color)
        copied = image.copy()
        copied.blit(shader, (0,0), special_flags=pg.BLEND_RGBA_MULT)
        return copied