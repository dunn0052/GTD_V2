import pygame as pg

class Audio:
    # sound type event enums
    # also alias for channel number
    MUSIC1 = 0
    MUSIC2 = 1
    EFFECT = 2


    def __init__(self):
        pg.mixer.init()
        # reserve music channel
        pg.mixer.set_reserved(self.MUSIC1)
        pg.mixer.set_reserved(self.MUSIC2)
        pg.mixer.Channel(self.MUSIC1).set_volume(0.3)
        pg.mixer.Channel(self.MUSIC2).set_volume(0.3)
        self.bgMusicChannel = self.MUSIC1
        self.soundBuffer = list()

    # stop all audio
    def end(self):
        pg.mixer.stop()

    # start all audio
    def pause(self):
        pg.mixer.pause()

    def unpause(self):
        pg.mixer.unpause()

    # used in update
    def setSoundBuffer(self, soundBuffer):
        self.soundBuffer = soundBuffer

    # play all sounds in soundBuffer stream
    # check first available channel
    def play(self):
        for sound in self.soundBuffer:
            if not pg.mixer.Channel(self.EFFECT).get_busy():
                pg.mixer.Channel(self.EFFECT).play(sound)
            #sound.play()
    def playMusic(self, bgMusic):
        # if bg music is playing, fade out and play new music
        if pg.mixer.Channel(self.bgMusicChannel).get_busy():
            pg.mixer.Channel(self.bgMusicChannel).fadeout(1000)

        self.bgMusicChannel = not self.bgMusicChannel #toggle between music1 and music2
        if bgMusic:
            pg.mixer.Channel(self.bgMusicChannel).play(bgMusic, loops = -1)
        