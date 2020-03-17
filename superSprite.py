import pygame, math, sys, os
vec = pygame.math.Vector2

import keyboardInput as KB

'''
This class is the base class for all game sprites
it has basic functions needed for sprites
There are virtual functions that can be used
for interaction with buttons
'''

class SuperSprite(pygame.sprite.Sprite):
    def __init__(self, image = None, frames=1):
      pygame.init()
      pygame.sprite.Sprite.__init__(self)
      
      # need a list because the images are ordered
      self.images = []
      self.x, self.y = 0, 0
      
      # could put file name or already loaded pygame image
      if type(image) == str:
          img = self.loadImage(image)
      else:
          img = image.convert_alpha()
      
      # frames should at least be a factor of the total
      # image width, if not a multiple of 4 for each direction
      self.frameWidth = img.get_width() // frames
      self.frameHeight = img.get_height()
      
      # slice the frames
      self.images = self.createFrames(frames, img)
      # self.image is what is drawn
      self.image = pygame.Surface.copy(self.images[0])

      # set starting image
      self.currentImage = 0
      self.rect = self.image.get_rect()

      self.mask = pygame.mask.from_surface(self.image)
      self.angle = 0
      self.scale = 1

      # iteration counter
      self.subFrame = 0     
      # how many iterations before moving to next frame
      self.frameCap = 10

      # commands
      self.commands = {KB.A:self.doA,KB.B:self.doB,KB.X:self.doX,KB.Y:self.doY,KB.DOWN:self.doDOWN, \
                                  KB.UP:self.doUP,KB.LEFT:self.doLEFT,KB.RIGHT:self.doRIGHT,KB.L:self.doL, \
                                  KB.R:self.doR,KB.START:self.doSTART, KB.SELECT:self.doSELECT}

# probably should delete, but could be useful?
    def parseColour(self,colour):
      if type(colour) == str:
          # check to see if valid colour
          return pygame.Color(colour)
      else:
          colourRGB = pygame.Color("white")
          colourRGB.r = colour[0]
          colourRGB.g = colour[1]
          colourRGB.b = colour[2]
          return colourRGB

#----- IMAGE FUNCTIONS -----#

    # load an image from a file path
    def loadImage(self,fileName: str):
      if os.path.isfile(fileName):
          image = pygame.image.load(fileName)
          image = image.convert_alpha()
          # Return the image
          return image
      else:
          raise Exception("Error loading image: " + fileName + " - Check filename and path?")

    # split image into individual frames
    # @frames: number of equally sized animation frames
    # @img: full image of all frames to be spliced into frames
    def createFrames(self, frames: int, img):
        imageList = []
        frameSurf = pygame.Surface((self.frameWidth, self.frameHeight), pygame.SRCALPHA, 32)

        for frame in range(0, -img.get_width(), -self.frameWidth):
            frameSurf = pygame.Surface((self.frameWidth, self.frameHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (frame, 0))
            imageList.append(frameSurf.copy())
        return imageList

    def addImage(self, filename: str):
      self.images.append(self.loadImage(filename))

    # set image to specific frame
    def changeImage(self, index: int):
      self.currentImage = index
      if self.angle == 0 and self.scale == 1:
          self.image = self.images[index]
      else:
          self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
      oldcenter = self.rect.center
      self.rect = self.image.get_rect()
      originalRect = self.images[self.currentImage].get_rect()
      self.frameWidth = originalRect.width
      self.frameHeight = originalRect.height
      self.rect.center = oldcenter
      self.mask = pygame.mask.from_surface(self.image)

    def nextFrame(self):
        self.currentImage += 1
        self.currentImage %= len(self.images)
        self.changeImage(self.currentImage)

    # in case you want to animate backwards?
    def prevFrame(self):
        self.currentImage -= 1
        self.currentImage %= len(self.images)
        self.changeImage(self.currentImage)

    # flip, skew, bop it! 
    # For real, this does all the work of rotating or changing sizes
    # and dealing with the rect
    def transform(self, angle = 0, scale = 1, hflip=False, vflip=False):
        oldmiddle = self.rect.center
        if hflip or vflip:
            tempImage = pygame.transform.flip(self.images[self.currentImage], hflip, vflip)
        else:
            tempImage = self.images[self.currentImage]
        if angle != 0 or scale != 1:
            self.angle = angle
            self.scale = scale
            tempImage = pygame.transform.rotozoom(tempImage, -angle, scale)
        self.image = tempImage
        self.rect = self.image.get_rect()
        self.rect.center = oldmiddle
        self.mask = pygame.mask.from_surface(self.image)

# ---- MOVEMENT FUNCTIONS ------
# move from current position x, y distance
    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        self.rect.x = self.x
        self.rect.y = self.y

# move to coordinates
    def moveTo(self, x, y):
        self.rect.x, self.x = x, x
        self.rect.y, self.y = y, y

# ------ COLLISION FUNCTIONS ------
    def touching(self, other):
        collided = pygame.sprite.collide_mask(self , other)
        return collided

    # Fun, but just notifies if any sprite in some group
    # is colliding
    def groupTouching(self, group):
        for sprite in group:
            if self.touching(sprite):
                return sprite

    # are the centers touching? Way faster if you can do this
    # instead of the mask collide.
    def checkCollision(self, other, center = False):
        if center:
            return self.rect.collidepoint(other.rect.center)
        return self.rect.colliderect(other)

# ------ BUTTON FUNCTIONS ------

    # A button input calls the command dictionary
    # and executes the command
    def doCommand(self, button):
        self.commands[button]()

# virtual functions to be difined by sub classes

    def doA(self):
        pass
    def doB(self):
        pass
    def doX(self):
        pass
    def doY(self):
        pass
    def doLEFT(self):
        pass
    def doRIGHT(self):
        pass
    def doUP(self):
        pass
    def doDOWN(self):
        pass
    def doL(self):
        pass
    def doR(self):
        pass
    def doSTART(self):
        pass
    def doSELECT(self):
        pass

    # virtual function to do
    # whatever the sprite needs
    # to do to animate
    def animate(self, dt):
        pass

    # take in a time delta to
    # use in calculating the real
    # time changes between game loops
    def update(self, dt = 0):
        self.dt = dt

# ------ LOADING FUNCTIONS ------
    # calls the packed lambda functions
    # that are needed to set a
    # superSprite up when loaded
    def unpackSprite(self):
        pass

# cheap shot to use level parameters - probably out of scope
    def setLevel(self, level):
        self.level = level
