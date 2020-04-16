import pygame as pg
from textBox import Textbox
# the level class holds the layers of sprites to draw
# it also executes commands of the current controller context


class Level:
    def __init__(self, layerNum = 7, name = "NoName"):
        self.tileHeight, self.tileWidth = 0,0
        # filenames
        self.name = name

        #index in game level
        self.index = 0

        # ensure that there is only one of each controller
        self.controllers = set()

        self.PC = None
        self.text_box = None
        self.darkness = pg.Surface((0,0))

        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.solid_sprites = dict()
        self.exit_triggers = pg.sprite.LayeredUpdates()
        self.animated_sprites = pg.sprite.Group()
        self.static_sprites = pg.sprite.OrderedUpdates() # maybe layeredUpdates?
        self.text_layer = pg.sprite.Group() # need more than 1 textbox?
        self.npc_sprites = [] #so you can access individual NPCs
        self.enemy_sprites = pg.sprite.Group()
        self.talking_sprites = pg.sprite.Group()

        # draw layers
        self.layers = []
        for _ in range(layerNum):
            self.layers.append(pg.sprite.LayeredUpdates())
        try:
            self.BACKGROUND = self.layers[0] # background image
            self.WALL_LAYER = self.layers[1] # level walls
            self.NPC_LAYER = self.layers[2] # draw NPC next
            self.TRIGGER_LAYER = self.layers[3] # level triggers
            self.PC_LAYER = self.layers[4] # draw pc
            self.OVER_LAYER = self.layers[5] # things overhead - bridges/roof
            self.WEATHER_LAYER = self.layers[6] # small alpha effects -- rain, clouds, etc.
        except:
            print("Number of layers must be greater than 7")

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

    def setBackground(self, background):
        self.mapHeight = background.image.get_height()
        self.mapWidth = background.image.get_width()
        self.BACKGROUND.add(background)

    def draw_weather_effects(self, screen):
        screen.blit(self.darkness, (0,0))

    # sets playable PC -- @TODO: setup for multiplayer
    def setPC(self, PC, x, y):
        # if PC is presnet then remove from all groups
        if self.PC:
            self.PC.kill()

        self.PC = PC
        self.PC_LAYER.add(self.PC)
        self.all_sprites.add(self.PC)
        self.animated_sprites.add(self.PC)
        self.setContext(self.PC)

        #eventualy move to tile
        self.PC.moveTo(x, y)

        # attatch rays to all solid sprites
        self.PC.createRays(self.solid_sprites.values())


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
        self.updateText()
        self.all_sprites.update(dt)
        self.PC.controllerMove(self.solid_sprites.values())
        self.PC.levelTriggerCollision(self.exit_triggers)
        self.animate()
        
    # Animate all sprites in the animation group
    def animate(self):
        for sprite in self.animated_sprites:
            sprite.animate()

    def updateLighting(self, camera):
        for ray in self.PC.rays:

            #ray.raytrace(self.solid_sprites, self.tileHeight, self.tileWidth)
            ray.rayTrace(self.tileHeight, self.tileWidth, self.solid_sprites)
            ray.update(camera.camera.topleft)
                

    # is the map too small for the screen dimensions? 
    # Needed for smallUpdate()
    def is_small(self, height, width):
        return self.mapWidth < width or self.mapHeight < height