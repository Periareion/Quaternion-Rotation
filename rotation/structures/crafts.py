
import math
import pygame

from ..graphics.draw_utils import *
from ..graphics.color import *

from ..qmath import *

from .parts import *
from .shapes import *

import random

pitch = 1
yaw = 2
roll = 3
x = 4
y = 5
z = 6

controls = [
    'pitch', 'yaw', 'roll',
    'x', 'y', 'z',
]

class Craft:

    def __init__(self, position, random_direction=False, random_rotation=False):

        self.position = position
        self.velocity_vector = Q()

        self.unit_vectors = UNIT_QUATERNIONS.copy()
        self.rotational_axis = Q(0,1,0,0)

        if not hasattr(self, 'parts'):
            self.parts = []

        self.update_mass()
        self.update_center()

        self.control = {
            'pitch': 0,
            'yaw': 0,
            'roll': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }

    def apply_force(self, position, direction, force, delta_time=1/60):
        force_vector = direction.normalized * force
        self.velocity_vector += force_vector.axis_transform(*self.unit_vectors) / self.mass * delta_time

        arm = position - self.center_of_mass
        perpendicular_force = arm.inverse * (arm*force_vector).vector(True)
        angular_acceleration = arm * perpendicular_force / self.mass
        self.rotational_axis += angular_acceleration.axis_transform(*self.unit_vectors) * delta_time

    def update_mass(self):
        self.mass = sum((part.mass for part in self.parts))
        self.center_of_mass = sum((part.root_position*(part.mass/self.mass) for part in self.parts))
    
    def update_center(self):
        for part in self.parts:
            part.root_position = Q(part.root_position) - self.center_of_mass

    def randomize(self, direction=False, rotation=False, position=False, velocity=False):
        if direction:
            self.unit_vectors.rotate(Q(0,random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)), random.uniform(0,math.tau))
        if rotation:
            self.rotational_axis = Q(0,random.uniform(-0.5,0.5),random.uniform(-0.5,0.5),random.uniform(-0.5,0.5)).normalized
        if position:
            self.position = [random.uniform(-0.5,0.5),random.uniform(-0.5,0.5),random.uniform(-0.5,0.5)]
        if velocity:
            self.velocity_vector = Q(0,random.uniform(-0.1,0.1),random.uniform(-0.1,0.1),random.uniform(-0.1,0.1)).normalized

    def update(self, delta_time=1/60, key_presses=None):

        if key_presses is not None:
            self.control['pitch'] = key_presses[pygame.K_s] - key_presses[pygame.K_w]
            self.control['yaw'] = key_presses[pygame.K_d] - key_presses[pygame.K_a]
            self.control['roll'] = key_presses[pygame.K_e] - key_presses[pygame.K_q]
            self.control['x'] = key_presses[pygame.K_l] - key_presses[pygame.K_j]
            self.control['y'] = key_presses[pygame.K_i] - key_presses[pygame.K_k]
            self.control['z'] = key_presses[pygame.K_h] - key_presses[pygame.K_n]

        # autopilot target

        for part in self.parts:
            if isinstance(part, RCS):
                if part.regressive and key_presses[pygame.K_LSHIFT]:
                    part.active = False
                    continue
                if True in [self.control[controls[abs(trigger)-1]] == math.copysign(1, trigger) for trigger in part.triggers]:
                    part.active = True
                else:
                    part.active = False

                if part.active:
                    self.apply_force(part.root_position+part.thrust_point, -part.direction, part.thrust)

        self.position = tuple((self.position[index]+(self.velocity_vector*delta_time).components[1:4][index] for index in range(3)))
        self.unit_vectors.rotate(self.rotational_axis, self.rotational_axis.norm*delta_time)

        self.draw()

    def draw(self):

        for part in self.parts:
            if isinstance(part, CompositePart):
                for subpart in part.subparts:
                    Polyhedron(subpart, Q(self.position) + (part.root_position).axis_transform(*self.unit_vectors), self.unit_vectors).render()
            elif isinstance(part, Cuboid):
                Polyhedron(part, self.position, self.unit_vectors).render()
            elif isinstance(part, RCS):
                Polyhedron(part, self.position, self.unit_vectors).render()
                if part.active:
                    Polyhedron(part.exhaust((part.root_position+part.thrust_point).vector(), part.direction), self.position, self.unit_vectors).render()

class Cross(Craft):

    def __init__(self, position):

        self.parts = [
            #Cuboid((0,0,0), size=(0.1,0.1,0.1), color=Color(150,150,150)),
            # X # rev pitch yaw roll x y z
            Cuboid((0.45,0,0), size=(0.8,0.1,0.1), color=Color(150,24,24)),
            Cuboid((0.9,0,0), size=(0.1,0.2,0.2), color=Color(100,100,100)),
            RCS((0.9,0.1,0), direction=j, triggers=[-roll, -y]),
            RCS((0.9,-0.1,0), direction=-j, triggers=[roll, y]),
            RCS((0.9,0,0.1), direction=k, triggers=[yaw, -z], regressive=True),#
            RCS((0.9,0,-0.1), direction=-k, triggers=[-yaw, z], regressive=True),#

            # -X
            Cuboid((-0.45,0,0), size=(0.8,0.1,0.1), color=Color(50,15,15)),
            Cuboid((-0.9,0,0), size=(0.1,0.2,0.2), color=Color(100,100,100)),
            RCS((-0.9,0.1,0), direction=j, triggers=[roll, -y]),
            RCS((-0.9,-0.1,0), direction=-j, triggers=[-roll, y]),
            RCS((-0.9,0,0.1), direction=k, triggers=[-yaw, -z], regressive=True),#
            RCS((-0.9,0,-0.1), direction=-k, triggers=[yaw, z], regressive=True),#

            # Y
            Cuboid((0,0.45,0), size=(0.1,0.8,0.1), color=Color(24,150,24)),
            Cuboid((0,0.9,0), size=(0.2,0.1,0.2), color=Color(100,100,100)),
            RCS((0,0.9,0.1), direction=k, triggers=[-pitch, -z]),
            RCS((0,0.9,-0.1), direction=-k, triggers=[pitch, z]),
            RCS((0.1,0.9,0), direction=i, triggers=[roll, -x], regressive=True),#
            RCS((-0.1,0.9,0), direction=-i, triggers=[-roll, x], regressive=True),#

            # -Y
            Cuboid((0,-0.45,0), size=(0.1,0.8,0.1), color=Color(15,50,15)),
            Cuboid((0,-0.9,0), size=(0.2,0.1,0.2), color=Color(100,100,100)),
            RCS((0,-0.9,0.1), direction=k, triggers=[pitch, -z]),
            RCS((0,-0.9,-0.1), direction=-k, triggers=[-pitch, z]),
            RCS((0.1,-0.9,0), direction=i, triggers=[-roll, -x], regressive=True),#
            RCS((-0.1,-0.9,0), direction=-i, triggers=[roll, x], regressive=True),#

            # Z
            Cuboid((0,0,0.45), size=(0.1,0.1,0.8), color=Color(24,24,150)),
            Cuboid((0,0,0.9), size=(0.2,0.2,0.1), color=Color(100,100,100)),
            RCS((0.1,0,0.9), direction=i, triggers=[-yaw, -x]),
            RCS((-0.1,0,0.9), direction=-i, triggers=[yaw, x]),
            RCS((0,0.1,0.9), direction=j, triggers=[pitch, -y], regressive=True),#
            RCS((0,-0.1,0.9), direction=-j, triggers=[-pitch, y], regressive=True),#

            # -Z
            Cuboid((0,0,-0.45), size=(0.1,0.1,0.8), color=Color(15,15,50)),
            Cuboid((0,0,-0.9), size=(0.2,0.2,0.1), color=Color(100,100,100)),
            RCS((0.1,0,-0.9), direction=i, triggers=[yaw, -x]),
            RCS((-0.1,0,-0.9), direction=-i, triggers=[-yaw, x]),
            RCS((0,0.1,-0.9), direction=j, triggers=[-pitch, -y], regressive=True),#
            RCS((0,-0.1,-0.9), direction=-j, triggers=[pitch, y], regressive=True),#
        ]

        super().__init__(position=position)


class Spaceship(Craft):

    def __init__(self, position):

        u = UNIT_QUATERNIONS.copy()
        u.rotate((i + j + k).normalized, math.radians(60))
        print(u)

        self.parts = [
            Cuboid((0,0,0), size=(0.8, 0.8, 1.2), color=Color(220,220,220)),
            Cuboid((0,0,-1.4), size=(1,1,1.6), color=Color(180,180,180)),
            DockingPort((0,0,0.6), UNIT_QUATERNIONS.copy().rotate((i + j + k).normalized, math.radians(60))),
        ]

        super().__init__(position=position)


class Station(Craft):

    def __init__(self, position, vector=j, angle=math.radians(90)):

        self.parts = [
            DockingPort((0,0,0))
        ]

        super().__init__(position)

        self.unit_vectors.rotate(vector, angle)