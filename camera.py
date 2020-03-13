import pygame as pg

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.mapWidth - self.width), x)  # right
        y = max(-(self.mapHeight - self.height), y)  # bottom
        self.camera = pg.Rect(x, y, self.mapWidth, self.mapHeight)

    def mapSize(self, height, width):
        self.mapHeight = height
        self.mapWidth = width