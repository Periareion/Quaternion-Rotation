
from quaternion import *
from qarray import QArray

import pygame
clock = pygame.time.Clock()
FPS = 60

scale = 250
WIDTH, HEIGHT = 800, 600

COLORS = {
    'RED': pygame.Color(255,0,0),
    'GREEN': pygame.Color(0,255,0),
    'BLUE': pygame.Color(0,0,255),
    'WHITE': pygame.Color(255,255,255),
    'BLACK': pygame.Color(0,0,0),
}

color_loop = ['RED', 'GREEN', 'BLUE']

def screen_position(q=Q()):
    x = WIDTH/2 + scale * q.i
    y = HEIGHT/2 - scale * q.j
    return x, y

def main():

    rotation_vectors = QArray([
        Q(i=1),
        #Q(j=1),
    ])

    unit_vectors = QArray([
        Q(i=1), Q(j=1), Q(k=1),
    ])

    RPM = 10

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('You spin me right round')
    pygame.display.set_icon(pygame.image.load('icon.png'))

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    rotation_vectors += Q(i=0.1)
                elif event.key == pygame.K_j:
                    rotation_vectors += Q(i=-0.1)
                elif event.key == pygame.K_i:
                    rotation_vectors += Q(j=0.1)
                elif event.key == pygame.K_k:
                    rotation_vectors += Q(j=-0.1)
                elif event.key == pygame.K_h:
                    rotation_vectors += Q(k=0.1)
                elif event.key == pygame.K_n:
                    rotation_vectors += Q(k=-0.1)

        screen.fill(COLORS['BLACK'])

        for v in rotation_vectors.array:
            unit_vectors.rotate(v/len(rotation_vectors), 2*math.pi * RPM / 60 / FPS)

        for q in rotation_vectors.array:
            pygame.draw.line(screen, COLORS['WHITE'], screen_position(-q), screen_position(q), 3)

        for n, q in enumerate(unit_vectors.array):
            
            color = COLORS[color_loop[n % len(color_loop)]]
            
            pygame.draw.line(screen, color, screen_position(origin), screen_position(q), 2)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
