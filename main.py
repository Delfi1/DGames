from engine import Game
from objects import PhysicsNode, Square
from maths import Pos2, Vec2, Size2
import random

game = Game("Test", "700x500", False)

PhysNode = PhysicsNode(Pos2(0, 0))

square1 = Square(Pos2(0, 0), Size2(50, 50), "white", 1)

PhysNode.add_child(square1)

count = 0
# Основная функция игры, выполняется каждый кадр
def main(_game: Game):
    global count

    if count <= 300:
        new = PhysNode.clone()
        new.pos = Pos2(random.randint(-200, 200), 0)
        count += 1
        game.add_object(new)

    if count == 300:
        print(f"Количество объектов = {count}")


game.mainloop(main)
