import pyglet as pg
#from pyglet import shapes

window = pg.window.Window(960, 540)
batch = pg.graphics.Batch()

square = pg.shapes.Rectangle(200, 200, 200, 200, color=(55, 55, 255), batch=batch)
square.opacity = 128
square.rotation = 0

@window.event
def on_draw():
    window.clear()
    batch.draw()

pg.app.run()