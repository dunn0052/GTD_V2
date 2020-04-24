from superSprite import SuperSprite
from PC import PC
from text import TextBox
import pygame as pg
from game import Game
from level import Level
from screen import Screen
from controllerIO import Controller
import levelSDK

import cProfile

# Screen must be created first
s = Screen()

# house level
l = levelSDK.packedLevel()
l.loadTileSheet("images\BWBG.png", 80, 80)
l.loadBackground("images\house.png")
l.loadWalls("data\house_Tile Layer 2.csv")
l.loadNPCs("data\house_Tile Layer 3.csv")
l.loadLevelTriggers("data\house_Tile Layer 4.csv")
l.setRayAnchors("data\house_Tile Layer 5.csv")
l.loadOverhead("data\house_Tile Layer 5.csv")
l.setLevelChange(0, 0, 398, 485, 0)
l.setLevelChange(1, 0, 398, 485, 0)
l.setLevelChange(2, 0, 398, 485, 0)
l.setNPCText(0, "hey")
l.setDarkness(s.height, s.width, 0)

# outside level
o = levelSDK.packedLevel()
o.loadTileSheet("images\BWBG.png", 80, 80)
o.loadBackground("images/out.png")
o.loadWalls("data\out_Tile Layer 2.csv")
o.loadNPCs("data\out_Tile Layer 4.csv")
o.loadOverhead("data\out_Tile Layer 3.csv")
o.loadLevelTriggers("data\out_Tile Layer 5.csv")
o.setRayAnchors("data\out_Tile Layer 6.csv")
o.setLevelChange(2, 1, 293, 686, 3)
o.setLevelChange(0,2,653, 2553,0)
o.setLevelChange(1,2,653, 2553,0)
o.setNPCText(0, "sneakin by ya")
o.setDarkness(s.height, s.width, 150)

r = levelSDK.packedLevel()
r.loadTileSheet("images\BWBG.png", 80, 80)
r.loadBackground("images/rt1.png")
r.loadWalls("data/rt1_Tile Layer 2.csv")
r.loadNPCs("data/rt1_Tile Layer 3.csv")
r.loadLevelTriggers("data/rt1_Tile Layer 4.csv")
r.setRayAnchors("data/rt1_Tile Layer 5.csv")
r.setLevelChange(0, 0, 880, 175, 3)
r.setLevelChange(1, 0, 880, 175, 3)
r.setLevelChange(2, 0, 880, 175, 3)


c = Controller(0)

test_level = o.unpackLevel()
test_level2 = l.unpackLevel()
test_level3 = r.unpackLevel()

test_game = Game()
sprite = PC("images/redPC.png", 10, 100, 100, 300, 0, downFrame=3, leftFrame=2, rightFrame=2,upFrame=3)
#sprite.addLightImage("images/light.png")
#wheel = SuperSprite("images/wheel.png", 4)
#wheel.moveTo(100,100)
#l.loadAnimatedSprite(wheel)

test_text = TextBox("images/textBackground.png", offset= 80)

txt = ""
for i in range(50):
    txt += str(i) + "TEST "
test_text.setText(txt)
l.loadTextBox(test_text)
o.loadTextBox(test_text)
r.loadTextBox(test_text)

test_game.setPC(sprite)
test_game.addController(c)


test_game.addLevel(test_level)
test_game.addLevel(test_level2)
test_game.addLevel(test_level3)


s.loadGame(test_game)
sprite.move(100,100)


s.run()
#cProfile.run("s.runProfiler(1000)")