import math
import pygame

from Engine.LevelRendering import Level


class CollideInfo:
    def __init__(self, index, tile, x, y):
        self.index = index
        self.tile = tile
        self.x = x
        self.y = y
        self.pos = x, y


def debug_rect(rect, surface):
    pygame.draw.rect(surface, (255, 255, 255), rect, 3)


def debug_point(center, surface):
    pygame.draw.circle(surface, (100, 255, 100), center, 3)


def level_as_rect_list(level, scaling, pos):
    tile_size = level.tile_size * scaling
    rects = []
    for i, tile in enumerate(level.floor_pieces):
        xy = (i % level.length, i // level.length)
        rects.append((pygame.Rect(xy[0] * tile_size + pos[0], xy[1] * tile_size + pos[1], tile_size, tile_size), tile))
    return rects


def tile_index_to_rect(pos: int, level: Level, scaling: float, lpos: tuple):
    xy = ((pos % level.length) * scaling, int(pos // level.length) * scaling)
    sp = (xy[0] + lpos[0], xy[1] + lpos[1])
    return pygame.Rect(*sp, level.tile_size * scaling, level.tile_size * scaling)


def rect_tile_collide(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list
