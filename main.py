from engine import Game
from objects import PhysicsNode, Square
from maths import Pos2, Vec2, Size2

game = Game("Test", "700x500", False)

PhysNode = PhysicsNode(Pos2(0, 0))

square1 = Square(Pos2(0, 0), Size2(100, 100), "white", 1)

PhysNode.add_child(square1)

square2 = Square(Pos2(5, 5), Size2(100, 100), "white", 1)

square1.add_child(square2)

game.add_object(PhysNode)

# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    pass

game.mainloop(main)
