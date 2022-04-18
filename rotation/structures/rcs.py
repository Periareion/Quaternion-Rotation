
from ..qmath import *

from .shapes import *

class RCS(SquarePyramid):

    def __init__(self, root_position=(0,0,0), direction=i, triggers=None, regressive=False, thrust=36, size=(0.05,0.03,0.03), color=Color(10,10,10)):
        super().__init__(root_position)
        
        self.direction = direction
        self.triggers = triggers
        self.regressive = regressive
        self.size = size
        self.color = color
        
        dimensional_morph = (self.size[0]*i, self.size[1]*j, self.size[2]*k)
        self.QVertices = QArray(list([Q(0, *v).axis_transform(*dimensional_morph).axis_transform(direction, direction.axis_transform(j, k, i), direction.axis_transform(k, i, j)) for v in self.vertices]))
        self.thrust_point = sum(self.QVertices[1:5])/3
        self.thrust = thrust
        self.mass = 10**-9
        
        self.exhaust = RCS_Exhaust
        self.active = False
        
        
class RCS_Exhaust(SquarePyramid):

    def __init__(self, root_position=(0,0,0), direction=i, size=(0.15,0.05,0.05), color=Color(200,200,200)):
        self.root_position = Q(root_position)
        self.direction = direction
        self.size = size
        dimensional_morph = (self.size[0]*i, self.size[1]*j, self.size[2]*k)
        self.QVertices = QArray(list([Q(0, *v).axis_transform(*dimensional_morph).axis_transform(direction, direction.axis_transform(j, k, i), direction.axis_transform(k, i, j)) for v in self.vertices]))
        self.color = color
