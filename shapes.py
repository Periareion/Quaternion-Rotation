
import math

from quaternion import *
from qarray import *

from color import *

class Mesh:

    def __init__(self, root_position=(0,0,0)):
        self.root_position = Q(0, *root_position)

class Cuboid(Mesh):

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
        super().__init__(root_position=root_position)
        self.size = size
        self.color = color
        self.volume = math.prod(size)
        self.mass = self.volume*density
        self.QVertices = QArray([0.5*Q(0, *vertex).axis_transform(self.size[0]*i, self.size[1]*j, self.size[2]*k) for vertex in self.vertices])

class SquarePyramid(Mesh):

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
        super().__init__(root_position)
        
class RCS_Exhaust(SquarePyramid):

    def __init__(self, root_position=(0,0,0), direction=i, size=(0.15,0.05,0.05), color=Color(200,200,200)):
        super().__init__(root_position)
        self.direction = direction
        self.size = size
        dimensional_morph = (self.size[0]*i, self.size[1]*j, self.size[2]*k)
        self.QVertices = QArray(list([Q(0, *v).axis_transform(*dimensional_morph).axis_transform(direction, direction.axis_transform(j, k, i), direction.axis_transform(k, i, j)) for v in self.vertices]))
        self.color = color
