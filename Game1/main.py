import tkinter as tk
import keyboard
from engine import *

# Cоздание основного окна
root = tk.Tk()

# Настройка окна
root.title("Game 1")
root.geometry("700x500")
root.resizable(False, False)

# Создание Canvas для отрисовки
Cnv = tk.Canvas(root)

# Создание основоного объекта игры
game = Game()

# Добавляем Canvas на экран
Cnv.pack(fill=tk.BOTH, expand=True)

def draw_rec(canvas: tk.Canvas, pos: Pos2):
    width = 550
    height = 50
    canvas.create_rectangle(pos.x -width/2, pos.y - height/2, width/2 + pos.x, height/2 + pos.y)

rect1 = GameObject(Pos2(0, 0), draw_rec)

def cube_draw_func(canvas: tk.Canvas, pos: Pos2):
    size = 50
    canvas.create_oval(pos.x -size/2, pos.y - size/2, size/2 - 1 + pos.x, size/2 - 1 + pos.y)
    canvas.create_rectangle(pos.x -size/2, pos.y - size/2, size/2 + pos.x, size/2 + pos.y)

cube = PhysObject(Pos2(100, 100), cube_draw_func)
camera = Camera2D(Pos2(0, 0))

game.add_object(rect1)
game.add_object(camera)

# Что делать в кадре?
def main(_game: Game):
    new_cube = cube.clone()
    new_cube.pos = Pos2(random.randint(-250, 250), 0)
    _game.add_object(new_cube)

# Создание основного цикла игры
game.mainloop(root, Cnv, main)