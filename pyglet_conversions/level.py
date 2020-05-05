import pygame as pg
import pygame.gfxdraw
from textBox import Textbox
from superSpriteGroup import SuperSpriteGroup as sg
import pyglet as pl
# the level class holds the layers of sprites to draw
# it also executes commands of the current controller context


class Level:
    # length of music fadein/out
    _fadeTime_ms = 1000

    def __init__(self, layerNum = 8, name = "NoName"):
        self.tileHeight, self.tileWidth = 0,0
        # filenames
        self.name = name

        #index in game level
        self.index = 0

        # ensure that there is only one of each controller
        self.controllers = set()

        # start bg music
        self.bgMusic = None

        # list of sounds to be played during update
        self.soundBuffer = list()

        # display constants
        self.PC = None
        self.text_box = None


        # initialize all variables and do all the setup for a new game
        self.solid_sprites = dict()
        self.npc_sprites = list() #so you can access individual NPCs
        self.movable_sprites = list()

        self.ray_anchors = dict()
        self.ray_reflect = dict()

        # draw layers
        self.layers = list()
        for order in range(layerNum):
            self.layers.append(sg(order))

        try:
            self.BACKGROUND = self.layers[0] # background image
            self.NPC_LAYER = self.layers[1] # draw NPC next
            self.WALL_LAYER = self.layers[2] # level walls
            self.RAY_LAYER = self.layers[3] # if layer change also change SetPC()
            self.PC_LAYER = self.layers[4] # draw pc
            self.TRIGGER_LAYER = self.layers[5] # level triggers
            self.OVER_LAYER = self.layers[6] # things overhead - bridges/roof
            self.WEATHER_LAYER = self.layers[7] # small alpha effects -- rain, clouds, etc.
            
            self.movable_sprites = self.layers[:7]
        except:
            print("Number of layers must be greater than 7")


    # audio functions
    def backgroundMusic(self, filename):
        self.bgMusic = pg.mixer.Sound(filename)

    # runs through all controllers and controls the PC
    # sends the button presses to the PC
    def doCommands(self, context):
        # get inputs from all controllers
        for controller in self.controllers:
            buttons = controller.getInput()
            for button in buttons:
                self.context.doCommand(button)

    # sets all controller(s)
    def setController(self, controller):
          self.controllers = controller

    def removeControllers(self):
        self.controllers.clear()

    def removeController(self, controller):
        self.controllers.discard(controller)

    # the context is what the camera follows
    def setContext(self, context):
        self.context = context

    def setScreenSize(self, height, width):
        self.screenHeight = height
        self.screenWidth = width
        for layer in self.layers:
            layer.updateDrawingOffset((0, self.screenHeight))

    def setBackground(self, background):
        self.mapHeight = background.image.height
        self.mapWidth = background.image.width
        self.BACKGROUND.add(background)

    def draw_weather_effects(self, screen):
        pass

    # sets playable PC -- @TODO: setup for multiplayer
    def setPC(self, PC, x, y):
        # if PC is presnet then remove from all groups
        if self.PC:
            self.PC.kill()

        # attach PC to level
        self.PC = PC
        self.PC_LAYER.add(self.PC)
        self.setContext(self.PC)

        #eventualy move to tile
        self.PC.moveTo(x, y)

        # attatch rays to all solid sprites
        #self.PC.createRays((self.tileWidth, self.tileHeight), (self.mapWidth, self.mapHeight), self.ray_anchors, self.ray_reflect)
        
        # darken over layer to match negative ray space darkness
        #if self.PC.rays.empty():
         #   self.OVER_LAYER.darken((100,100,100))
        # set to RAY_LAYER
        #self.layers[3] = self.PC.rays


    def updateText(self):
        # Check if any NPCs in range have something to say
        if self.PC.textNotify:

            talkingSprite = self.PC.collideRect(self.PC.interactionBox, self.talking_sprites)
            if talkingSprite:

                # check to see if you're facing the talking sprite
                if self.PC.anySideCollision(talkingSprite.rect):
                    self.text_box.setText(talkingSprite.text)
                    self.text_layer.add(self.text_box)
                    self.animated_sprites.add(self.text_box)
                    self.all_sprites.add(self.text_box)
                    self.setContext(self.text_box)

            self.PC.textNotify = False
            
        if self.text_box.done:
            self.setContext(self.PC)
            self.text_box.done = False

    # executes controller inputs to the current level
    def doCommands(self, controllers):
        for controller in controllers:
            inputs = controller.getInput()
            for button in inputs:
                self.context.commands[button]()

    # signals to level can be read to screen and game from here
    def update(self, dt):
        #self.updateText()
        for layer in self.layers:
            layer.update(dt)

        self.PC.controllerMove(self.solid_sprites.values())
        self.PC.levelTriggerCollision(self.exit_triggers)
        self.updateSound()
        self.animate()

    def updateSound(self):
        self.soundBuffer.clear()
        # go through sprite gorups and call their sound functions
        # add all sounds from a given sprite
        for sprite in self.PC_LAYER:
            self.soundBuffer += sprite.currentSounds

    # Animate all sprites in the animation group
    def animate(self):
        for sprite in self.animated_sprites:
            sprite.animate()

    def updateLighting(self, camera):
        for ray in self.PC.rays:
            ray.rayTraceAll()

    # is the map too small for the screen dimensions? 
    # Needed for smallUpdate()
    def is_small(self, height, width):
        return self.mapWidth < width or self.mapHeight < height