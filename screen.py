import pygame as pg
from camera import Camera
import os

# the screen object represents the screen/hardware of the game system
# it draws the layers of each level and updates game animation.

class Screen:

    def __init__(self, Height = 1280, Width = 1920, fps = 120, refresh = 10, Title = "Cat Mystery Dungeon"):
        pg.init()
        self.width = Width
        self.height = Height
        self.screen = pg.display.set_mode()
        pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.controllers = []
        # camera size of screen
        self.camera = Camera(Width, Height)

        # TIMING SETUP #
        self.fps = fps
        self.refresh = refresh
        self.next_frame = self.gameClock()
        self.screenRefresh = False
        self.tooSmall = False

    # will be used when level loading is created
    def loadGame(self, game):
        self.game = game
        self.game.start()
        self.loadLevel()

    # sets up a level to be displayed
    def loadLevel(self):
        self.camera.mapSize(self.game.currentLevel.mapHeight, self.game.currentLevel.mapWidth)
    
    def doCommands(self):
        self.game.doCommands()

    # starts the game
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(self.fps) / 1000
            self.doCommands()
            self.update()
            self.updateDisplay()

    def runProfiler(self, n):
        for _ in range(n):
            self.dt = self.clock.tick(self.fps) / 1000
            self.doCommands()
            self.update()
            self.updateDisplay()

    # updates the game and moves the camera
    def update(self):
        self.game.update(self.dt)
        # multiplayer take the average of player coords?
        self.camera.update(self.game.currentLevel)

    # redraw all sprites to screen
    # quit when necessary
    def updateDisplay(self):
        self.screen.fill((0,0,0))
        # explore dirty sprites
        for layer in self.game.currentLevel.layers:
                self.drawScrollLayer(layer)
        self.game.currentLevel.static_sprites.draw(self.screen)
        self.game.currentLevel.text_layer.draw(self.screen)
        pg.display.flip()
        keys = pg.key.get_pressed()
        if (keys[pg.K_ESCAPE]):
            self.quit()
        self.animate()

    def animate(self):
        self.game.currentLevel.animate()

    def gameClock(self):
        current_time = pg.time.get_ticks()
        return current_time

    # draws the level layers in order and
    # adjusts the sprites to the camera view
    def drawScrollLayer(self, layer):
        for sprite in layer:
            # keep sprite pos static and draw with camera offsets
            self.screen.blit(sprite.image, self.camera.apply(sprite))

    def quit(self):
        print("Game Ended")
        pg.quit()
        os._exit(1)
