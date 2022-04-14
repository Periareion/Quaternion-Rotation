
import math

from ..graphics import Color

from ..qmath import *

class Cuboid:

    vertices = (
        (-1, -1, -1),
        (-1, -1, 1),
        (-1, 1, -1),
        (-1, 1, 1),
        (1, -1, -1),
        (1, -1, 1),
        (1, 1, -1),
        (1, 1, 1),
    )

    edges = (
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        (0, 2),
        (1, 3),
        (4, 6),
        (5, 7),
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),
    )

    faces = (
        (0, 1, 3, 2),
        (0, 4, 5, 1),
        (0, 4, 6, 2),
        (7, 5, 4, 6),
        (7, 6, 2, 3),
        (7, 3, 1, 5),
    )

    def __init__(self, root_position=(0,0,0), size=(0.2,0.2,0.2), color=Color(50,50,50), density=1000):
        self.root_position = Q(root_position)
        self.size = size
        self.color = color
        self.volume = math.prod(size)
        self.mass = self.volume*density
        self.QVertices = QArray([0.5*Q(0, *vertex).axis_transform(self.size[0]*i, self.size[1]*j, self.size[2]*k) for vertex in self.vertices])

class SquarePyramid:

    vertices = (
        (-1, 0, 0),
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, -1),
        (1, -1, 1),
    )

    edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
    )

    faces = (
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
        (0, 4, 1),
        (1, 2, 3, 4),
    )

    def __init__(self, root_position):
        self.root_position = Q(root_position)