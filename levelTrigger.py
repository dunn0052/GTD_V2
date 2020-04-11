from trigger import Trigger

class LevelTransition(Trigger):

    def setLevel(self, index = -1, x = 0, y = 0, dir = 0):
        self.index = index
        self.PC_x, self.PC_y = x, y
        self.PC_dir = dir        
