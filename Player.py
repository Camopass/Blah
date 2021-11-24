import pygame

from Engine.Entity import Entity
from Engine.Entity.Animations import Animation
from Engine.Physics import level_as_rect_list, rect_tile_collide


class Player(Entity):
    def __init__(self, image, level):
        super().__init__("Player", "player", image)
        self.max_health = 5
        self.health = 5
        self.level = level
        self.collisions = [[], {'top': False, 'bottom': False, 'left': False, 'right': False}]
        self.run_animation = Animation('E:/Games/Slime/assets/sprites/player/run.json', 2)
        self.idle_animation = Animation('E:/Games/Slime/assets/sprites/player/blah.json', 2)
        self.last_ticks = pygame.time.get_ticks()

    def get_image(self):
        if abs(self.xvel) > 0.1:
            im = self.run_animation.get_image(pygame.time.get_ticks(), (1))
        else:
            im = self.idle_animation.get_image(pygame.time.get_ticks(), (11 - abs(self.xvel + 0.01)))
        if self.xvel < 0:
            im = pygame.transform.flip(im, True, False)
        return im

    def render(self, screen):
        screen.blit(self.get_image(), (self.rect.x - 17, self.rect.y - 17))

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
            # if tile not in collided_rects:
            #    collided_rects += tile
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
            # if tile not in collided_rects:
            #     collided_rects += tile

        self.game_x += (rect.x - self.rect.x) #/ pygame.time.get_ticks() - self.last_ticks
        self.game_y += (rect.y - self.rect.y) #/ pygame.time.get_ticks() - self.last_ticks
        self.last_ticks = pygame.time.get_ticks()

        if not collision_types['bottom']:
            self.yvel += 2

        if collision_types['top'] and not collision_types['bottom']:
            self.yvel = (self.yvel + 0.1) * -0.7

        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9

        self.collisions = collided_rects, collision_types
