from matrix import Pos2, Vec2
from maths import clump
import constants
from tkinter import Canvas as GameCanvas

def empty_render(canvas: GameCanvas, pos: Pos2):
    ...

def default_script(obj):
    ...

default_data = {

}

# Статичный объект
class GameObject():
    def __init__(self, pos: Pos2,
    render_func: callable = empty_render,
    script: callable = default_script, data: dict = default_data):
        self.pos = pos

        self.render_func = render_func
        self.script = script

        self.data = data

    # Рисование объекта
    def render(self, canvas: GameCanvas, delta_: float, render_pos: Pos2):
        self.render_func(canvas, render_pos)

        self.script(self) # Скрипты работают каждый кадр.

    def set_script(self, new_script: callable):
        self.script = new_script

    # Клонировать объект
    def clone(self):
        return GameObject(self.pos, self.render_func, self.script, self.data)

    def _type(self) -> str:
        return self.__class__.__name__


def default_phys(obj, delta):
    obj.vec.y += delta * obj.mass * constants.G # Земная гравитация
    obj.pos += Pos2(obj.vec.x, obj.vec.y)


class PhysObject(GameObject):
    def __init__(
        self,
        pos: Pos2,
        render_func: callable = empty_render,
        physics_func: callable = default_phys, mass = 1):
        super().__init__(pos, render_func)
        self.physics_func = physics_func
        self.mass = mass
        self.vec = Vec2.default()
    
    # Рисование объекта
    def render(self, canvas: GameCanvas, delta_: float, render_pos: Pos2):
        super().render(canvas, delta_, render_pos)

        # Применение физики
        self.physics_func(self, delta_)

    def set_physics(self, new_phys: callable):
        self.physics_func = new_phys
    
    # Клонировать объект
    def clone(self):
        return PhysObject(self.pos, self.render_func, self.physics_func, self.mass)


def camera_render(canvas: GameCanvas, pos: Pos2):
    size = 16
    canvas.create_oval(pos.x -size/2, pos.y - size/2, size/2 + pos.x, size/2 + pos.y)
    canvas.create_line(pos.x, 0, pos.x, canvas.winfo_height())
    canvas.create_line(0, pos.y, canvas.winfo_width(), pos.y)
    #canvas.create_line(pos.x, pos.y - size/2, pos.x, pos.y + size/2)
    #canvas.create_line(pos.x - size/2, pos.y, pos.x + size/2, pos.y)


def camera_phys(obj, delta):
    obj.pos += Pos2(obj.vec.x * delta, obj.vec.y * delta)
    obj.vec.clump(-50, -50, 50, 50)


class Camera2D(PhysObject):
    def __init__(
        self,
        pos: Pos2):
        super().__init__(pos, camera_render, camera_phys)
    
    # Рисование объекта
    def render(self, canvas: GameCanvas, delta_: float, render_pos: Pos2):
        self.render_func(canvas, render_pos)
        self.physics_func(self, delta_)