# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame

class spritesheet(object):
    def __init__(self, filename, tileHeight, tileWidth):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.tileHeight = tileHeight
        self.tileWidth = tileWidth
        self.height = self.sheet.get_height()
        self.width = self.sheet.get_width()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def get_tiles(self):
        extraHeight = self.height%self.tileHeight
        extraWidth = self.width%self.tileWidth
        if(extraHeight != 0 or extraWidth != 0):
            print("Sheet excess of ", extraHeight, "pixels in height.")
            print("Sheet excess of ", extraWidth, "pixels in width")
        self.tiles = []
        # in tile order
        for y in range(0, self.height, self.tileHeight):
            for x in range(0, self.width, self.tileWidth):
                # rect at top left of x, y, width, heigh to cut out of sheet
                self.tiles.append(self.image_at((x, y, self.tileWidth, self.tileHeight)))
        return self.tiles
