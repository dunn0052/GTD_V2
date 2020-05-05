import pygame as pg
from camera import Camera
from audio import Audio
import os

#testing
from ray2 import Ray

# the screen object represents the screen/hardware of the game system
# it draws the layers of each level and updates game animation.

class Screen:

    def __init__(self, Height = 1280, Width = 1920, fps = 120, refresh = 10, Title = "Cat Mystery Dungeon"):
        pg.init()
        self.width = Width
        self.height = Height
        self.screen = pg.display.set_mode(flags = pg.HWSURFACE | pg.DOUBLEBUF)
        pg.display.set_caption(Title)
        print(pg.display.Info())
        self.clock = pg.time.Clock()
        self.controllers = []
        # camera size of screen
        self.camera = Camera(Width, Height)

        # backdrop is black screen
        self.backdrop = pg.Surface((self.width, self.height))
        self.backdrop.fill((0,0,0))

        # TIMING SETUP #
        self.fps = fps
        self.refresh = refresh
        self.next_frame = self.gameClock()
        self.screenRefresh = False
        self.tooSmall = False

        self.fps_font = pg.font.SysFont("Arial", 100)

    # will be used when level loading is created
    def loadGame(self, game):
        self.game = game
        self.game.start()
        self.loadLevel()

    # sets up a level to be displayed
    def loadLevel(self):
        self.camera.mapSize(self.game.currentLevel.mapHeight, self.game.currentLevel.mapWidth)
        self.game.currentLevel.setScreenSize(self.height, self.width)

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

    # can be run to see if there is a game slowdown
    # and where it should be more effiecient
    def runProfiler(self, n):
        for _ in range(n):
            self.dt = self.clock.tick(self.fps) / 1000
            self.doCommands()
            self.update()
            self.updateDisplay()

    def displayFPS(self):
        fps_text = self.fps_font.render(str(int(self.clock.get_fps())), True, (255,0,0))
        self.screen.blit(fps_text, (100,100))

    # updates the game and moves the camera
    def update(self):
        self.game.update(self.dt)

        # move lighting with camera
        self.game.currentLevel.updateLighting(self.camera)
        
        self.camera.update(self.game.currentLevel)

    def clearScreen(self):
        # clear screen with black
        self.screen.blit(self.backdrop, (0,0))
    

    # redraw all sprites to screen
    # quit when necessary
    def updateDisplay(self):
        self.clearScreen()

        # explore dirty sprites
        self.drawAllLayers(self.game.currentLevel.layers)
        
        self.game.currentLevel.draw_weather_effects(self.screen)
        self.game.currentLevel.static_sprites.draw(self.screen)
        self.game.currentLevel.text_layer.draw(self.screen)

        self.displayFPS()

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

    def drawAllLayers(self, layers):
        for layer in layers:
            layer.draw(self.screen, self.camera.camera.topleft)


    def quit(self):
        print("Game Ended")
        pg.quit()
        os._exit(1)
