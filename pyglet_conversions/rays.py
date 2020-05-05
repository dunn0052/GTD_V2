import pygame as pg
from math import sqrt
from math import floor
from math import atan2
from math import tan

class Ray:

    _levelwidth = 80*20 + 20
    _levelheight = 0
    def __init__(self, origin_coords, width, height, color = (255,0,0), image = None):

        # origin coordinates - source of light
        self.o = origin_coords
        
        # used to calculate dy/dx of corner from o
        self.e = (0,0)

        # main trace
        self.w = (0,0)
        # upper and lower traces
        self.w1 = (0,0)
        self.w2 = (0,0)

        self.color = color
        # where to move the ray drawing - not used
        self.offset = (0,0)
        # where the ray collides with a solid object
        self.i= (0,0)
        self.dx = 1
        self.dy = 1
        self.a = 0
        self.width = width
        self.height = height
        self.length = list()
        if image:
            self.image = pg.image.load(image)

    def draw(self, surface, offset = (0,0)):
        o_coords = (self.o[0] + offset[0], self.o[1] + offset[1])
        i_coords = (self.i[0] + offset[0], self.i[1] + offset[1])
        e_coords = (self.e[0] + offset[0], self.e[1] + offset[1])
        pg.draw.aaline(surface, (0,0,255), o_coords, i_coords)

        pg.draw.circle(surface, (255, 0 ,0), self.w1, 5)

    def move(self, coords):
        self.o = coords
        self.dy = self.e[1] - self.o[1]
        self.dx = self.e[0] - self.o[0]

        d1 = tan(atan2(self.dy, self.dx) + 0.01)
        d2 = tan(atan2(self.dy, self.dx) - 0.01)
        # if right
        if self.dx > 0:
            y = (self._levelwidth - self.o[0])* d1+ self.o[1]
            self.w1 = (self._levelwidth, y)
        elif self.dx < 0:
            y = self.o[0] * -d2 + self.o[1]
            self.w1 = (0, y)
        else:
            self.w1 = (self.o[0], 0)

        if self.dx > 0:
            y = (self._levelwidth - self.o[0])* d1+ self.o[1]
            self.w2 = (self._levelwidth, y)
        elif self.dx < 0:
            y = self.o[0] * -d2 + self.o[1]
            self.w2 = (0, y)
        else:
            self.w2 = (self.o[0], 0)

        
        if self.dx > 0:
            y = (self._levelwidth - self.o[0]) * self.dy/self.dx + self.o[1]
            self.w = (self._levelwidth, y)
        elif self.dx < 0:
            y = self.o[0] * -self.dy/self.dx + self.o[1]
            self.w = (0, y)
        else:
            self.w = (self.o[0], 0)


    # @TODO use attatch to calculate dy/dx only
    # then attach end edges of map
    def attatch(self, coords):
        self.e = coords
        self.intersection(coords)
        # needed to set dy/dx
        self.move(self.o)
    
    def intersection(self, coord):
        self.i = coord

    def update(self, offset):
        self.offset = offset
            
    def findA(self):
        # ray is up
        if self.dy < 0:
            y = floor(self.o[1]/self.height) * self.height - 1
        else:
            y = floor(self.o[1]/self.height) * self.height + self.height

        safe = (self.o[1] - y)*self.dx/self.dy if self.dy != 0 else self.width
        x = self.o[0] - safe

        return (x, y)

    def isWall(self, coord, group):
        coord = (floor((coord[0])/self.width), floor(coord[1]/self.height))
        return coord in group

    def extendY(self, coord, group):

        A = self.findA()

        # immediately in front
        if self.isWall(A, group):
            #self.intersection(A)
            return A
        
        if self.dy < 0:
            Ya = -self.height
        else:
            Ya = self.height
        
        Xa = -self.width*self.dx/self.dy if self.dy != 0 else self.width*self.sign(self.dx)*self.sign(self.dy)

        X = A[0]
        Y = A[1]

        if self.dx <= 0 and self.dy <= 0:
            while X > coord[0] and Y > coord[1]:
                if self.isWall((X, Y), group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X += Xa
                Y += Ya

        if self.dx >= 0 and self.dy <= 0:
            while X < coord[0] and Y > coord[1]:
                if self.isWall((X, Y), group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X += Xa
                Y += Ya

        if self.dx >= 0 and self.dy >= 0:
            while X < coord[0] and Y < coord[1]:
                if self.isWall((X, Y), group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X -= Xa
                Y += Ya

        if self.dx <= 0 and self.dy >= 0:
            while X > coord[0] and Y < coord[1]:
                if self.isWall((X, Y), group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X -= Xa
                Y += Ya
             
        #self.intersection(self.w)
        return (X,Y)

    def findB(self):

        # check if ray is left or right
        
        if self.dx < 0:
            # ray is right
            x = floor(self.o[0]/self.width) * self.width - 1
        else:
            #ray is right
            x = floor(self.o[0]/self.width) * self.width + self.width

        y = self.o[1] - (self.o[0] - x)*self.dy/self.dx if self.dx !=0 else self.o[1]
        return (x, y)

    def extendX(self, coord, group):

            B = self.findB()

            if self.isWall(B, group):
                return B

            if self.dx < 0:
                Xb = - self.height
            else:
                Xb = self.height
            
            Yb = self.height*-self.dy/self.dx if self.dx !=0 else -self.width

            (X, Y) = B


            if self.dx <= 0 and self.dy <= 0:
                while X > coord[0] and Y > coord[1]:
                    if self.isWall((X, Y), group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y += Yb

            if self.dx >= 0 and self.dy <= 0:
                while X < coord[0] and Y > coord[1]:
                    if self.isWall((X, Y), group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y -= Yb

            if self.dx >= 0 and self.dy >= 0:
                while X < coord[0] and Y < coord[1]:
                    if self.isWall((X, Y), group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y -= Yb

            if self.dx < 0 and self.dy > 0:
                while X > coord[0] and Y < coord[1]:
                    if self.isWall((X, Y), group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y += Yb              

            #self.intersection(self.w)
            return (X,Y)


    def sign(self, n):
        if n < 0:
            return -1
        else:
            return 1

    def lineLength(self, coord):
        return sqrt((self.o[0] - coord[0])**2 + (self.o[1] -coord[1])**2)

    def closest(self, A, B):
        if self.lineLength(A) <= self.lineLength(B):
            return A
        else:
            return B

    def fastClosest(self, A, B):
        if abs(A[0]) < abs(B[0]):
            return A
        else:
            return B

    def calcRay(self, coord, group):
        X = self.extendX(coord, group)
        Y = self.extendY(coord, group)
        return self.closest(X, Y)
                
    def rayTrace(self, group):
        self.length.clear()
        self.length.append(self.calcRay(self.w, group))
        self.length.append(self.calcRay(self.w1, group))
        self.length.append(self.calcRay(self.w2, group))

        self.length.sort(key = lambda r: self.lineLength(r))
        i = self.length[-1]

        self.intersection(i)

        '''
        raytrace for w1, w2
        '''

            

            


