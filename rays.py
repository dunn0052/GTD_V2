import pygame as pg
from math import sqrt
from math import floor
from math import tan
from math import atan2
from math import isnan


class Ray:

    def __init__(self, origin_coords, color = (255,0,0)):

        self.o = origin_coords
        self.e = (0,0)
        self.color = color
        self.offset = (0,0)
        self.intersect = (0,0)
        self.dx = 1
        self.dy = 1
        self.a = 0

    def draw(self, surface):
        o_coords = (self.o[0] + self.offset[0], self.o[1] + self.offset[1])
        i_coords = (self.intersect[0] + self.offset[0], self.intersect[1] + self.offset[1])
        e_coords = (self.e[0] + self.offset[0], self.e[1] + self.offset[1])
        pg.draw.line(surface, (255,0,0), o_coords, e_coords)
        pg.draw.line(surface, (0,0,255), o_coords, i_coords, 3)

        pg.draw.circle(surface, (255, 0 ,0), i_coords, 5)

    def move(self, coords):
        self.o = coords
        self.dy = self.e[1] - self.o[1]
        self.dx = self.e[0] - self.o[0]
        self.a = atan2(self.dy, self.dx)

    def attatch(self, coords):
        self.e = coords
        self.intersection(coords)
    
    def intersection(self, coord):
        self.intersect = coord

    def update(self, offset):
        self.offset = offset
            
    def findA(self, width, height):
        # ray is up
        if self.dy < 0:
            y = floor(self.o[1]/height) * height - 1
        else:
            y = floor(self.o[1]/height) * height + height

        safe = (self.o[1] - y)/tan(self.a) if tan(self.a) != 0 else width
        x = self.o[0] - safe

        return (x, y)

    def isWallA(self, coord, height, width, group):
        coord = (floor((coord[0])/width), floor(coord[1]/height))
        return coord in group

    def isWallB(self, coord, height, width, group):
        coord = (floor((coord[0])/width), floor((coord[1])/height))
        return coord in group

    def extendY(self, height, width, group):

        A = self.findA(width, height)

        # immediately in front
        if self.isWallA(A, height, width, group):
            #self.intersection(A)
            return A
        
        if self.dy < 0:
            Ya = -height
        else:
            Ya = height
        
        Xa = -width/tan(self.a) if tan(self.a) != 0 else width

        X = A[0]
        Y = A[1]

        if self.dx <= 0 and self.dy <= 0:
            while X > self.e[0] and Y > self.e[1]:
                if self.isWallA((X, Y), height, width, group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X += Xa
                Y += Ya

        if self.dx >= 0 and self.dy <= 0:
            while X < self.e[0] and Y > self.e[1]:
                if self.isWallA((X, Y), height, width, group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X += Xa
                Y += Ya

        if self.dx >= 0 and self.dy >= 0:
            while X < self.e[0] and Y < self.e[1]:
                if self.isWallA((X, Y), height, width, group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X -= Xa
                Y += Ya

        if self.dx <= 0 and self.dy >= 0:
            while X > self.e[0] and Y < self.e[1]:
                if self.isWallA((X, Y), height, width, group):
                    #self.intersection((X, Y))
                    return (X,Y)
                X -= Xa
                Y += Ya
             
        #self.intersection(self.e)
        return (X,Y)

    def findB(self, width, height):

        # check if ray is left or right
        
        if self.dx < 0:
            # ray is right
            x = floor(self.o[0]/width) * width - 1
        else:
            #ray is right
            x = floor(self.o[0]/width) * width + width

        y = self.o[1] - (self.o[0] - x)*tan(self.a)
        return (x, y)

    def extendX(self, height, width, group):

            B = self.findB(width, height)

            if self.isWallB(B, height, width, group):
                return B

            if self.dx < 0:
                Xb = - height
            else:
                Xb = height
            
            Yb = height*-tan(self.a)

            X = B[0]
            Y = B[1]

            if self.dx <= 0 and self.dy <= 0:
                while X > self.e[0] and Y > self.e[1]:
                    if self.isWallB((X, Y), height, width, group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y += Yb

            if self.dx >= 0 and self.dy <= 0:
                while X < self.e[0] and Y > self.e[1]:
                    if self.isWallB((X, Y), height, width, group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y -= Yb

            if self.dx >= 0 and self.dy >= 0:
                while X < self.e[0] and Y < self.e[1]:
                    if self.isWallB((X, Y), height, width, group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y -= Yb

            if self.dx <= 0 and self.dy >= 0:
                while X > self.e[0] and Y < self.e[1]:
                    if self.isWallB((X, Y), height, width, group):
                        self.intersection((X, Y))
                        return (X,Y)
                    X += Xb
                    Y += Yb              

            #self.intersection(self.e)
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

    def extend(self, height, width, group):

        A = self.findA(width, height)
        B = self.findB(width, height)

        (Xa, Ya) = A
        (Xb, Yb) = B

        if self.dx < 0:
            Xbi = - height
        else:
            Xbi = height
        
        Ybi = height*-tan(self.a)

        # set up increments for B
        if self.dy < 0:
            Yai = -height
        else:
            Yai = height
        
        Xai = -width/tan(self.a)

        if self.dx <= 0 and self.dy <= 0:
            while (Xa > self.e[0] and Ya > self.e[1]) or (Xb > self.e[0] and Yb > self.e[1]):
                WallA = self.isWallA((Xa, Ya), height, width, group)
                WallB = self.isWallB((Xb, Yb), height, width, group)
                if WallA and WallB:
                    self.intersection(self.closest((Xa, Ya), (Xb, Yb)))
                    return None
                elif WallA:
                    self.intersection((Xa, Ya))
                    return None
                elif WallB:
                    self.intersection((Xb, Yb))
                    return None

                Xa += Xai
                Xb += Xbi
                Ya += Yai
                Yb += Ybi

        
        if self.dx > 0 and self.dy < 0:
            while (Xa < self.e[0] and Ya > self.e[1]) or (Xb < self.e[0] and Yb > self.e[1]):
                WallA = self.isWallA((Xa, Ya), height, width, group)
                WallB = self.isWallB((Xb, Yb), height, width, group)
                if WallA and WallB:
                    self.intersection(self.closest((Xa, Ya), (Xb, Yb)))
                    return None
                elif WallA:
                    self.intersection((Xa, Ya))
                    return None
                elif WallB:
                    self.intersection((Xb, Yb))
                    return None

                Xa += Xai
                Xb += Xbi
                Ya += Yai
                Yb -= Ybi


        if self.dx < 0 and self.dy > 0:
            while (Xa > self.e[0] and Ya < self.e[1]) or (Xb > self.e[0] and Yb < self.e[1]):
                WallA = self.isWallA((Xa, Ya), height, width, group)
                WallB = self.isWallB((Xb, Yb), height, width, group)
                if WallA and WallB:
                    self.intersection(self.closest((Xa, Ya), (Xb, Yb)))
                    return None
                elif WallA:
                    self.intersection((Xa, Ya))
                    return None
                elif WallB:
                    self.intersection((Xb, Yb))
                    return None

                Xa -= Xai
                Xb += Xbi
                Ya += Yai
                Yb -= Ybi


        if self.dx > 0 and self.dy > 0:
            while (Xa < self.e[0] and Ya < self.e[1]) or (Xb < self.e[0] and Yb < self.e[1]):
                WallA = self.isWallA((Xa, Ya), height, width, group)
                WallB = self.isWallB((Xb, Yb), height, width, group)
                if WallA and WallB:
                    self.intersection(self.closest((Xa, Ya), (Xb, Yb)))
                    return None
                elif WallA:
                    self.intersection((Xa, Ya))
                    return None
                elif WallB:
                    self.intersection((Xb, Yb))
                    return None

                Xa -= Xai
                Xb += Xbi
                Ya += Yai
                Yb += Ybi


        
        self.intersection(self.e)
                

    def rayTrace(self, height, width, group):
        X = self.extendX(height, width, group)
        Y = self.extendY(height, width, group)
        self.intersection(self.closest(X, Y))
            

            


