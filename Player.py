import pygame

from pygame import mixer

from Engine.Entity import Entity
from Engine.Entity.AnimationManager import AnimationManager, AnimationState
from Engine.Entity.Animations import Animation
from Engine.Physics import level_as_rect_list, rect_tile_collide

if not pygame.mixer.get_init():
    pygame.mixer.init()

mixer.set_num_channels(8)

land_snd = mixer.Sound("assets/Sounds/Blah/land.wav")


class Player(Entity):
    def __init__(self, image, level):
        super().__init__("Player", "player", image)
        self.max_health = 5
        self.health = 5
        self.level = level
        self.collisions = [[], {'top': False, 'bottom': False, 'left': False, 'right': False}]
        self.run_state = AnimationState(Animation('E:/Games/Slime/assets/sprites/player/run.json', 2), 'run')
        self.idle_state = AnimationState(Animation('E:/Games/Slime/assets/sprites/player/blah.json', 2), 'idle')
        self.animation_manager = AnimationManager(self.idle_state, self.run_state, self.idle_state)
        self.last_ticks = pygame.time.get_ticks()

    def get_image(self):
        im = self.animation_manager.get_frame()
        if self.xvel < 0:
            im = pygame.transform.flip(im, True, False)
        return im

    def render(self, screen):
        screen.blit(self.get_image(), (self.rect.x - 17, self.rect.y - 17))

    def update(self):
        rect_level = level_as_rect_list(self.level, 2, (-self.game_x, -self.game_y))

        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        collided_rects = []

//mister monkey! the poeple are rebelling!

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

        if collision_types['bottom'] and self.yvel > 16:
            land_snd.play()

        if collision_types['top'] and not collision_types['bottom']:
            self.yvel = (self.yvel + 0.1) * -0.7

        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9

        self.collisions = collided_rects, collision_types
