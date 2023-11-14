from tkinter import Canvas
from objects import Node
import copy
from maths import Pos2, Size2, Vec2, DELTA

class gui_node(Node):
    def __init__(self, pos: Pos2, anchor_x: str = "left", anchor_y: str = "top"):
        super.__init__(pos)

        # Anchor x: left/center/right
        # Anchor y: top/center/bottom
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def render(self, canvas: Canvas):
        pass
        # Отрисовка на экране относительно длины и ширины (size)
        # Отрисовка children относительно parent