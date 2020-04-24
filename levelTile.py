import pygame as pg

class LevelTile(pg.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


    def draw(self, surface, offset = (0,0)):
        surface.blit(self.image, \
        (self.rect.x + offset[0], self.rect.y + offset[1]))
