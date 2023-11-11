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


def func(canvas: tk.Canvas, pos: Pos2):
    size = 50

    canvas.create_oval(0 + pos.x, 0 + pos.y, size - 1 + pos.x, size - 1 + pos.y)
    canvas.create_rectangle(0 + pos.x, 0 + pos.y, size + pos.x, size + pos.y)


player = GameObject(Pos2(325, 200), func)

game.add_object(player)

# Что делать в кадре?
def main():
    pass

# Создание основного цикла игры
game.mainloop(root, Cnv, main)
