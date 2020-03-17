import pygame
from keyboardInput import KEYDICT as k 
import keyboardInput as KB
from enum import Enum
# globals
POS = 0.9
NEG = -1.0
NUM_BUTTONS = 10
NUM_AXIS = 2
class ButtonTypes(Enum):
    SINGLE = 0
    HOLD = 1

class Controller:

    # sub class for button map
    # and determines if you can hold it or not
    class Button:
        def __init__(self, button, mode = ButtonTypes.SINGLE):
            self.button = button
            self.mode = mode

        def getButton(self):  
            return self.button
            
    # number = controller number
    def __init__(self, index, keyboard = False):

        self.index = index

        # fast access mapping from input to enum
        if keyboard:
            self.buttonMap =   {k["x"]:self.Button(KB.X, ButtonTypes.SINGLE), k["a"]:self.Button(KB.A, ButtonTypes.SINGLE), \
                                k["b"]:self.Button(KB.B, ButtonTypes.SINGLE), k["y"]:self.Button(KB.Y, ButtonTypes.SINGLE), \
                                k["q"]:self.Button(KB.L, ButtonTypes.SINGLE), k["e"]:self.Button(KB.R, ButtonTypes.SINGLE), \
                                k["h"]:self.Button(KB.START, ButtonTypes.SINGLE), k["g"]:self.Button(KB.SELECT, ButtonTypes.SINGLE), \
                                k["up"]:self.Button(KB.UP, ButtonTypes.HOLD), k["down"]:self.Button(KB.DOWN, ButtonTypes.HOLD), \
                                k["left"]:self.Button(KB.LEFT, ButtonTypes.HOLD), k["right"]:self.Button(KB.RIGHT, ButtonTypes.HOLD)}
        else:
            self.buttonMap =   {0:self.Button(KB.X, ButtonTypes.SINGLE), 1:self.Button(KB.A, ButtonTypes.SINGLE), \
                                2:self.Button(KB.B, ButtonTypes.SINGLE), 3:self.Button(KB.Y, ButtonTypes.SINGLE), \
                                4:self.Button(KB.L, ButtonTypes.SINGLE), 5:self.Button(KB.R, ButtonTypes.SINGLE), \
                                8:self.Button(KB.SELECT, ButtonTypes.SINGLE), 9:self.Button(KB.START, ButtonTypes.SINGLE), \
                                "UP":self.Button(KB.UP, ButtonTypes.HOLD), "DOWN":self.Button(KB.DOWN, ButtonTypes.HOLD), \
                                "LEFT":self.Button(KB.LEFT, ButtonTypes.HOLD), "RIGHT":self.Button(KB.RIGHT, ButtonTypes.HOLD)}
        self.previousInputs = set()


        # access joystick number
        try:
            #init joystick
            pygame.init()
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(index)
            self.joystick.init()
        except:
            print("No controller detected!")
            keyboard = True
        # hiding the input function if a keyboard is used
        # or a controller is not connected for it
        if keyboard:
            self.getInput = self.getKeys



    # get controller input
    def getInput(self):
        inputs = set()

        pygame.event.get()
        # axis control
        # the threshold must be tested
        # to determine if it was actually pressed
        for i in range( NUM_AXIS ):
            axis = self.joystick.get_axis(i)
            if axis >= POS or axis == NEG:
                if axis > 0 and not i :
                    inputs.add(self.buttonMap["RIGHT"])
                if axis < 0 and not i:
                    inputs.add(self.buttonMap["LEFT"])
                if axis > 0 and i :
                    inputs.add(self.buttonMap["DOWN"])
                if axis < 0 and i :
                    inputs.add(self.buttonMap["UP"])

        # Haha oh boy, this just takes whatever was input and maps it to output pygame button commands
        inputs = inputs.union(set(map((lambda i: self.buttonMap[i]) , filter( (lambda i: self.joystick.get_button(i)), range(NUM_BUTTONS)))))

        # find all the new inputs
        newButtons = inputs.difference(self.previousInputs)
        self.previousInputs.clear()

        # set previous if single button key was pressed
        self.previousInputs = set(filter( lambda inp: ButtonTypes.SINGLE == inp.mode, inputs))
        
        # return all button enums
        return set( map( (lambda button: button.button), newButtons ))

    # input for keyboard instead @TODO get this to actually work again
    def getKeys(self):
        return None
        inputs = set()

        pygame.event.clear()
        keys = pygame.key.get_pressed()
        # keys pressed --> buttons
        if sum(keys):
            map( (lambda key: inputs.add(self.buttonMap[key]) if keys[key] else None), self.buttonMap )

        # find all the new inputs
        newButtons = inputs.difference(self.previousInputs)
        self.previousInputs.clear()

        #create new previous buttons
        self.previousInputs = set(filter( lambda inp: ButtonTypes.SINGLE == inp.mode, inputs))

        #return all button enums
        return set( map( (lambda button: button.button), newButtons ))
