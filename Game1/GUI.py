from tkinter import Canvas as GameCanvas, Tk as Window
from matrix import Pos2, Pos4

def empty_draw(canvas: GameCanvas, pos: Pos2):
    ...

def default_script(obj):
    ...

class gui_obj():
    def __init__(self, pos: Pos2,
    gui_draw: callable = empty_draw,
    anchor_x: str = "left",
    anchor_y: str = "top",
    gui_script: callable = default_script):
        self.pos = pos
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.gui_draw = gui_draw
        self.gui_script = gui_script
    
    def gui_pos(self, root: Window) -> Pos2:
        render_x = 0
        match self.anchor_x:
            case "left":
                render_x = 0 + self.pos.x
            case "right":
                render_x = root.winfo_width() - self.pos.x
            case "center":
                render_x = root.winfo_width()//2 + self.pos.x
            case _:
                render_x = 0 + self.pos.x
        render_y = 0
        match self.anchor_y:
            case "top":
                render_y = 0 + self.pos.y
            case "bottom":
                render_y = root.winfo_height() - self.pos.y
            case "center":
                render_y = root.winfo_height()//2 + self.pos.y
            case _:
                render_y = 0 + self.pos.y
        return Pos2(render_x, render_y)

    def draw(self, canvas: GameCanvas, root: Window):
        self.gui_draw(canvas, self.gui_pos(root), self)
        self.gui_script(self)


def default_rectangle_draw(canvas: GameCanvas, render_pos: Pos4, g):
    canvas.create_rectangle(render_pos.x1,
    render_pos.y1, render_pos.x2, render_pos.y2,
    fill=g.color, outline=g.border_color, width=g.border)


class rectangle(gui_obj):
    def __init__(self,
        pos: Pos4,
        anchor_x: str = "left", anchor_y: str = "top",
        color="black", border_color = "black", border: float = 0,
        gui_draw: callable = default_rectangle_draw, gui_script: callable = default_script):
        self.pos = pos
        self.color = color
        self.border = border
        self.border_color = border_color
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.gui_draw = gui_draw 
        self.gui_script = gui_script
    
    def gui_pos(self, root: Window) -> Pos4:
        render_x1 = 0
        match self.anchor_x:
            case "left":
                render_x1 = self.pos.x1
            case "right":
                render_x1 = root.winfo_width() - self.pos.x1
            case "center":
                render_x1 = root.winfo_width()//2 + self.pos.x1
            case _:
                render_x1 = self.pos.x1
        render_y1 = 0
        match self.anchor_y:
            case "top":
                render_y1 = self.pos.y1
            case "bottom":
                render_y1 = root.winfo_height() - self.pos.y1
            case "center":
                render_y1 = root.winfo_height()//2 + self.pos.y1
            case _:
                render_y1 = self.pos.y1
        
        render_x2 = 0
        match self.anchor_x:
            case "left":
                render_x2 = self.pos.x2
            case "right":
                render_x2 = root.winfo_width() - self.pos.x2
            case "center":
                render_x2 = root.winfo_width()//2 + self.pos.x2
            case _:
                render_x2 = self.pos.x2
        render_y2 = 0
        match self.anchor_y:
            case "top":
                render_y2 = self.pos.y2
            case "bottom":
                render_y2 = root.winfo_height() - self.pos.y2
            case "center":
                render_y2 = root.winfo_height()//2 + self.pos.y2
            case _:
                render_y2 = self.pos.y2
        return Pos4(render_x1, render_y1, render_x2, render_y2)

    def draw(self, canvas: GameCanvas, root: Window):
        print(type(self.gui_draw))
        self.gui_draw(canvas, self.gui_pos(root), self)
        self.gui_script(self)

def default_button_draw(canvas: GameCanvas, render_pos: Pos2, g):
    canvas.create_rectangle(render_pos.x, render_pos.y, g.point.x + render_pos.x, g.point.y + render_pos.y)

class button(rectangle):
    def __init__(self,
        point1: Pos2, point2: Pos2,
        gui_draw: callable = default_button_draw, anchor_x: str = "left", anchor_y: str = "top", gui_script: callable = default_script):
        super().__init__(point1=point1, point2=point2, anchor_x=anchor_x, anchor_y=anchor_y, gui_draw=gui_draw, gui_script=gui_script)
        self.point = point2

def screen_center(root: Window) -> Pos2:
    return Pos2(root.winfo_width()//2, root.winfo_height()//2)
