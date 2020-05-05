import pygame as pg
from superSprite import SuperSprite

pg.init()
screen = pg.display.set_mode()
sp = SuperSprite("images/csBig.png", 12)

print(len(sp.images))
index = 0
while True:
    screen.blit(sp.image, (0,0))
    pg.display.flip()
    index += 1
    index %= len(sp.images)
    print(index)
    sp.image = sp.images[index]
