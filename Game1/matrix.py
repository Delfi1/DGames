from maths import clump

class Pos2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clump(self, _min_x, _min_y, _max_x, _max_y):
        self.x = clump(self.x, _min_x, _max_x)
        self.y = clump(self.y, _min_y, _max_y)

    def default(*self):
        return Pos2(0, 0)

    def __str__(self):
        return str((self.x, self.y))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)


class Vec2():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def clump(self, _min_x, _min_y, _max_x, _max_y):
        self.x = clump(self.x, _min_x, _max_x)
        self.y = clump(self.y, _min_y, _max_y)

    def default(*self):
        return Vec2(0, 0)

    def length(*self) -> float:
        return (self.x**2 + self.y**2) ** (1/2)

    def __str__(self):
        return str((self.x, self.y))
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)