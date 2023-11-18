from engine import Game
from objects import PhysicsNode, Square, Oval, Camera2D
from gui import gui_node, Rect, Label
from maths import Pos2, Vec2, Size2
from math import atan, sin, cos
import random

game = Game("Test", "700x500", False)
game.switch_full_screen(0)

Phys = PhysicsNode(Pos2(0, 0))

oval1 = Oval(Pos2(0, 0), Size2(50, 50), "white", 1)

Phys.add_child(oval1)

camera = Camera2D(Pos2(0, 0))

game.add_object(camera)

for c in range(50):
    new = Phys.clone()

    new.pos = Pos2(random.randint(-325, 325), random.randint(-225, 225))

    game.add_object(new)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass

game.mainloop(main)
