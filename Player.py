import pygame

from Engine.Entity import Entity
from Engine.Physics import level_as_rect_list, rect_tile_collide, debug_rect


class Player(Entity):
    def __init__(self, image, level):
        super().__init__("Player", "player", image)
        self.max_health = 5
        self.health = 5
        self.level = level
        self.collisions = [[], {'top': False, 'bottom': False, 'left': False, 'right': False}]
        # self.animation = Animation() # TODO: Add animations you dumbs

    def update(self):
        rect_level = level_as_rect_list(self.level, 2, (-self.game_x, -self.game_y))

        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        collided_rects = []

        rect = self.rect.copy()

        rect.x += self.xvel
        hit_list = rect_tile_collide(rect, rect_level)
        for tile in hit_list:
            if tile[1] == 0:
                continue
            if self.xvel > 0:
                rect.right = tile[0].left
                collision_types['right'] = True
            elif self.xvel < 0:
                rect.left = tile[0].right
                collision_types['left'] = True
            if tile not in collided_rects:
                collided_rects += tile
        rect.y += self.yvel
        hit_list = rect_tile_collide(rect, rect_level)
        for tile in hit_list:
            if tile[1] == 0:
                continue
            if self.yvel > 0:
                rect.bottom = tile[0].top
                collision_types['bottom'] = True
            if self.yvel < 0:
                rect.top = tile[0].bottom
                collision_types['top'] = True
            if tile not in collided_rects:
                collided_rects += tile

        self.game_x += (rect.x - self.rect.x)
        self.game_y += (rect.y - self.rect.y)

        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9

        self.collisions = collided_rects, collision_types
