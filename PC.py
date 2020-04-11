from superSprite import SuperSprite
from spriteMessage import SpriteMessage
from math import sqrt
import pygame as pg

class PC(SuperSprite):
    
    # level index because this class is sent
    # through level instances
    level_index = 0


    # used for diagonal distance calculations
    __sqrt_2 = sqrt(2)

        # directions coordinate the direction frame collections
    __UP = 3
    __DOWN = 0
    __LEFT = 1
    __RIGHT = 2

    def __init__(self, image, frames: int, x: int, y: int, \
        speed: int, starting_direction: int, upFrame = 0, \
        downFrame = 0, leftFrame = 0, rightFrame = 0, \
        controllerIndex: int = 0, level_index = 0, buffer = 20):

        #init the super sprite
        super(PC, self).__init__(x, y, image, frames)

        # velocity in each direction
        self.vx, self.vy = 0, 0

        self.speed = speed
        self.direction = starting_direction
        self.animation_cycles = [downFrame, leftFrame, rightFrame, upFrame]
        if not any(self.animation_cycles):
            self.animation_cycles = [frames//4]*4

        # pre calculate animation direction starts
        self.frame_start = {self.__UP:self.animation_start(self.__UP),\
                            self.__DOWN:self.animation_start(self.__DOWN),\
                            self.__LEFT:self.animation_start(self.__LEFT),\
                            self.__RIGHT:self.animation_start(self.__RIGHT)}
        
        self.move_flag_y = False
        self.move_flag_x = False
        # number of animations must be the same for each direction

        self.controllerIndex = controllerIndex
        self.level_index = level_index

        self.buffer = buffer
        # make a rect that is slightly bigger than the sprite rect 
        # so that it can detect if things are close to it
        self.interactionBox = \
            pg.Rect(self.x - self.buffer, \
            self.y - self.buffer, self.rect.width + 2*self.buffer, \
            self.rect.height + 2*self.buffer)

        self.textNotify = False

    def animation_start(self, dir):
        return sum(self.animation_cycles[:dir])

    def changeDirection(self, direction: int):
        self.direction = direction
        self.changeImage(self.frame_start[self.direction] + self.current_frame%self.animation_cycles[self.direction])

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

    def update(self, dt):
        self.dt = dt

    def controllerMove(self, group):
        if self.move_flag_x:
            self.movementUpdateX(self.move_flag_y, group)
        if self.move_flag_y:
            self.movementUpdateY(self.move_flag_x, group)

        # reset to starting position
        if not self.vx and not self.vy:
            self.changeImage(self.frame_start[self.direction])
        self.vx, self.vy = 0,0
        self.move_flag_x, self.move_flag_y = False, False

    def levelTriggerCollision(self, group):
        transition = self.collideRect(self.hitbox, group)
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
        if diagonal:
            y_distance *= 0.7071
        self.y += y_distance
        self.rect.y = self.y
        self.hitbox.y = self.y + self.hitbox.height # hitbox is half our height
        self.interactionBox.y = self.y - self.buffer
        self.collideY(self.collideRect(self.hitbox, group))
        #self.collideY(self.groupTouching(group))

    def movementUpdateX(self, diagonal, group):
        x_distance = self.vx * self.dt
        if diagonal:
            x_distance *= 0.7071
        self.x += x_distance
        self.rect.x = self.x
        self.hitbox.x = self.x
        self.interactionBox.x = self.x
        self.collideX(self.collideRect(self.hitbox, group))
        #self.collideX(self.groupTouching(group))

    def collideX(self, ent):
        if not ent:
            return None
        if self.vx > 0:
            self.x = ent.rect.left - self.hitbox.width
        if self.vx < 0:
            self.x = ent.rect.right
        self.rect.x = self.x
        self.interactionBox.x = self.x - self.buffer
        self.hitbox.x = self.x


    def collideY(self, ent):
        if not ent:
            return None
        if self.vy > 0:
            self.y = ent.rect.top - self.rect.height
        if self.vy < 0:
            self.y = ent.rect.bottom - self.hitbox.height
        self.rect.y = self.y
        self.interactionBox.y = self.y - self.buffer
        self.hitbox.y = self.y + self.hitbox.height


    def transition(self, levelNum):
        self.level_index = levelNum

    def openTextBox(self):
        self.textNotify = True

    def animate(self):
        if self.animation_timer < self.animation_time_until_next:
            # 10ms is max animation speed
            self.animation_timer += self.dt
        else:
            self.current_frame = (self.current_frame+1)%self.animation_cycles[self.direction]              # Loop on end
            self.animation_timer = 0
