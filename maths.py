from math import atan
# Константы
FPS = 120
DELTA = 1/60 # Время обработки одного кадра

def clump(value, _min, _max):
    return max(_min, min(_max, value))

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

class Size2():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def default(*self):
        return Size2(0, 0)

    def __str__(self):
        return str((self.width, self.height))

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

    def length(self) -> float:
        return (self.x**2 + self.y**2) ** (1/2)

    def to(self, pos: Pos2):
        return Vec2(self.x - pos.x, self.y - pos.y)

    def __str__(self):
        return str((self.x, self.y))
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, value: float):
        return Vec2(self.x * value, self.y * value)

class Rot2():
    def __init__(self, angle: float):
        self.angle = 0

    def __add__(self, value: float):
        return Rot2(self.angle + value)

    def __str__(self):
        return str(self.angle)

    def default(*self):
        return Rot2(0)

class Transform():
    def __init__(self, pos: Pos2, size: Size2 = Size2.default(), rotation: Rot2 = Rot2.default()):
        self.position = pos
        self.size = size
        self.rotation = rotation
    
    def rotate(angle: float):
        self.rotation += angle
    
    def __str__(self):
        return str((self.position.x, self.position.y, self.size.width, self.size.height, self.rotation.angle))
    
    def __add__(self, other):
        return Transform(self.position + other.position, Size2.default(), self.rotation + other.rotation.angle)