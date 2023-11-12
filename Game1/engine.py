import time
import random
import tkinter as tk

def tksleep(self, time:float) -> None:
    self.after(int(time*1000), self.quit)
    self.mainloop()
tk.Misc.tksleep = tksleep

DELTA = 0.02

def tksleep(root, t: float):
    try:
        ms = int(t*1000)
        root = tk._get_default_root('sleep')
        var = tk.IntVar(root)
        root.after(ms, var.set, 1)
        root.wait_variable(var)
    except:
        pass

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


def empty_draw(canvas: tk.Canvas, obj):
    ...

def default_script(obj):
    ...

def gen_id() -> int:
    return random.randint(0, 999999999999)


default_data = {
    "id": 0,
}

# Статичный объект
class GameObject():
    def __init__(self, pos: Pos2,
    draw_func: callable = empty_draw,
    script: callable = default_script, data: dict = default_data):
        self.pos = pos

        self.vec = Vec2.default()
        self.draw_func = draw_func
        self.script = script

        self.data = data

        self.data["id"] = gen_id()
        self.data["removed"] = False

    # Рисование объекта
    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self)
        self.script(self) # Скрипты работают каждый кадр.

    def remove(self):
        self.data["removed"] = True

    def set_script(self, new_script: callable):
        self.script = new_script

    # Клонировать объект
    def clone(self):
        return GameObject(self.pos, self.draw_func, self.script, self.data)

    def __str__(self):
        return str(self.data["id"])


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
        self.draw_func(canvas, self)

        # Применение физики
        self.physics_func(self)

        self.script(self) # Скрипты работают каждый кадр.

    def set_physics(self, new_phys):
        self.physics_func = new_phys
    
    # Клонировать объект
    def clone(self):
        return PhysObject(self.pos, self.draw_func, self.physics_func, self.mass)

def is_rendered(root: tk.Tk, obj) -> bool:
    if obj.pos.y < -100 or obj.pos.y > root.winfo_height() + 100 or obj.pos.x < -100 or obj.pos.x > root.winfo_width() + 100:
        return False
    else:
        return True

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
                _main(self) # Вызываем необходимые функции

                root.update() # Обновление Окна

                # Очистка Canvas
                game_canvas.delete('all')

                # Отрисовка всех объектов на экране
                for obj in self.objects:
                    if obj.data["removed"] == True:
                        self.objects.remove(obj)
                    if is_rendered(root, obj):
                        obj.draw(game_canvas)

                root.tksleep(DELTA) # Ожидание 
    
        except tk.TclError:
            print("Window is closed. Exiting...")
