from superSprite import SuperSprite
from math import sqrt

UP = 3
DOWN = 0
LEFT = 1
RIGHT = 2

class PC(SuperSprite):
    
    __level_index = 0
    __sqrt_2 = sqr(2)

    def __init__(self, image, frames: int, x: int, y: int, speed: int, starting_direction: int):

        #init the super sprite
        super(PC, self).__init__(image, frames)

        # velocity in each direction
        self.vx, self.vy = 0, 0
        self.x, self.y = x, y

        self.speed = speed
        self.direction = starting_direction
        self.move_flag = False
        # number of animations must be the same for each direction
        self.animation_cycle = frames//4
        self.current_frame = 0
        self.frame_speed = 1
        
        self.frame_cap = 12
        self.sub_frame = 0
    

    def changeDirection(self, direction: int):
        self.direction = direction
        self.changeImage(self.direction*self.animation_cycle + self.current_frame)

    #---- movement commands ----
    def doDOWN(self):
        #  First dir
        self.changeDirection(DOWN)
        self.vy = self.speed
        self.move_flag = True

    def doLEFT(self):
        self.changeDirection(LEFT)
        self.vx = -self.speed
        self.move_flag = True

    def doRIGHT(self):
        self.changeDirection(RIGHT)
        self.vx = self.speed
        self.move_flag = True

    def doUP(self):
        self.changeDirection(UP)
        self.vy = -self.speed
        self.move_flag = True

    def update(self, dt):
        self.dt = dt
        if self.move_flag:
            self.movementUpdate()

    def doLEFT(self):
        return self.exit()

    def movementUpdate(self):
        x_distance, y_distance = self.vx * self.dt, self.vy * self.dt
        # get signed square root of each
        if(x_distance and y_distance):
            x_distance *= self.__sqrt_2
            y_distance *= self.__sqrt_2

        self.move(x_distance, y_distance)        
        '''
        self.levelTrigger()
        self.rect.x = self.x
        self.hitbox.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.hitbox.y = self.y + self.hitbox.height
        self.collide_with_walls('y')
        '''
        # reset to starting position
        if not self.vx and not self.vy:
            self.changeImage(self.direction * self.animation_cycle)
        self.vx, self.vy = 0,0

    def animate(self):
        if self.sub_frame < self.frame_cap:
            # 10ms is max animation speed
            self.sub_frame += self.frame_speed
        else:
            self.current_frame = (self.current_frame+1)%self.animation_cycle              # Loop on end
            self.sub_frame = 0

    def exit(self):
        return self.__level_index
