import time
import keyboard
import random
import tkinter as tk

def tksleep(self, time:float) -> None:
    self.after(int(time*1000), self.quit)
    self.mainloop()
tk.Misc.tksleep = tksleep

DELTA = 1/60 # 60 кадров в секунду

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

    def clump(self, _min_x, _min_y, _max_x, _max_y):
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


class Vec2():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def clump(self, _min_x, _min_y, _max_x, _max_y):
        self.x = clump(self.x, _min_x, _max_x)
        self.y = clump(self.y, _min_y, _max_y)

    def default(*self):
        return Vec2(0, 0)

    def length(*self) -> float:
        return (self.x**2 + self.y**2) ** (1/2)

    def __str__(self):
        return str((self.x, self.y))
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)


def empty_draw(canvas: tk.Canvas, pos: Pos2):
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
    def draw(self, canvas: tk.Canvas, camera_pos: Pos2):
        self.draw_func(canvas, self.pos+camera_pos)

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

    def _type(self) -> str:
        return self.__class__.__name__


G = 9.8


def default_phys(obj):
    obj.vec.y += DELTA * obj.mass * G # Земная гравитация
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
    def draw(self, canvas: tk.Canvas, camera_pos: Pos2):
        super().draw(canvas, camera_pos)

        # Применение физики
        self.physics_func(self)

    def set_physics(self, new_phys):
        self.physics_func = new_phys
    
    # Клонировать объект
    def clone(self):
        return PhysObject(self.pos, self.draw_func, self.physics_func, self.mass)


def camera_draw(canvas: tk.Canvas, pos: Pos2):
    size = 15
    canvas.create_oval(pos.x -size/2, pos.y - size/2, size/2 + pos.x, size/2 + pos.y)


def camera_phys(obj):
    obj.pos += Pos2(obj.vec.x * DELTA, obj.vec.y * DELTA)
    obj.vec.clump(-50, -50, 50, 50)


class Camera2D(PhysObject):
    def __init__(
        self,
        pos: Pos2):
        super().__init__(pos, camera_draw, camera_phys)
    
    # Рисование объекта
    def draw(self, canvas: tk.Canvas, camera_pos: Pos2):
        self.draw_func(canvas, camera_pos)
        self.physics_func(self)
        

def root_center(root: tk.Tk) -> Pos2:
    return Pos2(root.winfo_width()//2, root.winfo_height()//2)


class Game():
    def __init__(self, root: tk.Tk):
        self.objects = []
        self.root = root

    def add_object(self, *objs: GameObject):
        for obj in list(objs):
            if not(obj in self.objects):
                self.objects.append(obj)

    def find_camera(self, objects: list) -> Camera2D | None:
        for obj in list(objects):
            if obj._type() == "Camera2D":
                return obj
        return None

    def mainloop(self, game_canvas: tk.Canvas, _main: callable):
        try:
            while True:
                _main(self) # Вызываем необходимые функции

                self.root.update() # Обновление Окна

                # Очистка Canvas
                game_canvas.delete('all')

                current_camera = self.find_camera(self.objects)

                # Отрисовка всех объектов на экране
                for obj in self.objects:
                    if current_camera == None:
                        continue
                    # Отрисовка камеры, если нужно
                    if obj == current_camera:
                        obj.draw(game_canvas, root_center(self.root))
                        continue
                    if obj.data["removed"] == True:
                        # Удаление объектов с тегом "removed"
                        self.objects.remove(obj)
                        continue

                    obj.draw(game_canvas, root_center(self.root) + current_camera.pos)

                self.root.tksleep(DELTA) # Ожидание 
    
        except tk.TclError:
            print("Window is closed. Exiting...")
