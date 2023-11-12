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


def cube_draw_func(canvas: tk.Canvas, obj):
    size = 50
    canvas.create_oval(0 + obj.pos.x, 0 + obj.pos.y, size - 1 + obj.pos.x, size - 1 + obj.pos.y)
    canvas.create_rectangle(0 + obj.pos.x, 0 + obj.pos.y, size + obj.pos.x, size + obj.pos.y)

def cube_phys(obj):
    pass

cube = PhysObject(Pos2(325, 100), cube_draw_func)

# Что делать в кадре?
def main(_game: Game):
    new = cube.clone()

    new.pos = Pos2(random.randint(100, 600), 100)
    
    _game.add_object(new)

# Создание основного цикла игры
game.mainloop(root, Cnv, main)