from engine import Game, Pos2, Pos4, keyboard, random
from objects import PhysObject, Camera2D
from GUI import button, rectangle
from tkinter import Canvas

# Создание основоного объекта игры
game = Game(title="Game 1", geometry="700x500", resizable=False)

def cube_draw_func(canvas: Canvas, pos: Pos2):
    size = 50
    canvas.create_oval(pos.x -size/2, pos.y - size/2, size/2 - 1 + pos.x, size/2 - 1 + pos.y)
    canvas.create_rectangle(pos.x -size/2, pos.y - size/2, size/2 + pos.x, size/2 + pos.y)

rect1 = rectangle(Pos4(10, 10, 120, 40), color="blue", anchor_x="left", anchor_y="bottom")

game.add_gui(rect1)

cube = PhysObject(Pos2(0, 0), cube_draw_func)

is_spawn = False

def can_spawn(event):
    global is_spawn
    is_spawn = not(is_spawn)

game.root.bind('<e>', lambda e:can_spawn(e))

camera = Camera2D(Pos2(0, 0))
game.add_object(camera)

# Что делать в кадре?
counter = 0
def main(_game: Game):
    global counter
    global is_spawn

    if is_spawn:
        new_cube = cube.clone()
        counter += 1
        new_cube.pos = Pos2(random.randint(-250, 250), 0)
        _game.add_object(new_cube)
        if counter % 100 == 0:
            print(f"Всего объектов: {counter}")
            is_spawn = False
    
    if keyboard.is_pressed('w'):
        camera.vec.y += 5
    if keyboard.is_pressed('s'):
        camera.vec.y -= 5
    if keyboard.is_pressed('a'):
        camera.vec.x += 5
    if keyboard.is_pressed('d'):
        camera.vec.x -= 5
    

# Создание основного цикла игры
game.mainloop(main)