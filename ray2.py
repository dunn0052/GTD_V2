import pygame as pg 
from pygame.math import Vector2 
from math import floor, cos, sin

class Ray:

    _group = set()
    _mapSize = (0,0)
    _tileSize = (0,0)

    # start= origin, end = attached coord, width = tilewidth, height = tilehidth
    def __init__(self, start, end, tileSize = None, mapSize = None, group = None):
        self.o = pg.Vector2(start)
        self.e = pg.Vector2(end)
        self.i = pg.Vector2(0,0)
        self.calculateTileVector()
        self.type = 0


        #testing
        self.gridXHits = list()
        self.gridYHits = list()
        self.x = pg.Vector2(0,0)
        self.y = pg.Vector2(0,0)

        if tileSize and mapSize and group:
            self.setRayConstants(tileSize, mapSize, group)

    def setRayConstants(self, tileSize, mapSize, group):
        self._group = group
        self._mapSize = mapSize
        self._tileSize = tileSize

    # calculate 1 tile unit
    def calculateTileVector(self):
        self.v = self.e - self.o
        if self.v.length() != 0:
            self.u = self.v.normalize() * self._tileSize[0]
        else:
            self.u = self.v

    def move(self, coord):
        self.o.update(coord)
        self.calculateTileVector()


    def attach(self, coord):
        self.e.update(coord)
        self.calculateTileVector()

    def intersect(self, coord):
        self.i.update(coord)

    # get all ray anchor corner coordinates
    def isWall(self, coord):
        coord = (floor((coord.x)/self._tileSize[0]), floor(coord.y/self._tileSize[1]))
        return coord in self._group

    def notWall(self, coord):
        coord = (floor((coord.x)/self._tileSize[0]), floor(coord.y/self._tileSize[1]))
        return coord not in self._group


    def firstY(self):

        if self.v.y < 0:
            # get next tile height and - 1
            y = floor(self.o.y/self._tileSize[1]) * self._tileSize[1] - 1
        else:
            # else get tile height and move down one tile
            y = floor(self.o.y/self._tileSize[1]) * self._tileSize[1] + self._tileSize[1]


        # find x coordinate by multiplying dy to the next tile and find the x change in the vector direction
        safe = (self.o.y - y)*self.v.x/self.v.y if self.v.y != 0 else self._tileSize[0]
        x = self.o.x - safe

        return pg.Vector2(x,y)

    def firstX(self):

        # check if ray is left or right
        
        if self.v.x < 0:
            # ray is right
            x = floor(self.o.x/self._tileSize[0]) * self._tileSize[0] - 1
        else:
            #ray is right
            x = floor(self.o.x/self._tileSize[0]) * self._tileSize[0] + self._tileSize[0]

        y = self.o.y - (self.o.x - x)*self.v.y/self.v.x if self.v.x !=0 else self.o.y - self._tileSize[1]
        return pg.Vector2(x,y)

    def inBounds(self, coord):
        return 0 < coord.x < self._mapSize[0] and 0 < coord.y < self._mapSize[1]

    def rayTrace(self):

        # starting points on first tile bounds
        X, Y = self.firstX(), self.firstY()
        wall_bit = 0
        bounds_bit = 0
        Xv = self.v * abs((self._tileSize[0]/self.v.x)) if self.v.x !=0 else pg.Vector2(0, self._tileSize[1])
        Yv = self.v * abs((self._tileSize[1]/self.v.y)) if self.v.y !=0 else pg.Vector2(self._tileSize[0], 0)

        #[X in bounds, Y in bounds, X wall hit, Y wall hit]
        # 8 4 2 1
        draw_bit = 0b0000

        while (~draw_bit&8 and ~draw_bit&1) or (~draw_bit&4 and ~draw_bit&2):

            #self.gridXHits.append((X.x, X.y))
            #self.gridYHits.append((Y.x, Y.y))

            #bounds_bit |= self.inBounds(X) | self.inBounds(Y) << 1

            # set flags
            draw_bit |= self.isWall(X) | self.isWall(Y) << 1\
                     | (not self.inBounds(Y))<<2 | (not self.inBounds(X))<<3
            '''
            if wall_bit == 3:
                self.type = wall_bit
                break
            '''

            if ~draw_bit&1:
                X += Xv
            if ~draw_bit&2:
                Y += Yv

        self.intersect(min(X, Y, key = lambda ray: ray.distance_to(self.o)))

