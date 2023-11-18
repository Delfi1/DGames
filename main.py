from engine import Game
from objects import *
from gui import *
from maths import *
import random

game = Game("Test", "700x500", False)

Obj1 = PhysicsNode(Pos2(0, 0))

ov1 = Oval(Pos2(0, 0), Size2(50, 50))

platform = Square(Pos2(0, 200), Size2(1000, 0))

game.add_object(platform)

def script_1(obj):
    if obj.transform.position.y > platform.transform.position.y - obj.children[0].transform.size.height//2:
        if obj.transform.position.y >= platform.transform.position.y - obj.children[0].transform.size.height//2:
            if obj.vec.y > 0:
                obj.vec = Vec2(obj.vec.x, -obj.vec.y)
    
    obj.transform.position.y = clump(obj.transform.position.y, -10000, platform.transform.position.y - obj.children[0].transform.size.height//2-2)


Obj1.set_script(script_1)

Obj1.add_child(ov1)

colors = {
    "0": "red",
    "1": "green",
    "2": "blue"
}

counter = 0
for c in range(3):
    for k in range(-325, 375, 50):
        new = Obj1.clone()
        new.transform.position = Pos2(k, c*50 - counter * 5 - 100)
        new.children[0].color = colors[str(c)]
        game.add_object(new)
        counter += 1
    counter = 0

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass
game.mainloop(main)