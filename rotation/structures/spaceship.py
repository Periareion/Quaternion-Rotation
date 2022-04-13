

from copy import deepcopy

import pygame

from ..graphics.draw_utils import *
from ..graphics.color import *

from ..qmath import *

from .shapes import *

class RCS(SquarePyramid):

    def __init__(self, root_position=(0,0,0), direction=i, keys=None, thrust=36, size=(0.05,0.03,0.03), color=Color(10,10,10)):
        super().__init__(root_position)
        self.direction = direction
        self.keys = keys
        self.size = size
        dimensional_morph = (self.size[0]*i, self.size[1]*j, self.size[2]*k)
        self.QVertices = QArray(list([Q(0, *v).axis_transform(*dimensional_morph).axis_transform(direction, direction.axis_transform(j, k, i), direction.axis_transform(k, i, j)) for v in self.vertices]))
        self.thrust_point = sum(self.QVertices[1:5])/3
        self.mass = 10**-9
        self.thrust = thrust
        self.color = color
        
        self.active = False

class Body:

    def __init__(self, position):
        self.unit_vectors = deepcopy(UNIT_QUATERNIONS)

        self.velocity_vector = Q()
        self.rotational_axis = Q(0,0.3,0,0)
        
        self.position = position
        self.parts = [
            #Cuboid(root_position=(0,0,0), size=(0.1,0.1,0.1), color=Color(150,150,150)),
            # X
            Cuboid(root_position=(0.45,0,0), size=(0.8,0.1,0.1), color=Color(150,24,24)),
            Cuboid(root_position=(0.9,0,0), size=(0.1,0.2,0.2), color=Color(100,100,100)),
            RCS((0.9,0,0.1), direction=k, color=Color(10,10,10), keys=[pygame.K_k, pygame.K_e, pygame.K_LSHIFT]),
            RCS((0.9,0,-0.1), direction=-k, color=Color(10,10,10), keys=[pygame.K_i, pygame.K_q, pygame.K_LSHIFT]),
            RCS((0.9,0.1,0), direction=j, color=Color(10,10,10), keys=[pygame.K_n, pygame.K_d]),
            RCS((0.9,-0.1,0), direction=-j, color=Color(10,10,10), keys=[pygame.K_h, pygame.K_a]),

            # -X
            Cuboid(root_position=(-0.45,0,0), size=(0.8,0.1,0.1), color=Color(50,15,15)),
            Cuboid(root_position=(-0.9,0,0), size=(0.1,0.2,0.2), color=Color(100,100,100)),
            RCS((-0.9,0,0.1), direction=k, color=Color(10,10,10), keys=[pygame.K_k, pygame.K_q, pygame.K_LSHIFT]),
            RCS((-0.9,0,-0.1), direction=-k, color=Color(10,10,10), keys=[pygame.K_i, pygame.K_e, pygame.K_LSHIFT]),
            RCS((-0.9,0.1,0), direction=j, color=Color(10,10,10), keys=[pygame.K_n, pygame.K_a]),
            RCS((-0.9,-0.1,0), direction=-j, color=Color(10,10,10), keys=[pygame.K_h, pygame.K_d]),

            # Y
            Cuboid(root_position=(0,0.45,0), size=(0.1,0.8,0.1), color=Color(24,150,24)),
            Cuboid(root_position=(0,0.9,0), size=(0.2,0.1,0.2), color=Color(100,100,100)),
            RCS((0.1,0.9,0), direction=i, color=Color(10,10,10), keys=[pygame.K_j, pygame.K_a, pygame.K_LSHIFT]),
            RCS((-0.1,0.9,0), direction=-i, color=Color(10,10,10), keys=[pygame.K_l, pygame.K_d, pygame.K_LSHIFT]),
            RCS((0,0.9,0.1), direction=k, color=Color(10,10,10), keys=[pygame.K_k, pygame.K_w]),
            RCS((0,0.9,-0.1), direction=-k, color=Color(10,10,10), keys=[pygame.K_i, pygame.K_s]),

            # -Y
            Cuboid(root_position=(0,-0.45,0), size=(0.1,0.8,0.1), color=Color(15,50,15)),
            Cuboid(root_position=(0,-0.9,0), size=(0.2,0.1,0.2), color=Color(100,100,100)),
            RCS((0.1,-0.9,0), direction=i, color=Color(10,10,10), keys=[pygame.K_j, pygame.K_d, pygame.K_LSHIFT]),
            RCS((-0.1,-0.9,0), direction=-i, color=Color(10,10,10), keys=[pygame.K_l, pygame.K_a, pygame.K_LSHIFT]),
            RCS((0,-0.9,0.1), direction=k, color=Color(10,10,10), keys=[pygame.K_k, pygame.K_s]),
            RCS((0,-0.9,-0.1), direction=-k, color=Color(10,10,10), keys=[pygame.K_i, pygame.K_w]),

            # Z
            Cuboid(root_position=(0,0,0.45), size=(0.1,0.1,0.8), color=Color(24,24,150)),
            Cuboid(root_position=(0,0,0.9), size=(0.2,0.2,0.1), color=Color(100,100,100)),
            RCS((0.1,0,0.9), direction=i, color=Color(10,10,10), keys=[pygame.K_j, pygame.K_q]),
            RCS((-0.1,0,0.9), direction=-i, color=Color(10,10,10), keys=[pygame.K_l, pygame.K_e]),
            RCS((0,0.1,0.9), direction=j, color=Color(10,10,10), keys=[pygame.K_n, pygame.K_s, pygame.K_LSHIFT]),
            RCS((0,-0.1,0.9), direction=-j, color=Color(10,10,10), keys=[pygame.K_h, pygame.K_w, pygame.K_LSHIFT]),

            # -Z
            Cuboid(root_position=(0,0,-0.45), size=(0.1,0.1,0.8), color=Color(15,15,50)),
            Cuboid(root_position=(0,0,-0.9), size=(0.2,0.2,0.1), color=Color(100,100,100)),
            RCS((0.1,0,-0.9), direction=i, color=Color(10,10,10), keys=[pygame.K_j, pygame.K_e]),
            RCS((-0.1,0,-0.9), direction=-i, color=Color(10,10,10), keys=[pygame.K_l, pygame.K_q]),
            RCS((0,0.1,-0.9), direction=j, color=Color(10,10,10), keys=[pygame.K_n, pygame.K_w, pygame.K_LSHIFT]),
            RCS((0,-0.1,-0.9), direction=-j, color=Color(10,10,10), keys=[pygame.K_h, pygame.K_s, pygame.K_LSHIFT]),
        ]

        self.mass = sum([part.mass for part in self.parts])
        self.center_of_mass = sum((part.root_position*(part.mass/self.mass) for part in self.parts))

    def apply_force(self, position, direction, force, delta_time=1/60):
        force_vector = direction.normalized * force
        self.velocity_vector += force_vector.axis_transform(*self.unit_vectors) / self.mass * delta_time

        #self.rotational_axis += (((position - self.center_of_mass)*force_vector).vector(True)).axis_transform(*self.unit_vectors) / self.mass * delta_time

        arm = position - self.center_of_mass
        perpendicular_force = arm.inverse * (arm*force_vector).vector(True)
        angular_acceleration = arm * perpendicular_force / self.mass
        self.rotational_axis += angular_acceleration.axis_transform(*self.unit_vectors) * delta_time

    def update(self, delta_time=1/60):
        key_presses = pygame.key.get_pressed()
        for part in self.parts:
            if isinstance(part, RCS):
                if part.keys == None:
                    continue
                if key_presses[pygame.K_LSHIFT] and pygame.K_LSHIFT not in part.keys:
                    part.active = False
                elif not part.active and True in [key_presses[key] for key in part.keys if key != pygame.K_LSHIFT]:
                    part.active = True
                elif part.active and True not in [key_presses[key] for key in part.keys if key != pygame.K_LSHIFT]:
                    part.active = False

                if part.active:
                    self.apply_force(part.root_position+part.thrust_point, -part.direction, part.thrust)

        self.position = tuple((self.position[index]+(self.velocity_vector*delta_time).components[1:4][index] for index in range(3)))
        self.unit_vectors.rotate(self.rotational_axis, self.rotational_axis.norm*delta_time)

        self.draw()

    def draw(self):

        for part in self.parts:
            if isinstance(part, Cuboid):
                Polyhedron(part, self.position, self.unit_vectors).render()
            elif isinstance(part, RCS):
                Polyhedron(part, self.position, self.unit_vectors).render()
                if part.active:
                    Polyhedron(RCS_Exhaust((part.root_position+part.thrust_point).vector(), part.direction), self.position, self.unit_vectors).render()