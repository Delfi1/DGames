import tkinter
from tkinter import Canvas
from objects import Node
import copy
from maths import Pos2, Size2, Vec2, DELTA

class gui_node():
    def __init__(self, pos: Pos2, anchor_x: str = "left", anchor_y: str = "top"):
        self.pos = pos # Центр ноды
        self.children = list()

        # Anchor x: left/center/right
        # Anchor y: top/center/bottom
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def add_child(self, *children):
        for c in list(children):
            self.children.append(c)

    def get_anchor_pos(self, parent_pos: Pos2, parent_size: Size2) -> Pos2:
        render_x = 0
        match self.anchor_x:
            case "left":
                render_x = parent_pos.x + self.pos.x
            case "right":
                render_x = parent_pos.x + parent_size.width - self.pos.x
            case "center":
                render_x = parent_pos.x + parent_size.width//2 + self.pos.x
            case _:
                render_x = parent_pos.x + self.pos.x
        render_y = 0
        match self.anchor_y:
            case "top":
                render_y = parent_pos.y + self.pos.y
            case "bottom":
                render_y = parent_pos.y + parent_size.height - self.pos.y
            case "center":
                render_y = parent_pos.y + parent_size.height//2 + self.pos.y
            case _:
                render_y = parent_pos.y + self.pos.y
        return Pos2(render_x, render_y)

    def render(self, canvas: Canvas, parent_pos: Pos2, parent_size: Size2):
        render_pos = self.get_anchor_pos(parent_pos, parent_size)
        
        #canvas.create_oval(render_pos.x - 5, render_pos.y - 5, render_pos.x + 5, render_pos.y + 5)
        # Отрисовка children относительно parent
        for c in self.children:
            c.render(canvas, self.get_anchor_pos(parent_pos, parent_size))
        
    def clone(self):
        return copy.deepcopy(self)

    def __type__(self):
        return self.__class__.__name__

# Прямоугольник 
# Отрисовка на экране относительно длины и ширины (size)
class Rect(gui_node):
    def __init__(self, pos: Pos2, size: Size2, anchor_x: str = "left", anchor_y: str = "top", color: str = "black", border: float = 0, border_color: str = "black",):
        super().__init__(pos, anchor_x, anchor_y)
        self.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def get_anchor_pos(self, parent_pos: Pos2, parent_size: Size2) -> Pos2:
        render_x = 0
        match self.anchor_x:
            case "left":
                render_x = parent_pos.x + self.pos.x + self.size.width//2
            case "right":
                render_x = parent_pos.x + parent_size.width - self.pos.x - self.size.width//2
            case "center":
                render_x = parent_pos.x + parent_size.width//2 + self.pos.x
            case _:
                render_x = parent_pos.x + self.pos.x + + self.size.width//2
        render_y = 0
        match self.anchor_y:
            case "top":
                render_y = parent_pos.y + self.pos.y + self.size.height//2
            case "bottom":
                render_y = parent_pos.y + parent_size.height - self.pos.y - self.size.height//2
            case "center":
                render_y = parent_pos.y + parent_size.height//2 + self.pos.y
            case _:
                render_y = parent_pos.y + self.pos.y + self.size.height//2
        return Pos2(render_x, render_y)

    def render(self, canvas, parent_pos, parent_size):
        render_pos = self.get_anchor_pos(parent_pos, parent_size)

        canvas.create_rectangle(render_pos.x - self.size.width//2, render_pos.y + self.size.height//2,
        render_pos.x + self.size.width//2, render_pos.y - self.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)
        
        super().render(canvas, parent_pos, parent_size)

class Button(Rect):
    pass

class Label(gui_node):
    def __init__(self, pos: Pos2, text: str):
        super().__init__(pos)
        self.text = text
    
    def render(self, canvas, parent_pos, parent_size):
        render_pos = self.get_anchor_pos(parent_pos, parent_size)

        label = tkinter.Label(canvas, text=self.text)
        label.place(render_pos)
        super().render(canvas, parent_pos, parent_size)