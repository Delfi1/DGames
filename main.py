from engine import Game
from objects import PhysicsNode, Square
from gui import gui_node, Rect
from maths import Pos2, Vec2, Size2
import random

game = Game("Test", "700x500", False)

PhysNode = PhysicsNode(Pos2(0, 0))

square1 = Square(Pos2(0, -50 * 50), Size2(50, -100 * 50), "white", 1)

PhysNode.add_child(square1)

game.add_object(PhysNode)

gui1 = Rect(Pos2(5, 5), size=Size2(200, 100))

game.add_gui(gui1)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass

game.mainloop(main)
