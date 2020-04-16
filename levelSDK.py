from level import Level
import objectRW
from superSprite import SuperSprite
from PC import PC
import npc
import levelTile
import levelTrigger
from spritesheet import spritesheet

import pygame as pg
import csv
import os

class packedLevel:

    def __init__(self):
        self.level = Level()
        self.startupCommands = list()

    def loadTileSheet(self, spriteSheetPath, tileHeight, tileWidth):
        self.tileHeight = tileHeight
        self.tileWidth =  tileWidth
        self.level.tileHeight = tileHeight
        self.level.tileWidth = tileWidth
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

    def loadBackground(self, backgroundImage = None):
        background = SuperSprite(0, 0, backgroundImage, 1)
        self.level.setBackground(background)

    def loadWalls(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTile.LevelTile(x = col * self.tileHeight, y = row * self.tileWidth, \
                                image = self.tiles[int(tile)])
                            self.level.WALL_LAYER.add(ent)
                            self.level.all_sprites.add(ent)
                            self.level.solid_sprites[(col, row)] = ent

    def loadTriggers(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = trigger.Trigger(x = col * self.tileHeight, y = row * self.tileWidth, \
                                height = self.tileHeight, width = self.tileWidth, transparent = True)
                            self.level.TRIGGER_LAYER.add(ent)
                            self.level.all_sprites.add(ent)

    def setTriggerCommand(self, index, command):
        # command must be a lambda function
        self.level.TRIGGER_LAYER.get_sprite(index).setInteraction(command)

    def loadLevelTriggers(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTrigger.LevelTransition(x = col * self.tileHeight, y = row * self.tileWidth, \
                                height = self.tileHeight, width = self.tileWidth, transparent = True)
                            ent.setLevel()
                            self.level.TRIGGER_LAYER.add(ent)
                            self.level.all_sprites.add(ent)
                            self.level.exit_triggers.add(ent)

    def setLevelChange(self, transition_index, level_index, pcx, pcy, pcdir):
        self.level.exit_triggers.get_sprite(transition_index).setLevel(level_index, pcx, pcy, pcdir)
        


    def loadOverhead(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTile.LevelTile(x = col * self.tileHeight, y = row * self.tileWidth, \
                                image = self.tiles[int(tile)])
                            self.level.OVER_LAYER.add(ent)
                            self.level.all_sprites.add(ent)

    def setDarkness(self, height, width, alpha):
        #set to size of screen
        self.level.darkness = pg.Surface((width, height))
        #fill with black
        self.level.darkness.fill((0,0,0))
        # adjust opacity
        self.level.darkness.set_alpha(alpha)

    def loadNPCs(self, filename):
        npc_index = 0
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = npc.NPC(x = col * self.tileWidth, y = row * self.tileHeight, \
                                image = self.tiles[int(tile)], frames = 1, speed = 0, starting_direction = 0)
                            self.level.NPC_LAYER.add(ent)
                            self.level.all_sprites.add(ent)
                            self.level.solid_sprites[(col, row)] = ent
                            self.level.npc_sprites.append(ent)
                            self.setNPCText(npc_index, str(npc_index))
                            npc_index += 1

    def setNPCText(self, index, text):
        self.level.npc_sprites[index].setText(text)
        self.level.talking_sprites.add(self.level.npc_sprites[index])

    def loadTextBox(self, sprite):
        self.level.text_box = sprite


    def loadAnimatedSprite(self, sprite):
        self.level.NPC_LAYER.add(sprite)
        self.level.all_sprites.add(sprite)
        #self.level.solid_sprites.add(sprite)
        self.level.animated_sprites.add(sprite)

#---------- PACK COMMANDS -----------
# These functions "spring load" image loading

    def unpackLevel(self):
        for command in self.startupCommands:
            command()
        return self.level

    