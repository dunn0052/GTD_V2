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

    # controllers are in a set in case the same one is added more than once
    def addController(self, controller):
        self.controllers.add(controller)

    def loadLevel(self, levelPath):
        self.levelBuffer = loadObject(levelPath)
        self.initLevel(self.levelBuffer.unpack())
    # start a level to be used by the screen
    def initLevel(self, level, PC):
        self.currentLevel = level
        self.currentLevel.setController(self.controllers)
        self.addLevel(self.currentLevel)
        self.currentLevel.setPC(PC, 0, 0)
        
    # adds level on deck
    def addLevel(self, level):
        self.levels.add(level)

    # changes the current level to another one
    def setCurrentLevel(self, index, x, y):
        #self.screenFade()
        PC = self.currentLevel.PC
        # remove from current sprite update
        self.currentLevel.PC.kill()
        # avoid crashes
        if 0 < index < len(self.levels):
            self.currentLevel = self.levels[index]
        self.initLevel(self.currentLevel, PC)

    # pass information about a level/game to the screen
    def update(self, dt):
        self.currentLevel.update(dt)