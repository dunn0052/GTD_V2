from superSprite import SuperSprite
from math import sqrt
import pygame as pg
from ray2 import Ray
from rayGroup import RayGroup
from pygame import Vector2 as v2

class PC(SuperSprite):
    # in theory these should be passed from SuperSPrite
    # used for diagonal distance calculations
    __i_sqrt_2 = 1/sqrt(2)

    # directions coordinate the direction frame collections
    __UP = 3
    __DOWN = 0
    __LEFT = 1
    __RIGHT = 2

    # level index because this class is sent
    # through level instances
    level_index = 0

    def __init__(self, image, frames: int, x: int, y: int, \
        speed: int, starting_direction: int, upFrame = 0, \
        downFrame = 0, leftFrame = 0, rightFrame = 0, \
        controllerIndex: int = 0, level_index = 0, buffer = 20):

        #init the super sprite
        super(PC, self).__init__(x, y, image, frames, speed, \
        starting_direction, upFrame, downFrame, leftFrame, rightFrame)

        # Set the controller that owns this PC
        self.controllerIndex = controllerIndex
        self.level_index = level_index

        # the interaction buffer size -- how many px around char rect to consider
        # an "interaction"
        self.buffer = buffer
        # make a rect that is slightly bigger than the sprite rect 
        # so that it can detect if things are close to it
        self.interactionBox = \
            pg.Rect(self.x - self.buffer, \
            self.y - self.buffer, self.rect.width + 2*self.buffer, \
            self.rect.height + 2*self.buffer)

        # Var to let the level know that PC is looking for someone to talk to
        self.textNotify = False

        
        self.rays = None

    def createRays(self, tileSize, mapSize, rayAnchors, solidObjects):
        self.rays = RayGroup(tileSize, mapSize, solidObjects.keys())

        for coord in rayAnchors:
            anchor = rayAnchors[coord]
            for corner in self.find_corners(coord, anchor, solidObjects):
                self.rays.append(Ray(self.rect.center, corner))

    def find_corners(self,coord, anchor, solidObjects):
        r = anchor
        corners = [r.topleft, r.topright, r.bottomright, r.bottomleft]

        '''
        coordinate offsets to R
        0|1|2
        7|R|3
        6|5|4
        '''
        blockOffsets = [ (-1,-1), (0,-1),(1,-1), \
                             (1,0),(1,1),(0,1), \
                             (-1,-1),(-1,0) ]

        #clockwise starting at top center
        surrounding = 0b00000000
        c = coord
        for b in range(len(blockOffsets) -1):
            blockCoordinate = \
            (c[0] + blockOffsets[b][0], c[1] + blockOffsets[b][1])
            
            surrounding |= self.isSolid(blockCoordinate, solidObjects)<<b

        # check if any of the corners are present
        # 0b100000011 0b000001110 0b000111000 0b111000000
        if surrounding & 0b000000001:
            corners.remove(r.topleft)
        if surrounding & 0b000000100:
            corners.remove(r.topright)
        if surrounding & 0b000010000:
            corners.remove(r.bottomright)
        if surrounding & 0b010000000:
            corners.remove(r.bottomleft)
        
        return corners


    def isSolid(self, coord, solidObjects):
        return coord in solidObjects
        
    #---- movement commands ----
    def doDOWN(self):
        #  First dir
        self.changeDirection(self.__DOWN)
        self.vy = self.speed
        self.move_flag_y = True

    def doLEFT(self):
        self.changeDirection(self.__LEFT)
        self.vx = -self.speed
        self.move_flag_x = True

    def doRIGHT(self):
        self.changeDirection(self.__RIGHT)
        self.vx = self.speed
        self.move_flag_x = True

    def doUP(self):
        self.changeDirection(self.__UP)
        self.vy = -self.speed
        self.move_flag_y = True

    def doSELECT(self):
        return self.transition(not self.level_index)

    def doA(self):
        self.openTextBox()

    def doX(self):
        print(self.x, self.y)

    def updateTime(self, dt):
        self.currentSounds.clear()
        self.dt = dt

    # move PC if needed
    def controllerMove(self, group):
        if self.move_flag_x:
            self.movementUpdateX(self.move_flag_y, group)
        if self.move_flag_y:
            self.movementUpdateY(self.move_flag_x, group)
        
        for ray in self.rays:
            ray.move(self.rect.center)

        # reset to starting position
        if not self.vx and not self.vy:
            self.changeImage(self.frame_start[self.direction])
        self.vx, self.vy = 0,0
        self.move_flag_x, self.move_flag_y = False, False

    # change level and move the PC to the defined position
    def levelTriggerCollision(self, group):
        transition = self.collideRect(self.rect, group)
        if transition:
            if transition.index > -1:
                self.x = transition.PC_x
                self.y = transition.PC_y
                self.transition(transition.index)

    
    def anySideCollision(self, rectangle):
        # ugly but quick
        # interaction only when facing npc
        return \
            (self.interactionBox.collidepoint(rectangle.center[0], rectangle.top) and self.direction == self.__DOWN) or \
            (self.interactionBox.collidepoint(rectangle.center[0], rectangle.bottom) and self.direction == self.__UP) or \
            (self.interactionBox.collidepoint(rectangle.left, rectangle.center[1]) and self.direction == self.__RIGHT) or \
            (self.interactionBox.collidepoint(rectangle.right, rectangle.center[1]) and self.direction == self.__LEFT)

    def movementUpdateY(self, diagonal, group):
        y_distance = self.vy * self.dt
        # move sqrt 2 in each direction to offset both x and y velocities
        if diagonal:
            y_distance *= self.__i_sqrt_2
        self.y += y_distance
        self.image.y = self.y
        self.rect.y = self.y
        self.hitbox.y = self.y + self.hitbox.height # hitbox is half our height
        self.interactionBox.y = self.y - self.buffer
        self.collideY(self.collideRect(self.hitbox, group))

    def movementUpdateX(self, diagonal, group):
        x_distance = self.vx * self.dt
        if diagonal:
            x_distance *= self.__i_sqrt_2
        self.x += x_distance
        self.image.x = self.x
        self.rect.x = self.x
        self.hitbox.x = self.x
        self.interactionBox.x = self.x
        self.collideX(self.collideRect(self.hitbox, group))

    # if colliding with something move PC to the edge of it
    def collideX(self, ent):
        if not ent:
            return None
        if self.vx > 0:
            self.x = ent.rect.left - self.hitbox.width
        if self.vx < 0:
            self.x = ent.rect.right
        self.image.x = self.x
        self.rect.x = self.x
        self.interactionBox.x = self.x - self.buffer
        self.hitbox.x = self.x

        #ent.playSound("bump")




    def collideY(self, ent):
        if not ent:
            return None
        if self.vy > 0:
            self.y = ent.rect.top - self.rect.height
        if self.vy < 0:
            self.y = ent.rect.bottom - self.hitbox.height
        self.image.y = self.y
        self.rect.y = self.y
        self.interactionBox.y = self.y - self.buffer
        self.hitbox.y = self.y + self.hitbox.height

        #ent.playSound("bump")

    # level is set by the index of the PC on every frame
    # somehow faster than an if statement check
    def transition(self, levelNum):
        self.level_index = levelNum

    # request to open dialog with the nearest NPC
    def openTextBox(self):
        self.textNotify = True


    # updates directional frame index if enough time has elapsed
    def animate(self):
        if self.animation_timer < self.animation_time_until_next:
            self.animation_timer += self.dt
        else:
            self.current_frame = (self.current_frame+1)%self.animation_cycles[self.direction]              # Loop on end
            self.animation_timer = 0
