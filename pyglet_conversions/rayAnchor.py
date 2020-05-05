# RayTrace anchor blocks for corners
from math import floor
class RayAnchor:

    def __init__(self, coord, tileWidth, tileHeight):
        
        # pixel coordinate
        self.coord = coord

        (self.X, self.Y) = coord

        # tile coordinate
        #self.X = floor(self.X/tileWidth)
        #self.Y = floor(self.Y/tileHeight)

        self.topleft = (self.X, self.Y)
        self.topright = (self.X + tileWidth, self.Y)
        self.bottomleft = (self.X, self.Y + tileHeight)
        self.bottomright = (self.X + tileWidth, self.Y + tileHeight)
        
