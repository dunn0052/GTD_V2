import pygame as pg 
from level import Level 

# this class holds levels and manages level
# transitions, controllers, etc..
class Game:
    
    def __init__(self):
        self.levels = set()
        self.controllers = set()
        self.currentLevel = None
        self.levelIndex = 0

    def addController(self, controller):
        self.controllers.add(controller)

    def loadLevel(self, levelPath):
        self.levelBuffer = loadObject(levelPath)
        self.initLevel(self.levelBuffer.unpack())

    def initLevel(self, level, PC):
        self.currentLevel = level
        self.currentLevel.setController(self.controllers)
        self.addLevel(self.currentLevel)
        self.currentLevel.setPC(PC, 0, 0)

    def addLevel(self, level):
        self.levels.add(level)

    def setLevel(self, index, x, y):
        #self.screenFade()
        PC = self.currentLevel.PC
        # remove from current sprite update
        self.currentLevel.PC.kill()
        # avoid crashes
        if 0 < index < len(self.levels):
            self.currentLevel = self.levels[index]
        self.initLevel(self.currentLevel, PC)
        # add same PC to next level
        self.currentLevel.setPC(PC, x, y)

    # pass information about a level/game to the screen
    def update(self, dt):
        self.currentLevel.update(dt)