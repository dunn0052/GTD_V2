import pygame as pg

class Trigger(pg.sprite.Sprite):
    def __init__(self, x, y, height, width, interaction = lambda:print("Triggered"), transparent = False):

        pg.sprite.Sprite.__init__(self)

        if transparent:
            self.image = pg.Surface((width, height))
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pg.Surface((width, height))
            self.image.fill((255,0,0))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.interaction = interaction

    def interact(self):
        self.interaction()

    def setInteraction(self, interaction):
        self.interaction = interaction
