import pyglet
window = pyglet.window.Window()

quad = pyglet.graphics.vertex_list(4,
    ('v2i', (10, 10,  100, 10, 100, 100, 10, 100)),
    ('c3B', (0, 0, 255, 0, 0, 255, 0, 255, 0,  0, 255, 0)))

@window.event
def on_draw():
    window.clear()
    quad.draw(pyglet.gl.GL_QUADS)


pyglet.app.run()
