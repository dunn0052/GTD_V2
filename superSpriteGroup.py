import pygame as pg

class SuperSpriteGroup:

    _moved = True

    def __init__(self, width = 1920, height = 1024):
        self.canvas = pg.Surface((width, height), flags = pg.SRCALPHA)
        self.sprites = list()

    def draw(self, surface, offset = (0,0)):
        self.canvas.fill((0,0,0,0))
        for sprite in self.sprites:
            sprite.draw(self.canvas, offset)

        surface.blit(self.canvas, (0,0))

    def add(self, sprite):
        self.sprites.append(sprite)

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