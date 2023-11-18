from tkinter import Canvas
import copy
from maths import Pos2, Rot2, Size2, Vec2, Transform, DELTA

def default_script(obj):
    pass

class Node():
    def __init__(self, pos: Pos2, script: callable = default_script):
        self.transform = Transform(pos)
        self.children = list()
        self.script = script
        self.layer = 0 # Дефолт Layer 

    def add_child(self, *children):
        for c in list(children):
            self.children.append(c)

    def set_script(self, new_script):
        self.script = new_script

    def render(self, canvas: Canvas, render_transform: Transform):
        self.script(self)

        for c in self.children:
            c.render(canvas, c.transform + render_transform)

    def clone(self):
        return copy.deepcopy(self)

    def _type(self):
        return self.__class__.__name__

# Квадрат, имеющий размер и отрисовку
class Square(Node):
    def __init__(self, pos: Pos2, size: Size2, color: str = "black", border: float = 0, border_color: str = "black", ):
        super().__init__(pos)
        self.transform.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def render(self, canvas: Canvas, render_transform: Transform):
        # Отрисовка 
        canvas.create_rectangle(render_transform.position.x - self.transform.size.width//2, render_transform.position.y + self.transform.size.height//2,
        render_transform.position.x + self.transform.size.width//2, render_transform.position.y - self.transform.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)

        super().render(canvas, render_transform)

# Овал, имеющий размер и отрисовку
class Oval(Node):
    def __init__(self, pos: Pos2, size: Size2, color: str = "black", border: float = 0, border_color: str = "black", ):
        super().__init__(pos)
        self.transform.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def render(self, canvas: Canvas, render_transform: Transform):
        # Отрисовка 
        canvas.create_oval(render_transform.position.x - self.transform.size.width//2, render_transform.position.y + self.transform.size.height//2,
        render_transform.position.x + self.transform.size.width//2, render_transform.position.y - self.transform.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)

        super().render(canvas, render_transform)

def default_physics(obj):
    # Default gravity
    obj.vec += obj.gravity * obj.mass

def none_physics(obj):
    pass

# Точка в пространстве, которая имеет физику
class PhysicsNode(Node):
    def __init__(self, pos: Pos2, gravity: Vec2 = Vec2(0, 9.81), mass: float = 1):
        super().__init__(pos)
        self.vec = Vec2.default()
        self.gravity = gravity
        self.mass = mass
        self.physics = default_physics
    
    def set_physics(self, phys: callable):
        self.physics = phys

    def render(self, canvas: Canvas, render_transform: Transform):
        # call physics function
        self.physics(self)
        self.transform.position += self.vec * DELTA

        super().render(canvas, render_transform)

class Area2D(Node):
    def __init__(self, pos: Pos2, size: Size2, signal: callable):
        super().__init__(pos)
        self.transform.size = size
        self.signal = signal

class Camera2D(Node):
    def __init__(self, pos: Pos2):
        super().__init__(pos)

    def default(*self):
        return Camera2D(Pos2.default())