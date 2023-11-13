from tkinter import Canvas as GameCanvas, Tk as Window
from matrix import Pos2

def empty_draw(canvas: GameCanvas, pos: Pos2):
    ...

def default_script(obj):
    ...

class gui_obj():
    def __init__(self, pos: Pos2,
    gui_draw: callable = empty_draw,
    gui_script: callable = default_script):
        self.pos = pos
        self.gui_draw = gui_draw
        self.gui_script = gui_script

    def draw(self, canvas: GameCanvas):
        self.gui_draw(canvas, self)
        self.gui_script(self)


def default_button_draw(canvas, g):
    canvas.create_rectangle(g.pos.x, g.pos.y, g.point.x + g.pos.x, g.point.y + g.pos.y)


class button(gui_obj):
    def __init__(self,
        point1: Pos2, point2: Pos2,
        gui_draw: callable = default_button_draw, gui_script: callable = default_script):
        super().__init__(point1, gui_draw, gui_script)
        self.point = point2
    
    def draw(self, canvas: GameCanvas):
        super().draw(canvas)


def default_rectangle_draw(canvas, g):
    canvas.create_rectangle(g.pos.x,
    g.pos.y, g.point.x + g.pos.x, g.point.y + g.pos.y,
    fill=g.color, outline=g.border_color, width=g.border)


class rectangle(gui_obj):
    def __init__(self,
        point1: Pos2, point2: Pos2,
        color="black", border_color = "black", border: float = 0,
        gui_draw: callable = default_rectangle_draw, gui_script: callable = default_script):
        super().__init__(point1, gui_draw, gui_script)
        self.point = point2
        self.color = color
        self.border = border
        self.border_color = border_color
    
    def draw(self, canvas: GameCanvas):
        super().draw(canvas)

def screen_center(root: Window) -> Pos2:
    return Pos2(root.winfo_width()//2, root.winfo_height()//2)

"""
# Anchors
def get_gui_pos(root: Window, anchor: str = "cc") -> Pos2:
    width = 0
    match anchor[0]:
        case "c":
            width = 0
        case ""
"""