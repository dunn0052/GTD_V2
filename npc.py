from superSprite import SuperSprite

class NPC(SuperSprite):

    def __init__(self, image, frames: int, x: int, y: int, \
        speed: int, starting_direction: int):

        super().__init__(x, y, image, frames)
        self.text = ""

    def setText(self, text: str):
        self.text = text

    def interact(self):
        pass
