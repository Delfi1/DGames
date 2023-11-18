from engine import Game
from objects import *
from gui import *
from maths import *
import random

game = Game("Test", "700x500", False)

Obj1 = PhysicsNode(Pos2(0, 0))

ov1 = Oval(Pos2(0, 0), Size2(50, 50))

def script_1(obj):
    if obj.transform.position.y >= game.Window.winfo_height()//2 - obj.transform.size.height:
        obj.vec = Vec2(-obj.vec.x, -obj.vec.y)

Obj1.set_script(script_1)

Obj1.add_child(ov1)

colors = {
    "0": "red",
    "1": "green",
    "2": "blue"
}

for c in range(3):
    for k in range(-325, 375, 50):
        new = Obj1.clone()
        new.transform.position = Pos2(k, c*50)
        new.children[0].color = colors[str(c)]
        game.add_object(new)

#game.add_object(Obj1)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass

game.mainloop(main)