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
    canvas.create_oval(0+pos.x, 0+pos.y, 50+pos.x, 50+pos.y)
    #print(pos.x, pos.y)


player = GameObject(Pos2(200, 200), func)

game.add_object(player)

speed = 2

def moving(event, key: int):
    match key:
        case 1:
            player.vec += Vec2(0, -speed)
        case 2:
            player.vec += Vec2(-speed, 0)
        case 3:
            player.vec += Vec2(0, speed)
        case 4:
            player.vec += Vec2(speed, 0)
        case 5:
            player.vec += Vec2(-speed, -speed)
        case 6:
            player.vec += Vec2(speed, -speed)
        case 7:
            player.vec += Vec2(-speed, speed)
        case 8:
            player.vec += Vec2(speed, speed)

root.bind('<w>', lambda e:moving(e, 1))
root.bind('<a>', lambda e:moving(e, 2))
root.bind('<s>', lambda e:moving(e, 3))
root.bind('<d>', lambda e:moving(e, 4))

root.bind('<w>+<a>', lambda e:moving(e, 5))
root.bind('<w>+<d>', lambda e:moving(e, 6))

root.bind('<s>+<a>', lambda e:moving(e, 7))
root.bind('<s>+<d>', lambda e:moving(e, 8))

def main():
    pass

# Создание основного цикла игры
game.mainloop(root, Cnv, main)
