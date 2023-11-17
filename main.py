from engine import Game
from objects import PhysicsNode, Square, Oval
from gui import gui_node, Rect, Label
from maths import Pos2, Vec2, Size2
from math import atan, sin, cos
import random

game = Game("Test", "700x500", False)

PhysNode = PhysicsNode(Pos2(-100, -100))

oval1 = Oval(Pos2(0, 0), Size2(50, 50), "white", 1)

PhysNode.add_child(oval1)

game.add_object(PhysNode)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass

game.mainloop(main)
