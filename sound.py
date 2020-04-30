from pygame import pygame.mixer

class Sound:
    def __init__(self):
        pygame.mixer.init()


    def end(self):
        pygame.mixer.stop()

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

    def loadSound(self, filename):
        self.sound = pygame.mixer.Sound(filename)

    def play(self):
        self.sound.play()