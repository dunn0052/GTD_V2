import pygame as pg
from ray2 import Ray
from pygame.math import Vector2
from pygame import gfxdraw


class RayGroup(object):

    # unit vector @ 0 rads
    _ref = pg.Vector2((1,1))

    def __init__(self, tileSize, mapSize, group):
        self._rays = list()

        # blit shadows onto surface and then blit surface onto screen
        #self.surface = pg.Surface(viewSize)

        # used in ray drawing calculations
        self._mapSize = mapSize
        
        self._tileSize = tileSize

        self._group = group

    def setSurface(self, viewWidth, viewHeight):
        self.surface = pg.Surface(viewWidth, viewHeight)

    def append(self, ray: Ray):
        self._rays.append(ray)
        self._rays[-1].setRayConstants(self._tileSize, self._mapSize, self._group)

    def __iter__(self):
        for ray in self._rays:
            yield ray

    def __getitem__(self, inded):
        self._rays.clear()

    def draw(self, screen, offset):

        offset = Vector2(offset, offset)
        self.sort()
        i = len(self._rays) - 1
        while i > -1:
            r1 = self._rays[i]
            r2 = self._rays[i-1]

            connected = [ r1.i + offset, r1.o + offset, r2.i + offset ]
            pg.gfxdraw.filled_polygon(screen, connected, (255,255,0))
            i -= 1
        
        #for ray in self._rays:
            #pg.draw.aaline(screen, (0,255,0), ray.o + offset, ray.i + offset)


    def sort(self):

        #sort by direction from (0,1)
        self._rays.sort(key = lambda ray: ray.v.angle_to(self._ref))

    def clear(self):
        self._rays.clear()