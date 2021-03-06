import pygame as pg 
from level import Level 

# this class holds levels and manages level
# transitions, controllers, etc..
class Game:
    
    def __init__(self):
        self.levels = list()
        self.controllers = set()
        self.currentLevel = None
        self.PC = None

    def start(self):
        self.currentLevel = self.levels[self.PC.level_index]
        self.currentLevel.setPC(self.PC, self.PC.x, self.PC.y)


    # controllers are in a set in case the same one is added more than once
    def addController(self, controller):
        self.controllers.add(controller)

    def loadLevel(self, levelPath):
        levelBuffer = loadObject(levelPath)
        self.addLevel(levelBuffer.unpack())

    def setPC(self, PC):
        self.PC = PC

    def changeLevel(self):
        PC = self.currentLevel.PC
        PC.rays.clear()
        self.currentLevel.stopBGMusic()
        self.currentLevel = self.levels[PC.level_index]
        self.currentLevel.setPC(PC, PC.x, PC.y)
        self.currentLevel.playBGMusic()


    # adds level on deck
    def addLevel(self, level):
        if self.PC:
            self.levels.append(level)
            self.levels[-1].setController(self.controllers)
            self.levels[-1].index = len(self.levels) -1
        else:
            print("Need to set a PC first")

    def doCommands(self):
        self.currentLevel.doCommands(self.controllers)

    # pass information about a level/game to the screen
    def update(self, dt):
        # handle level transitions
        if self.currentLevel.index != self.currentLevel.PC.level_index:
            self.changeLevel()
        self.currentLevel.update(dt)

    def getLevelIndex(self):
        return self.currentLevel.PC.getLevelIndex()