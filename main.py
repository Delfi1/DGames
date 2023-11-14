from engine import Game
from objects import PhysicsNode, Square
from maths import Pos2, Vec2, Size2
import random

game = Game("Test", "700x500", False)

PhysNode = PhysicsNode(Pos2(0, 0))

square1 = Square(Pos2(0, -100 * 50), Size2(50, 50), "white", 1)

PhysNode.add_child(square1)

for x in range(0, 100):
    new = square1.clone()
    new.pos = Pos2(0, (x-100)*50)

    PhysNode.add_child(new)

game.add_object(PhysNode)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass


game.mainloop(main)
