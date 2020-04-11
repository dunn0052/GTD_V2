
# This class is a container for sending
# messages from sprites to the level
class SpriteMessage:

    def __init__(self):
        self.levelRequest = None

    def requestLevel(self, levelNum):
        self.levelRequest = levelNum

    def notify(self):
        return self