import pygame as pg
import pyglet as pl 
from superSpriteGroup import SuperSpriteGroup as sg


from camera import Camera
from audio import Audio


class Console:

    def __init__(self, Width = 1920, Height = 1080, fps = 60, refresh = 10, Title = "Cat Mystery Dungeon"):
        pg.init()
        self.width = Width
        self.height = Height

        self.controllers = []

        # camera size of screen
        self.camera = Camera(Width, Height)

        self.screen = pl.window.Window(visible=True, vsync = True, fullscreen=True)
        self.clock = pl.clock
        self.fps_display = pl.window.FPSDisplay(window=self.screen)
        self.on_draw = self.screen.event(self.on_draw)
        self.clock.schedule(self.loopUpdate)

    def loopUpdate(self, dt):
        self.doCommands()
        self.update(dt)

    def doCommands(self):
        self.game.doCommands()

    # updates the game and moves the camera
    def update(self, dt): 
        self.game.update(dt)
        self.camera.update(self.game.currentLevel)

    def on_draw(self):
        self.screen.clear()
        sg.draw()
        self.fps_display.draw()


    def set_controller(self, controller):
        self.controllers.append(controller)
        self.screen.push_handlers(self.controllers[-1].getKeyboardHandler())

    def run(self):
        pl.app.run()


    # will be used when level loading is created
    def loadGame(self, game):
        self.game = game
        self.screen.set_caption(self.game.title)
        self.game.start()
        self.loadLevel()

    # sets up a level to be displayed
    def loadLevel(self):
        self.camera.mapSize(self.game.currentLevel.mapHeight, self.game.currentLevel.mapWidth)
        self.game.currentLevel.setScreenSize(self.height, self.width)
