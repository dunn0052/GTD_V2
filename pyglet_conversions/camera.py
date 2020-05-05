import pygame as pg

# this class is responsible for the game view
# it follows a rect and moves all other sprites
# relative to the targeted sprite
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.c = (1,1)
        self.width = width
        self.height = height

    # move entity relative to camera position
    def apply(self, entity):

        return entity.rect.move(self.camera.topleft)

    def applyCoord(self, entity):
        return entity.move(self.camera.topleft)

    # keeps target on center or
    # stops on edge of map edges
    def update(self, level):
        target = level.PC
        self.mapSize(level.mapHeight, level.mapWidth)
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.mapWidth - self.width), x)  # right
        y = max(-(self.mapHeight - self.height), y)  # bottom
        self.camera = pg.Rect(x, y, self.mapWidth, self.mapHeight)

    def moved(self):
        moved = (self.c[0] != self.camera.x or self.c[1] != self.camera.y)
        self.c = (self.camera.x, self.camera.y)
        return moved
 
    # define map edges
    def mapSize(self, height, width):
        self.mapHeight = height
        self.mapWidth = width