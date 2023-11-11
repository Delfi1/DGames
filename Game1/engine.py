import time
import tkinter as tk

DELTA = 0.03

def clump(value, _min, _max):
    return max(_min, min(_max, value))

class Pos2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clump(self, _min_x, _max_x, _min_y, _max_y):
        self.x = clump(self.x, _min_x, _max_x)
        self.y = clump(self.y, _min_y, _max_y)

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
    
    def clump(self, _min_x, _max_x, _min_y, _max_y):
        self.x = clump(self.x, _min_x, _max_x)
        self.y = clump(self.y, _min_y, _max_y)

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


G = 9.8


def default_phys(obj):
    obj.vec.y += DELTA * obj.mass * G

    obj.pos += Pos2(obj.vec.x, obj.vec.y)


class PhysObject(GameObject):
    def __init__(
        self,
        pos: Pos2,
        draw_func: callable = empty_draw,
        physics_func: callable = default_phys, mass = 1):
        super().__init__(pos, draw_func)
        self.physics_func = physics_func
        self.mass = mass
        self.vec = Vec2.default()
    
    # Рисование объекта
    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self.pos)

        # Применение физики
        self.physics_func(self)
    

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
