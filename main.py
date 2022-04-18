
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from rotation import *

def main(width=1000, height=800, FPS=60):

    screen = pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
    pygame.display.set_caption('You spin me right round')
    pygame.display.set_icon(pygame.image.load('icon.png'))

    time = 0
    delta_time = 1/FPS
    
    clock = pygame.time.Clock()
        
    gluPerspective(60, width/height, 0.1, 50.0)
    glTranslatef(0, 0, -4)
    glRotatef(-70, 1, 0, 0)
    glRotatef(-30, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    cross_structure = Cross([0,0,0])
    spaceship = Spaceship([0,0,0])
    docking_port = Station([-3, 0, 0])

    running = True
    while running:

        key_presses = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cross_structure.randomize(True, True, True, True)

        glClearColor(*Color(24, 24, 24), 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        cross_structure.update(delta_time, key_presses)
        #spaceship.update(delta_time)
        docking_port.update(delta_time)

        pygame.display.flip()
        time += delta_time
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
