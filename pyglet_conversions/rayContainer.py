import pygame as pg
from rays import Ray
from math import atan2
from math import pi
from pygame import gfxdraw

# A container for rays that can draw

class RayContainer():

    def __init__(self, height = 0, width = 0):
        self._rays =  list()
        self.surface = pg.Surface((width, height))


    def setSurface(self, x, y):
        self.surface = pg.Surface((x, y))
        
    def append(self, ray: Ray):
        self._rays.append(ray)

    def __iter__(self):
        for ray in self._rays:
            yield ray

    def __getitem__(self, index):
         return self._rays[index]

    def clear(self):
        self._rays.clear()

    def draw(self, screen, offset, color = (0,0,255)):

        self.sort()
        points1 = list()
        points2 = list()

        i = len(self._rays) - 1
        while i > -1:
            r1 = self._rays[i]
            r2 = self._rays[i-1]
            connected = [(r1.i[0] + offset[0], r1.i[1] + offset[1]), \
                         (r1.o[0] + offset[0], r1.o[1] + offset[1]), \
                         (r2.i[0] + offset[0], r2.i[1] + offset[1])]
            pg.gfxdraw.textured_polygon(screen, connected, self._rays[i].image, 0, 0)

            # used to draw aux traces
            points1.append((r1.o[0] + offset[0], r1.o[1] + offset[1]))
            points1.append((r1.w1[0] + offset[0], r1.w1[1] + offset[1]))
            points2.append((r1.o[0] + offset[0], r1.o[1] + offset[1]))
            points2.append((r1.w2[0] + offset[0], r1.w2[1] + offset[1]))

            '''
            pg.draw.aaline(screen, (0,255,0), \
                        (r1.o[0] + offset[0], r1.o[1] + offset[1]), \
                        (r1.w1[0] + offset[0], r1.w1[1] + offset[1]))
            
            pg.draw.aaline(screen, (0, 0, 255), \
                        (r1.o[0] + offset[0], r1.o[1] + offset[1]), \
                        (r1.w2[0] + offset[0], r1.w2[1] + offset[1]))
            '''
            pg.draw.circle(screen, (255,0,0), (r1.i[0] + offset[0], r1.i[1] + offset[1]), 5)
            i -= 1
        
        if points1 and points2:
            pg.draw.aalines(screen, (0,255,0), False, points1, False)
            pg.draw.aalines(screen, (0,255, 0), False, points2, False)

        points = list()
        for ray in self._rays:
            points.append((ray.o[0] + offset[0], ray.o[1] + offset[1]))
            points.append((ray.i[0] + offset[0], ray.i[1] + offset[1]))
        
        #if points:
            #pg.draw.aalines(screen, (255,0,0), False, points, False)

    def angle(self, A, B):
        ang1 = atan2(*A[::-1])
        ang2 = atan2(*B[::-1])
        return ((ang1 - ang2) % (2 * pi))

    # sort by angle
    def sort(self):
        self._rays.sort(key = lambda ray: atan2(ray.i[0] - ray.o[0], ray.i[1] - ray.o[1]))

    '''
    def update(self, update with PC)
    '''