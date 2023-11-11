import time
import tkinter as tk

DELTA = 0.03

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


class GameObject():
    def __init__(self, pos: Pos2, draw_func: callable, max_speed: float=10):
        self.pos = pos
        self.max_speed = max_speed
        self.vec = Vec2.default()
        self.draw_func = draw_func

    def clump(self, _min, _max):
        self.vec = Vec2(max(_min, min(_max, self.vec.x)), max(_min, min(_max, self.vec.y)))

    def moving(self):
        self.clump(-self.max_speed, self.max_speed)

        self.pos += Pos2(self.vec.x, self.vec.y) * DELTA * self.max_speed

        self.vec -= self.vec * DELTA

    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self.pos)
        self.pos = Pos2(self.pos.x, self.pos.y)
        
        self.moving()


class PhysObject(GameObject):
    def __init__(self, pos: Pos2, draw_func: callable, max_speed: float=50):
        super().__init__(pos, draw_func, max_speed)
    
    def clump(self, _min1, _max1, _min2, _max2):
        self.vec = Vec2(max(_min1, min(_max1, self.vec.x)), max(_min2, min(_max2, self.vec.y)))

    def moving(self):
        #self.clump(-self.max_speed, self.max_speed, 0, 10000)

        self.pos += Pos2(self.vec.x, self.vec.y + 9.8) * DELTA * self.max_speed

        self.vec -= self.vec * DELTA * self.max_speed

    def draw(self, canvas: tk.Canvas):
        self.draw_func(canvas, self.pos)
        self.pos = Pos2(self.pos.x, self.pos.y)
        
        self.moving()


class Game():
    def __init__(self):
        self.objects = []

    def add_object(self, obj: GameObject):
        if not(obj in self.objects):
            self.objects.append(obj)

    def mainloop(self, root: tk.Tk, game_canvas: tk.Canvas, _main: callable):
        while True:
            _main() # Вызываем необходимые функции

            root.update()
            # Очистка Canvas
            try:
                game_canvas.delete('all')
            except:
                pass

            for obj in self.objects:
                obj.draw(game_canvas)

            time.sleep(DELTA)

            # Проверка открыто ли окно
            try:
                state = root.wm_state()
            except tk.TclError:
                print("Window is closed. Exiting...")
                break
