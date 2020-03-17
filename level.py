import pygame as pg
#from textBox import Textbox
# the level class holds the layers of sprites to draw
# it also executes commands of the current controller context


class Level:
    def __init__(self, layerNum = 7, name = "NoName"):
        self.tileHeight, self.tileWidth = 0,0
        # filenames
        self.name = name

        # ensure that there is only one of each controller
        self.controllers = set()

        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.solid_sprites = pg.sprite.Group()
        self.animated_sprites = pg.sprite.Group()
        self.static_sprites = pg.sprite.OrderedUpdates() # maybe layeredUpdates?
        self.text_layer = pg.sprite.GroupSingle()
        self.npc_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
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
                self.PC.doCommand(button)

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

    def setBackground(self, background):
        self.mapHeight = background.image.get_height()
        self.mapWidth = background.image.get_width()
        self.BACKGROUND.add(background)

    # sets playable PC -- @TODO: setup for multiplayer
    def setPC(self, PC, x, y):
        self.PC = PC
        self.PC_LAYER.add(self.PC)
        self.all_sprites.add(self.PC)
        self.animated_sprites.add(self.PC)
        self.setContext(self.PC)

        #eventualy move to tile
        self.PC.moveTo(x, y)

    # signals to level can be read to screen and game from here
    def update(self, dt):
        self.all_sprites.update(dt)
        for sprite in self.animated_sprites:
            sprite.animate()
        
    # Animate all sprites in the animation group
    def animate(self):
        for sprite in self.animated_sprites:
            sprite.animate()

    # is the map too small for the screen dimensions? 
    # Needed for smallUpdate()
    def is_small(self, height, width):
        return self.mapWidth < width or self.mapHeight < height
'''
    def setPC(self, PC, x, y):
        self.PC = PC
        self.PC.level = self
        self.PC_LAYER.add(self.PC)
        self.all_sprites.add(self.PC)
        self.animated_sprites.add(self.PC)
        self.PC.moveToTile(x, y)
        self.setControllerContext(self.PC)
        if self.PC.weapon:
            self.PC.weapon.kill()
            self.PC.weapon.level = self.PC.level

    def displayText(self, text):
        self.text = Textbox(text = text, backgroundImage = "images//textBackground.png", offset = 65, level = self)
        self.all_sprites.add(self.text)
        self.text_layer.add(self.text)
        self.setControllerContext(self.text)

# make fade surface on static layer
    def screenFade(self):
        self.setControllerContext(self.off)
        fade = pg.Surface((self.currentLevel.width, self.currentLevel.height))
        fade.fill((0,0,0))
        for alpha in range(0, 100, 2):
            fade.set_alpha(alpha)
            pg.display.flip()
            pg.time.delay(10)


    def initLevel(self, levelPath):
        self.levelBuffer = loadObject(levelPath)
        self.level = self.levelBuffer.unpackLevel()
        self.level.setController(self.controllers[0])
        self.camera.mapSize(self.level.background.originalHeight, self.level.background.originalWidth)
        if self.level.background.originalWidth < self.width or self.level.background.originalHeight < self.height:
            self.updateDisplay = self.updateDisplaySmall
        else:
            self.updateDisplay = self.updateDisplay
'''