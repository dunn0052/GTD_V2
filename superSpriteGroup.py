import pygame as pg

class SuperSpriteGroup(pg.sprite.Group):
    #_canvas = pg.Surface((1920,1024))

    def __init__(self, width = 1920, height = 1024):
        self.canvas = pg.Surface((width, height), flags = pg.SRCALPHA)
        super().__init__()

    def draw(self, surface, offset = (0,0), effect = None):
        self.canvas.fill((0,0,0,0))
        for sprite in self.sprites():
            self.canvas.blit(sprite.image, \
                (sprite.rect.x + offset[0], sprite.rect.y + offset[1]))

        surface.blit(self.canvas, (0,0))


    def sound(self):
        pass

    def darken(self, color):

        for sprite in self.sprites():
            sprite.image = self.shaded_image(sprite.image, color)

    def shaded_image(self, image, color):
        m = pg.mask.from_surface(image, 0)
        shader = pg.Surface((image.get_size()), masks=m).convert_alpha()
        shader.fill(color)
        copied = image.copy()
        copied.blit(shader, (0,0), special_flags=pg.BLEND_RGBA_MULT)
        return copied