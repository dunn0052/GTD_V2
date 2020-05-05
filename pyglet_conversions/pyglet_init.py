import pyglet
window = pyglet.window.Window()

sprite_image = pyglet.image.load("images/redPC.png")

batch = pyglet.graphics.Batch()

ball_sprites = []
for i in range(100):
    x, y = i * 10, 50
    ball_sprites.append(pyglet.sprite.Sprite(sprite_image, x, y, batch=batch))

@window.event
def on_draw():
    batch.draw()


pyglet.app.run()
