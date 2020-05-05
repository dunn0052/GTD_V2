from level import Level
import objectRW
from PC import PC
from BACKGROUND import Background
import WALL
import pygame as pg
from spritesheet import spritesheet
import csv
import os

class MapMaker:

    def __init__(self, layers = 7, name = "NoName"):
        # create new level
        # default name should change to not overwrite another default
        self.newLevel = Level(layers, name)
        self.runningCommands = []


# functions needed when running
    def addRunningCommand(self, command):
        self.runningCommands.append(command)
# functions a level doesn't need while running

    def unpackLevel(self):
        for command in self.runningCommands:
            command()
        return self.newLevel

    def packBackground(self, backgroundImage):
        self.addRunningCommand(lambda: self.loadBackground(backgroundImage))

    def packTileSheet(self, tileSheet, tileHeight, tileWidth):
        self.addRunningCommand(lambda: self.loadTileSheet(tileSheet, tileHeight, tileWidth))

    def packWallMap(self, path):
        self.addRunningCommand(lambda:self.loadWalls(path))
    def packNpcMap(self, path):
        self.addRunningCommand(lambda:self.loadNpcs(path))
    def packTriggerMap(self, path):
        self.addRunningCommand(lambda:self.loadTriggers(path))
    def packOverMap(self, path):
        self.addRunningCommand(lambda:self.loadOver(path))
    def packWeatherMap(self, path):
        self.addRunningCommand(lambda:self.loadWeather(path))

    def packPCMap(self, x, y, image, spd, direction, frames, cycle, frameSpeed):
        self.addRunningCommand(lambda:self.packPC(PC(x = x, y = y, image = image, spd = spd, direction = direction, frames = frames, cycle = cycle, level = self.newLevel, frameSpeed = frameSpeed), x, y))



    def saveLevel(self):
        path = "levels//" + self.newLevel.name + ".pkl"
        objectRW.saveObject(self, path)

    def loadBackground(self, backgroundImage = None):
        if backgroundImage:
            self.newLevel.background = Background(x = 0, y = 0, image = backgroundImage)
        else:
            self.newLevel.background = Background(x = 0, y = 0, level = self, height = 10000, width = 19200)

        self.newLevel.BACKGROUND.add(self.newLevel.background)
        self.newLevel.all_sprites.add(self.newLevel.background)


    def packPC(self, PC, x, y):
        self.newLevel.setPC(PC, x, y)

    def packEnemy(self, ene):
        self.addRunningCommand(lambda: self.addEnemy(ene))


    def addExit(self,level):
        self.newLevel.exit.append(level)


    # factory for game objects
    def makeEnt(self, entType, image = None, x = 0, y = 0, frames = 12, direction = 1, cycle = 3, spd = 200, interaction = None, frameSpeed = 100):
        entType = entType.upper()
        if entType == "WALL":
            entity = WALL.Wall(x, y, image)
            self.newLevel.all_sprites.add(entity)
            self.newLevel.WALL_LAYER.add(entity)
        elif entType == "PLAYER":
            entity = PC(x, y, image, spd, direction, frames, cycle, level = self, frameSpeed = frameSpeed)
            self.newLevel.packPC(entity, x, y)
        elif entType == "NPC":
            entity = NPC.Npc(image, x, y, frames, direction, cycle, spd, level = self)
            self.newLevel.all_sprites.add(entity)
            self.newLevel.NPC_LAYER.add(entity)
        elif entType == "TRIGGER":
            entity = TRIGGER.Trigger(x, y, 64,64, interact = interaction, transparent = True, level = self)
            self.newLevel.all_sprites.add(entity)
            self.newLevel.TRIGGER_LAYER.add(entity)
        elif entType == "ANIMATION":
            entity = NPC.Npc(image = image, x = x, y = y, frames = frames, level = self)
            self.newLevel.all_sprites.add(entity)
            self.newLevel.NPC_LAYER.add(entity)
            self.newLevel.animated_sprites.add(entity)
            self.newLevel.solid_sprites.add(entity)
        elif entType == "MELE":
            entity = mele.Mele(image = image, x = x, y = y, frames = frames, frameSpeed = 10)
            self.newLevel.all_sprites.add(entity)
            self.newLevel.NPC_LAYER.add(entity)


    def loadTileSheet(self, spriteSheetPath, tileHeight, tileWidth):
        self.tileHeight = tileHeight
        self.tileWidth =  tileWidth
        self.newLevel.tileHeight = tileHeight
        self.newLevel.tileWidth = tileWidth
        self.sheet = spritesheet(spriteSheetPath, tileHeight, tileWidth)
        self.tiles = self.sheet.get_tiles()
    # Level has a map class to help design levels
    def loadData(self, filename):
        data = []
        if filename.endswith(".txt"):
            with open(filename, 'rt') as f:
                for line in f:
                    data.append(line.strip())
        elif filename.endswith(".csv"):
            with open(filename, 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    data.append(row)
        return data

    def loadWalls(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = WALL.Wall(x = col * self.tileHeight, y = row * self.tileWidth, image = self.tiles[int(tile)])
                            self.newLevel.WALL_LAYER.add(ent)
                            self.newLevel.all_sprites.add(ent)
                            self.newLevel.solid_sprites.add(ent)

    def loadTriggers(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = TRIGGER.Trigger(x = col * self.tileHeight, y = row * self.tileWidth, height = self.tileHeight, width = self.tileWidth, transparent = True)
                            self.newLevel.TRIGGER_LAYER.add(ent)
                            self.newLevel.all_sprites.add(ent)

    def loadNpcs(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = NPC.Npc(x = col * self.tileHeight, y = row * self.tileWidth, image = self.tiles[int(tile)], level = self)
                            self.newLevel.NPC_LAYER.add(ent)
                            self.newLevel.all_sprites.add(ent)
                            self.newLevel.solid_sprites.add(ent)
                            self.newLevel.npc_sprites.add(ent)

    def addEnemy(self, enemy):
        ene = enemy()
        self.newLevel.enemy_sprites.add(ene)
        self.newLevel.solid_sprites.add(ene)
        self.newLevel.NPC_LAYER.add(ene)
        self.newLevel.all_sprites.add(ene)
        self.newLevel.animated_sprites.add(ene)
        ene.move(ene.x, ene.y)

    def loadOver(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = over.Over(x = col * self.tileHeight, y = row * self.tileWidth, image = self.tiles[int(tile)])
                            self.newLevel.OVER_LAYER.add(ent)
                            self.newLevel.all_sprites.add(ent)



    def loadWeather(self, filename):
        ent = None
        #self.newLevel.WEATHER_LAYER.add()

    def makeText(self, text):
        self.newLevel.text = Textbox(text = text, backgroundImage = "images//textBackground.png", offset = 65, level = self.newLevel)
        self.newLevel.all_sprites.add(self.newLevel.text)
        self.newLevel.text_layer.add(self.newLevel.text)
        self.newLevel.setControllerContext(self.newLevel.text)

    def addNpcDialogue(self, NPCnum, text):
        # get NPC and add dialogue function
        self.newLevel.NPC_LAYER.get_sprite(NPCnum).setInteraction(lambda:self.makeText(text))
