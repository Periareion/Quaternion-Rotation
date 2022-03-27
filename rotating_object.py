
import sys, os
import math
from copy import copy, deepcopy

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from shapes import *
from draw_utils import *
from color import *

from quaternion import *
from qarray import *
from vector import Vec

class RCS(SquarePyramid):

    def __init__(self, root_position=(0,0,0), direction=i, keys=None, thrust=16, size=(0.05,0.03,0.03), color=Color(10,10,10)):
        self.root_position = Q(0, *root_position)
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
            # Xa
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
        print(self.mass)

    def apply_force(self, position, direction, force):
        force_vector = direction.normalized * force
        self.velocity_vector += force_vector.axis_transform(*self.unit_vectors) / self.mass / FPS

        self.rotational_axis += (((position - self.center_of_mass)*force_vector).vector(True)).axis_transform(*self.unit_vectors) / self.mass / FPS
        #arm = position - self.center_of_mass
        #perpendicular_force = (arm*force_vector).vector(True)*arm
        #angular_acceleration = perpendicular_force / arm / self.mass
        #self.rotational_axis += angular_acceleration.axis_transform(*self.unit_vectors) / FPS

    def update(self):
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

        self.position = tuple((self.position[index]+(self.velocity_vector/FPS).components[1:4][index] for index in range(3)))
        self.unit_vectors.rotate(self.rotational_axis, self.rotational_axis.norm / FPS)

    def draw(self):
        self.update()

        for part in self.parts:
            if isinstance(part, Cuboid):
                Polyhedron(part, self.position, self.unit_vectors).render()
            elif isinstance(part, RCS):
                Polyhedron(part, self.position, self.unit_vectors).render()
                if part.active:
                    Polyhedron(RCS_Exhaust((part.root_position+part.thrust_point).vector(), part.direction), self.position, self.unit_vectors).render()

def main():

    unit_vectors = deepcopy(UNIT_QUATERNIONS)
    
    clock = pygame.time.Clock()
    global FPS
    FPS = 60

    width, height = 800, 600

    screen = pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
    pygame.display.set_caption('You spin me right round')
    pygame.display.set_icon(pygame.image.load('icon.png'))
        
    gluPerspective(60, width/height, 0.1, 50.0)
    glTranslatef(0, 0, -3)
    glRotatef(-60, 1, 0, 0)
    glRotatef(-30, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)  

    Thing = Body([0,0,0])
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Hello, World!")
                elif event.key == pygame.K_p:
                    print(Thing.position)
                elif event.key == pygame.K_v:
                    print(Thing.velocity_vector)


        glClearColor(*Color(24, 24, 24), 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Thing.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
      
##    diag = (i+j+k)#.normalized
##    cube = Cuboid(color=Color(50,50,50))

##        unit_vectors.rotate(i+j+k, math.pi/180)
##
##        for index, q in enumerate(unit_vectors.array):
##            draw_line((0,0,0), (q.i, q.j, q.k), COLORS[['RED', 'GREEN', 'BLUE'][index % 3]], 4)
##
##        diag_prime = diag.axis_transform(*unit_vectors.array)
##        draw_line((0,0,0), diag_prime.components[1:4], COLORS['WHITE'])
##        draw_cube(cube, unit_vectors, (0.5,0.5,0.5))

        #Thing.unit_vectors.rotate(i+k, math.pi/180)