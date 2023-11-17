from engine import Game
from objects import PhysicsNode, Square, Oval
from gui import gui_node, Rect, Label
from maths import Pos2, Vec2, Size2
from math import atan, sin, cos
import random

game = Game("Test", "700x500", False)

Phys = PhysicsNode(Pos2(0, 0))

oval1 = Oval(Pos2(0, 0), Size2(50, 50), "white", 1)

Phys.add_child(oval1)

summon = True
counter = 0

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    global summon, counter

    if summon:
        new = Phys.clone()
        new.pos = Pos2(random.randint(-250, 250), 0)
        new.level = random.randint(0, 10)
        game.add_object(new)
        counter += 1
    if counter == 100:
        summon = False

game.mainloop(main)
