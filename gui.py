import tkinter
from tkinter import Canvas
from objects import Node
import copy
from maths import Pos2, Rot2, Size2, Vec2, Transform, DELTA

class gui():
    def __init__(self, pos: Pos2, anchor_x: str = "left", anchor_y: str = "top"):
        self.transform = Transform(pos) # Центр GUI
        self.transform.size = Size2.default()
        self.children = list()

        # Anchor x: left/center/right
        # Anchor y: top/center/bottom
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def add_child(self, *children):
        for c in list(children):
            self.children.append(c)
    
    def default_anchor(self, render_transform: Transform) -> Transform:
        left_pos = Pos2(render_transform.position.x - self.transform.size.width//2,
        render_transform.position.y - self.transform.size.height//2)

        return Transform(left_pos, self.transform.size)

    def get_anchor_pos(self, parent_transform: Transform) -> Transform:
        render_x = 0
        match self.anchor_x:
            case "left":
                render_x = parent_transform.position.x + self.transform.position.x + self.transform.size.width//2
            case "right":
                render_x = parent_transform.position.x + parent_transform.size.width - self.transform.position.x - self.transform.size.width//2
            case "center":
                render_x = parent_transform.position.x + parent_transform.size.width//2 + self.transform.position.x
            case _:
                render_x = parent_transform.position.x + self.transform.position.x + self.transform.size.width//2
        render_y = 0
        match self.anchor_y:
            case "top":
                render_y = parent_transform.position.y + self.transform.position.y + self.transform.size.height//2
            case "bottom":
                render_y = parent_transform.position.y + parent_transform.size.height - self.transform.position.y - self.transform.size.height//2
            case "center":
                render_y = parent_transform.position.y + parent_transform.size.height//2 + self.transform.position.y
            case _:
                render_y = parent_transform.position.y + self.transform.position.y + self.transform.size.height//2
        return Transform(Pos2(render_x, render_y))

    def draw(self, canvas: Canvas, parent_transform: Transform):
        render_transform = self.get_anchor_pos(parent_transform)
        
        #canvas.create_oval(render_transform.position.x - 5, render_transform.position.y - 5, render_transform.position.x + 5, render_transform.position.y + 5)
        # Отрисовка children относительно parent
        for c in self.children:
            c.draw(canvas, self.default_anchor(render_transform))
        
    def clone(self):
        return copy.deepcopy(self)

    def __type__(self):
        return self.__class__.__name__

# Прямоугольник 
# Отрисовка на экране относительно длины и ширины (size)
class Rect(gui):
    def __init__(self, pos: Pos2, size: Size2, anchor_x: str = "left", anchor_y: str = "top", color: str = "black", border: float = 0, border_color: str = "black",):
        super().__init__(pos, anchor_x, anchor_y)
        self.transform.size = size
        self.color = color
        self.border = border
        self.border_color = border_color

    def draw(self, canvas, parent_transform):
        render_transform = self.get_anchor_pos(parent_transform)

        canvas.create_rectangle(render_transform.position.x - self.transform.size.width//2, render_transform.position.y + self.transform.size.height//2,
        render_transform.position.x + self.transform.size.width//2, render_transform.position.y - self.transform.size.height//2,
        fill=self.color, width=self.border, outline=self.border_color)
        
        super().draw(canvas, parent_transform)

class Button(Rect):
    pass

class Label(gui):
    def __init__(self, pos: Pos2, text: str, color: str = "white"):
        super().__init__(pos)
        self.text = text
        self.color = color
    
    def render(self, canvas: Canvas, parent_transform):
        render_transform = self.get_anchor_pos(parent_transform)
        #canvas.create_oval(render_pos.x - 5, render_pos.y - 5, render_pos.x + 5, render_pos.y + 5, fill="white")
        canvas.create_text(render_pos.x, render_pos.y, text = self.text, fill=self.color)
        
        super().render(canvas, parent_transform)