import pygame as pg
import pyglet as pl 


bg = pl.image.load('images/out.png')

class Screen:

    def __init__(self, Height = 1280, Width = 1920, fps = 120, refresh = 10, Title = "Cat Mystery Dungeon"):
        pg.init()
        self.width = Width
        self.height = Height


        self.controllers = []

        self.screen = pl.window.Window(width=self.width, height=self.height,visible=True)

        self.on_draw = self.screen.event(self.on_draw)


    def on_draw(self):
        self.screen.clear()

    def run(self):
        pl.app.run()


s = Screen()

s.run()