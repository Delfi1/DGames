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


def cube_draw_func(canvas: tk.Canvas, pos: Pos2):
    size = 50
    canvas.create_oval(0 + pos.x, 0 + pos.y, size - 1 + pos.x, size - 1 + pos.y)
    canvas.create_rectangle(0 + pos.x, 0 + pos.y, size + pos.x, size + pos.y)


def cube_phys(obj):
    pass

camera = Camera2D(Pos2(0, 0))
cube = GameObject(Pos2(100, 100), cube_draw_func)

game.add_object(cube, camera)

# Что делать в кадре?
def main(_game: Game):
    pass

# Создание основного цикла игры
game.mainloop(root, Cnv, main)