import random
import typing

import numpy as np
import pygame


# class Particle:
#     def __init__(self, im_index, pos, angle, index):
#         self.im_index = im_index
#         self.pos = list(pos)
#         self.angle = angle
#         self.index = index

# (im_ind, x, y, angle, index)

def update(particle, dimensions):
    particle[1] -= random.randint(4, 8)
    particle[2] += random.randint(4, 5)
    particle[3] += random.randint(-10, 10)
    if pygame.time.get_ticks() % 2 == 0:
        if particle[1] < 0 or particle[1] > dimensions[0]:
            particle[1] = random.randint(0, dimensions[0])
            particle[2] = 0
        if particle[2] < 0 or particle[2] > dimensions[1]:
            particle[1] = random.randint(0, dimensions[0])
            particle[2] = 0
    else:
        if particle[1] < 0 or particle[1] > dimensions[0]:
            particle[1] = dimensions[0]
            particle[2] = random.randint(0, dimensions[1])
        if particle[2] < 0 or particle[2] > dimensions[1]:
            particle[1] = dimensions[0]
            particle[2] = random.randint(0, dimensions[1])


class Particles:
    def __init__(self, images: typing.List[pygame.Surface], count: int, dimensions: typing.Tuple[int, int]):
        self.images = images
        self._count = count
        self.dimensions = dimensions
        self.particles = np.empty(count, list)

        for i in range(count):
            self.particles[i] = [random.randint(0, len(images) - 1), random.randint(0, dimensions[0]), random.randint(0, dimensions[1]), 0, i]

    def tick(self):
        for i, particle in enumerate(self.particles):
            update(particle, self.dimensions)

    def render(self, surface: pygame.Surface, screen_rect: pygame.Rect):
        for particle in self.particles:
            if screen_rect.collidepoint(particle[1:3]):
                if particle[3] == 0:
                    surface.blit(self.images[particle[0]], (particle[1] - screen_rect.x, particle[2] - screen_rect.y))
                else:
                    im = pygame.transform.rotate(self.images[particle[0]], particle[3])
                    surface.blit(im, (particle[1]-+ screen_rect.x, particle[2] - screen_rect.y))
