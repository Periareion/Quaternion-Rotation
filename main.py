
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from packages.graphics.shapes import *
from packages.graphics.draw_utils import *
from packages.graphics.color import *

from packages.qmath.quaternion import *
from packages.qmath.qarray import *
from packages.qmath.vector import Vec

from packages.spaceship.body import *

def main():
    
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

        glClearColor(*Color(24, 24, 24), 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Thing.update(FPS)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()