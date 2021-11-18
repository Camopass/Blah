import math

import bottom as bottom
import pygame
import tile as tile

from Engine.LevelRendering import Level


def debug_rect(rect, surface):
    pygame.draw.rect(surface, (255, 255, 255), rect, 3)


def debug_point(center, surface):
    pygame.draw.circle(surface, (255, 255, 255), center, 3)


def collision_ground(rect: pygame.Rect, level: Level, level_scaling: int, level_screen_pos, window):
    """-1: Error, 0: Floating, 1: Resting, 2: In ground"""
    debug_rect(rect, window.screen)
    tile_size = level.tile_size * level_scaling
    nt = level.get_null_tile()

    pixel_pos = [rect.x - level_screen_pos[0], rect.y - level_screen_pos[1]]
    pos = [math.floor(pixel_pos[0] / tile_size), math.floor(pixel_pos[1] / tile_size)]
    top_left = pos[1] * level.length + pos[0]
    debug_rect(pygame.Rect(pos[0] * tile_size + level_screen_pos[0], pos[1] * tile_size + level_screen_pos[1], tile_size, tile_size), window.screen)

    pp2 = [(rect.x + rect.w) - level_screen_pos[0], (rect.y + rect.h) - level_screen_pos[1]]
    p2 = [math.floor(pp2[0] / tile_size), math.floor(pp2[1] / tile_size)]
    bottom_right = p2[1] * level.length + p2[0]
    debug_rect(pygame.Rect(p2[0] * tile_size + level_screen_pos[0], p2[1] * tile_size + level_screen_pos[1], tile_size, tile_size), window.screen)
