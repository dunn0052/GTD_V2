import pygame
from enum import Enum
from pyglet.window import key
import keyboardInput as KB


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

        self.keyboard = keyboard
        self.pressedButtons = set()

        # access joystick number
        try:
            #init joystick
            pygame.init()
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(index)
            self.joystick.init()
        except:
            print("No controller detected!")
            self.keyboard = True

        # fast access mapping from input to enum
        if self.keyboard:

            self.buttonMap =   {key.X:self.Button(KB.X, ButtonTypes.SINGLE), key.A:self.Button(KB.A, ButtonTypes.SINGLE), \
                                key.B:self.Button(KB.B, ButtonTypes.SINGLE), key.Y:self.Button(KB.Y, ButtonTypes.SINGLE), \
                                key.Q:self.Button(KB.L, ButtonTypes.SINGLE), key.E:self.Button(KB.R, ButtonTypes.SINGLE), \
                                key.H:self.Button(KB.START, ButtonTypes.SINGLE), key.G:self.Button(KB.SELECT, ButtonTypes.SINGLE), \
                                key.UP:self.Button(KB.UP, ButtonTypes.HOLD), key.DOWN:self.Button(KB.DOWN, ButtonTypes.HOLD), \
                                key.LEFT:self.Button(KB.LEFT, ButtonTypes.HOLD), key.RIGHT:self.Button(KB.RIGHT, ButtonTypes.HOLD)}

            self.keys = key.KeyStateHandler()
            # hiding the input function if a keyboard is used
            # or a controller is not connected for it
            self.getInput = self.getKeys

        else:
            self.buttonMap =   {0:self.Button(KB.X, ButtonTypes.SINGLE), 1:self.Button(KB.A, ButtonTypes.SINGLE), \
                                2:self.Button(KB.B, ButtonTypes.SINGLE), 3:self.Button(KB.Y, ButtonTypes.SINGLE), \
                                4:self.Button(KB.L, ButtonTypes.SINGLE), 5:self.Button(KB.R, ButtonTypes.SINGLE), \
                                8:self.Button(KB.SELECT, ButtonTypes.SINGLE), 9:self.Button(KB.START, ButtonTypes.SINGLE), \
                                "UP":self.Button(KB.UP, ButtonTypes.HOLD), "DOWN":self.Button(KB.DOWN, ButtonTypes.HOLD), \
                                "LEFT":self.Button(KB.LEFT, ButtonTypes.HOLD), "RIGHT":self.Button(KB.RIGHT, ButtonTypes.HOLD)}

        self.inputs = set()
        self.previousInputs = set()


    # must be sent to pl window
    def getKeyboardHandler(self):
        return self.keys


    # get controller input
    def getInput(self):
        inputs = set()

        # axis control
        # the threshold must be tested
        # to determine if it was actually pressed
        # In theory this should work? I think my controller is broken
        for i in range( NUM_AXIS ):
            axis = self.joystick.get_axis(i)
            if axis >= POS or axis == NEG:
                if axis > 0 and i == 0:
                    inputs.add(self.buttonMap["RIGHT"])
                if axis < 0 and i == 0:
                    inputs.add(self.buttonMap["LEFT"])
                if axis > 0 and i  == 1:
                    inputs.add(self.buttonMap["DOWN"])
                if axis < 0 and i == 1:
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

    def getKeys(self):
        self.inputs.clear()
        self.pressedButtons.clear()

        # keys pressed --> buttons
        for key in self.buttonMap.keys():
            if self.keys[key]:
                self.inputs.add(self.buttonMap[key])
                
        # find all the new inputs
        newButtons = self.inputs.difference(self.previousInputs)
        self.previousInputs.clear()

        #create new previous buttons
        self.previousInputs = set(filter( lambda inp: ButtonTypes.SINGLE == inp.mode, self.inputs))

        #return all button enums
        self.pressedButtons = set( map( (lambda button: button.button), newButtons ))
