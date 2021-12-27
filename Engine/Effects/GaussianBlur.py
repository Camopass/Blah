import numpy
import typing
import pygame
import math

from numba import njit


def gaussian(x, a, b, c):
    return a * math.exp(-(((x - b) * (x - b))/2*(c*c)))


def normalize(l: typing.Union[list, numpy.ndarray]):
    s = l.sum()
    for i, x in enumerate(l):
        l[i] = x / s


@njit
def run_pixel_av(weight_map: typing.List[float], pixels: numpy.ndarray, radius: int):
    for


def gaussian_blur(image: pygame.Surface, radius: int):
    weight_map = [gaussian(x, 1.0, 0.0, 1.0) for x in range(-radius, radius+1)]
    normalize(weight_map)
    # print('weight_map', weight_map, 'sum', sum(weight_map))
    pixels = pygame.surfarray.array2d(image)
    run_pixel_av(weight_map, pixels, radius)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((800, 480))

    im = pygame.image.load('Testing.png').convert()
    gaussian_blur(im, 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        screen.blit(im, (0, 0))
        pygame.display.update()
