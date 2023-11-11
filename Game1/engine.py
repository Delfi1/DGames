import time
import tkinter as tk

DELTA = 0.03

def clump(value, _min, _max):
    return max(_min, min(_max, value))

class Pos2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def default(*self):
        return Pos2(0, 0)

    def __str__(self):
        return str((self.x, self.y))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vec2(self.x * value, self.y * value)


class Vec2():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def default(*self):
        return Vec2(0, 0)

    def __str__(self):
        return str((self.x, self.y))
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vec2(self.x * value, self.y * value)


def empty_draw(canvas: tk.Canvas, pos: Pos2):
    pass


def default_phys(canvas: tk.Canvas, pos: Pos2, vec: Vec2):
    pass


# Статичный объект
class GameObject():
    def __init__(self, pos: Pos2, draw_func: callable = empty_draw):
        self.pos = pos

        self.vec = Vec2.default()
        self.draw_func = draw_func

    # Рисование объекта
    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self.pos)


    # Клонировать объект
    def clone(self):
        return GameObject(self.pos, self.draw_func)


class PhysObject(GameObject):
    def __init__(self, pos: Pos2, draw_func: callable = empty_draw, physics_func: callable = default_phys):
        super().__init__()
        self.vec = Vec2.default()
    
    # Рисование объекта
    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self.pos)

        # Применение физики
        physics_func(canvas, pos, vec)
    

class Game():
    def __init__(self):
        self.objects = []

    def add_object(self, *objs: GameObject):
        for obj in list(objs):
            if not(obj in self.objects):
                self.objects.append(obj)

    def mainloop(self, root: tk.Tk, game_canvas: tk.Canvas, _main: callable):
        try:
            while True:
                _main() # Вызываем необходимые функции

                root.update() # Обновление Окна

                # Очистка Canvas
                game_canvas.delete('all')

                # Отрисовка всех объектов на экране
                for obj in self.objects:
                    obj.draw(game_canvas)

                time.sleep(DELTA) # Ожидание 
    
        except tk.TclError:
            print("Window is closed. Exiting...")
