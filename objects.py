from tkinter import Canvas
import copy
from maths import Pos2, Size2, Vec2, DELTA

# Статичный объект (без отрисовки и коллизии), точка в пространстве
class Node():
    def __init__(self, pos: Pos2):
        self.pos = pos # Центр ноды
        self.children = list()
        self.level = 0

    def add_child(self, *children):
        for c in list(children):
            self.children.append(c)

    # Рендер относительно камеры
    def render(self, canvas: Canvas, render_pos: Pos2):
        for c in self.children:
            c.render(canvas, c.pos + render_pos)

    def clone(self):
        return copy.deepcopy(self)

    def _type(self):
        return self.__class__.__name__

# Квадрат, имеющий размер и отрисовку
class Square(Node):
    def __init__(self, pos: Pos2, size: Size2, color: str = "black", border: float = 0, border_color: str = "black", ):
        super().__init__(pos)
        self.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def render(self, canvas: Canvas, render_pos: Pos2):
        # Отрисовка квадрата
        canvas.create_rectangle(render_pos.x - self.size.width//2, render_pos.y + self.size.height//2,
        render_pos.x + self.size.width//2, render_pos.y - self.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)

        super().render(canvas, render_pos)

# Овал, имеющий размер и отрисовку
class Oval(Node):
    def __init__(self, pos: Pos2, size: Size2, color: str = "black", border: float = 0, border_color: str = "black", ):
        super().__init__(pos)
        self.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def render(self, canvas: Canvas, render_pos: Pos2):
        # Отрисовка квадрата
        canvas.create_oval(render_pos.x - self.size.width//2, render_pos.y + self.size.height//2,
        render_pos.x + self.size.width//2, render_pos.y - self.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)

        super().render(canvas, render_pos)

def default_physics(obj):
    # Default gravity
    obj.vec += obj.gravity

def none_physics(obj):
    pass

# Точка в пространстве, которая имеет физику
class PhysicsNode(Node):
    def __init__(self, pos: Pos2, gravity: Vec2 = Vec2(0, 9.81)):
        super().__init__(pos)
        self.vec = Vec2.default()
        self.gravity = gravity
        self.physics = default_physics
    
    def set_physics(self, phys: callable):
        self.physics = phys

    def render(self, canvas: Canvas, render_pos: Pos2):
        # call physics function
        self.physics(self)
        self.pos += self.vec * DELTA

        super().render(canvas, render_pos)

class Camera2D(PhysicsNode):
    def __init__(self, pos: Pos2):
        super().__init__(pos)
        self.physics = none_physics
    
    def default(*self):
        return Camera2D(Pos2.default())