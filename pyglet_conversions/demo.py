from console import Console 
from controllerIO import Controller 
import pyglet as pl
from game import Game
from levelSDK import PackedLevel

if __name__ == '__main__':
    c = Controller(0, keyboard=True)

    l1 = PackedLevel()
    l1.loadTileSheet("images/BWBG.png", 80, 80)
    # load walls
    # make PC
    # set pc into game
    g = Game()
    g.setTitle("Cat Mystery Dungeon")
    s = Console()
    s.set_controller(c)
    s.loadGame(g)
    s.run()