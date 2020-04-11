from superSprite import SuperSprite
import pygame as pg

class TextBox(SuperSprite):

    def __init__(self, bgImg, offset = 20, endOffset = 80, font = 'Arial', \
        fontsize = 64, fontColor = 'black'):

        # should probably have actual coordinates
        super().__init__(0, 0, bgImg, 1)
        self.originalImage = self.loadImage(bgImg)
        self.borderOffset = offset
        self.endBorder = endOffset
        self.font = font
        self.fontColor = pg.Color(fontColor)
        self.font = pg.font.SysFont(font, fontsize)

        self.text = "default"
        self.spaceWidth, self.word_height = self.font.size(' ')
        self.current_word_width = 0
        self.current_word_surface = None
        self.done = False #notify when ending
        self.screenFull = False

        self.animation_timer = 0
        self.animation_time_until_next = 0.03

        self.borderOffset = offset
        self.textX, self.textY = self.borderOffset, self.borderOffset
        self.originalX = self.textX
        self.originalY = self.textY
        self.letterIndex = 0
        self.wordIndex = 0
        self.lineIndex = 0

        self.player_is_patient = True
        self.textDone = False

    def setText(self, text):
        self.text = text
        self.lines = [line.split(' ') for line in self.text.splitlines()]
        self.maxLineIndex = len(self.lines)
        self.currentLine = self.lines[0] # get first line
        self.currentWord = self.currentLine[0]

    def reset(self):
        self.clearScreen()
        self.setText(self.text)
        self.letterIndex = 0
        self.wordIndex = 0
        self.lineIndex = 0
        self.done = False
        self.player_is_patient = True
        self.animation_timer = 0
        self.animation_time_until_next = 0.03
        self.animate = self.hold
        self.textDone = False



    def setWordPlacement(self):
        self.current_word_surface = self.font.render(self.currentWord, 0, self.fontColor, self.font)
        self.current_word_width, self.word_height = self.current_word_surface.get_size()

        if self.textX + self.current_word_width >= self.rect.width - self.endBorder:
            self.setNewLine(self.word_height)
        else:
            self.textX += self.current_word_width

    def setNewLine(self, word_height):
        if self.textY + word_height >= self.rect.height - self.endBorder:
            self.screenFull = True
        else:
            self.newLine(word_height)
                
    def clearScreen(self):
        self.textX = self.originalX
        self.textY = self.originalY
        self.image.blit(self.originalImage, (0,0))
        self.screenFull = False

    def newLine(self, word_height):
        self.textX = self.originalX
        self.textY += word_height

    def blitLetter(self):
        word_surface = self.font.render(self.currentWord[:self.letterIndex], 0, self.fontColor, self.font)
        self.image.blit(word_surface, (self.textX, self.textY))
        self.letterIndex += 1


    def nextLetter(self):
        return self.letterIndex <= len(self.currentWord)

    def nextWord(self):
        return self.wordIndex < len(self.currentLine) -1
    
    def nextLine(self):
        return self.lineIndex < len(self.lines) -1

    def setNextWord(self):
        self.letterIndex = 0
        self.wordIndex += 1
        self.currentWord = self.currentLine[self.wordIndex]


    def setNextLine(self):
        self.wordIndex = 0
        self.lineIndex += 1
        self.currentLine = self.lines[self.lineIndex]
        self.setNewLine(self.word_height)



    def renderText(self):
        if self.nextLetter():
            self.blitLetter()
        else:
            if self.nextWord():
                self.setNextWord()
                self.setWordPlacement()
            else:
                if self.nextLine():
                    self.setNextLine()
                else:
                    # to end a full blit when done
                    self.screenFull = True
                    self.textDone = True
                    self.animate = self.hold

    def scrollLetters(self):
        if self.animation_timer < self.animation_time_until_next:
            # 10ms is max animation speed
            self.animation_timer += self.dt
        else:
            # do animation stuff
            if not self.screenFull:
                self.renderText()
            self.animation_timer = 0

    def blitAll(self):
        while not self.screenFull:
            self.renderText()
        
    def close(self):
        self.reset()
        self.done = True
        self.kill()

    def hold(self):
        pass

    def animate(self):
        pass

    def doA(self):
        if self.textDone:
            self.close()

        if not self.screenFull:
            if self.player_is_patient:
                self.animate = self.scrollLetters
                self.player_is_patient = False
            else:
                self.blitAll()
                self.player_is_patient = True

        else:
            self.animation = self.hold
            self.clearScreen()
