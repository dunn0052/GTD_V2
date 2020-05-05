import pygame as py 
from superSpriteGroup import SuperSpriteGroup as sg

class LayerContainer:

    def __init__(self, width = 1920, height = 1024):
        # push in screen dimensions
        self._screen = pg.Surface(width, height)
        self._screen.set_alpha(0)
        self._group = sg()

    # draw images from group onto layer screen
    def draw(self, group, offset):
        group.draw(self._screen)
        self.drawEffects()

    def drawEffects(self):
        for effect in self._effects:
            self._screen.blit()

    # draw layer screen to game screen
    def drawScreen(self, screen, camera):
        screen.blit(self._screen, )


    def add(self, ent):
        sg.add(ent)