from superSprite import SuperSprite
import pygame as pg

class Textbox(SuperSprite):
    def __init__(self, backgroundImage, font = 'Arial', fontsize = 64, fontColor = 'black', offset = 20):
        # set up background
        self.offset = offset
        super().__init__(backgroundImage, 1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.textRectPlacement = pg.rect.Rect(self.rect.left - self.offset, self.rect.top - self.offset, self.rect.width - 2*self.offset, self.rect.height - 2*self.offset)
        self.textRect = pg.Surface(self.textRectPlacement)
        self.textRect.fill((255,0,0))

        self.originalImage = self.image.copy()

        # index of word blits
        self.font = pg.font.SysFont(font, fontsize)
        self.fontColor = pg.Color(fontColor)

        # text splitting and iters
        self.text = "a"
        self.reset()
        self.space = self.font.size(' ')[0]  # The width of a space.

        self.done = False # notify when ending

    def setText(self, text):
        self.text = text
        self.words = iter([word.split(' ') for word in self.text.splitlines()])  # 2D array where each row is a list of words.
        self.line = iter(next(self.words)) # get first line as iter
        self.nextWord()


    def update(self, dt):
        if self.next:
            self.blitLetter()
        else:
            pass

    def nextWord(self):
        try:
            self.word = next(self.line)
            self.wordLength = len(self.word)
            self.letterIndex = 0
            self.wordSurface = self.font.render(self.word, 0, self.fontColor)
            self.word_width, self.word_height = self.wordSurface.get_size()
            # if word length goes past the length of the text box
            if self.textX + self.word_width >= self.rect.width - self.offset:
                self.lineBreak()

        except StopIteration:
            # if no more words then get next line
            self.nextLine()

    #TODO: definitely get rid the try/exception
    def nextLine(self):
        try:
            # get next line
            self.line = iter(next(self.words))
            # go to next line
            self.lineBreak()
            self.nextWord()
            if self.textY + self.word_height + self.offset >= self.rect.height:
                self.clearScreen()
        except StopIteration:
            self.end = True
            self.next = False


    def blitLetter(self):
        word_surface = self.font.render(self.word[:self.letterIndex], 0, self.fontColor)
        self.image.blit(self.textRect, (0,0))
        self.image.blit(word_surface, (self.textX, self.textY))
        if self.letterIndex < self.wordLength:
            self.letterIndex += 1
        else:
            self.textX += self.word_width + self.space
            self.nextWord = True

    def blitWord(self):
        while not self.nextWord:
            self.blitLetter()
        self.nextWord = False
        self.wordEnd = True

    def blitAll(self):
        while self.next:
            self.blitWord()

    def lineBreak(self):
        self.textX = self.originalX
        self.textY += self.word_height

    def clearScreen(self):
        self.next = True
        self.textX = self.originalX
        self.textY = self.originalY
        self.image.blit(self.textRect, (0,0))

    def nextScreen(self):
        if not self.next:
            self.clearScreen()
        if self.end:
            self.reset()
            self.kill()
            self.done = True

    def reset(self):
        self.originalX = self.rect.x + self.offset
        self.originalY = self.rect.y + self.offset
        self.textX = self.originalX
        self.textY = self.originalY
        self.next = True
        self.end = False
        self.setText(self.text)

    def doA(self):
        if not self.next:
            self.nextScreen()
        else:
            self.blitAll()
