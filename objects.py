from tkinter import Canvas
import copy
from maths import *

class AddSceneAsChild(Exception):
    def __init__(self, message, errors):
        super().__init__(message)

class Node():
    def __init__(self, position: Pos2):
        self.transform = Transform(position)
        self.children = list()

    def add_child(self, *children):
        for obj in list(children):
            if not(obj in self.children):
                if obj._type() == "Scene":
                    raise AddSceneAsChild
                self.children.append(obj)

    def render(self, canvas: Canvas, render_transform: Transform):
        for c in self.children:
            children_transform = render_transform + c.transform
            c.render(canvas, children_transform)

    def clone(self):
        return copy.deepcopy(self)
    
    def _type(self):
        return self.__class__.__name__


class Square(Node):
    def __init__(self, position: Pos2, size: Size2, color: str = "black", border: float = 0, border_color: str = "black", ):
        super().__init__(position)
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

class Camera2D(Node):
    def __init__(self, position):
        self.transform = Transform(position)

    def default(*self):
        return Camera2D(Pos2.default())


class Scene(Node):
    def __init__(self):
        self.objects = list()
        self.gui = list()

        self.current_camera = Camera2D.default()
    
    def add_object(self, *objects):
        for obj in list(objects):
            self.objects.append(obj)

    def render(self, canvas: Canvas):
        for obj in self.objects:
            screen_center = Pos2(canvas.winfo_width()//2, canvas.winfo_height()//2)
            render_transform = obj.transform + Transform(screen_center) + self.current_camera.transform
            obj.render(canvas, render_transform)