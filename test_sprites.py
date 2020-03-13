from superSprite import SuperSprite
from PC import PC
import pygame as pg
from game import Game
from level import Level
from screen import Screen
from controllerIO import Controller

c = Controller(0)
s = Screen()

test_level = Level()
test_level2 = Level()

bg = SuperSprite("images/pkBg.png")
bg2 = SuperSprite("images/house.png")

test_level.setBackground(bg)
test_level2.setBackground(bg2)

test_game = Game()
test_game.addController(c)

sprite = PC("images/csBig.png", 12, 100, 1, 300, 0)
test_game.initLevel(test_level, sprite)
test_game.addLevel(test_level2)


s.loadGame(test_game)
sprite.move(100,100)


s.run()
