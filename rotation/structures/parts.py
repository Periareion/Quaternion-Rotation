
from ..qmath import *

from .rcs import *

class CompositePart:

    def __init__(self, subparts=[], root_position=(0,0,0), unit_vectors=None):

        if unit_vectors is None:
            unit_vectors = UNIT_QUATERNIONS.copy()
        self.unit_vectors = unit_vectors

        self.root_position = Q(root_position)

        self.subparts = subparts
        self.mass = sum([sp.mass for sp in self.subparts])


class DockingPort(CompositePart):

    def __init__(self, root_position=(0,0,0), unit_vectors=None):
        super().__init__(
            [
                Cuboid((0,0,0), size=(0.5, 0.5, 0.05), color=Color(80,80,80)),
                Cuboid((0,0,0.05), size=(0.4, 0.4, 0.05), color=Color(120,120,120)),
            ],
            root_position,
            unit_vectors,
        )
        

"""
from .rcs import *

class RCS(Part):

    def __init__(self, root_position=(0,0,0), direction=i, keys=None, thrust=36):

        super().__init__([
            [RCS_Engine(subpart_root_position=(0,0,0), direction=direction)], root_position, None
        ])

        self.keys = keys
        self.mass = 10**-9
        self.thrust = thrust

        self.active = False
        self.exhaust = RCS_Exhaust
"""