import pygame

from pygame import mixer

from Engine.Scene import Scene
from Engine import LevelRendering
from Engine.EntityManager import EntityManager
from Engine.ObjectManager import ObjectManager

from Player import Player

if not pygame.mixer.get_init():
    pygame.mixer.init()


class Game(Scene):
    def setup(self):
        bg = pygame.image.load("assets/Backgrounds/Testing.png")
        self.background = pygame.transform.scale(bg, (1600, 960))

        self.level = LevelRendering.Level.load("Levels/long.m2l", 32)

        pt = pygame.image.load("assets/sprites/player/idle_01.png")
        player_tex = pygame.transform.scale2x(pt)
        self.player = Player(player_tex, self.level)
        self.player.rect = pygame.Rect(0, 0, 64, 96)
        self.player.x, self.player.y = 800, 500
        self.player.game_y = -500

        self.entity_manager = EntityManager(self.window.screen, self.player)
        self.object_manager = ObjectManager(self.window.screen)

        self.level_im = pygame.transform.scale2x(self.level.render())

        self.font = pygame.font.Font("assets/fonts/ComicMono.ttf", 20)

    def do_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.player.xvel -= 1
        if key[pygame.K_d]:
            self.player.xvel += 1
        if key[pygame.K_w] and self.player.collisions[1]['bottom']:
            self.player.yvel -= 50
        if key[pygame.K_s]:
            self.player.yvel += 1

    def tick(self):
        self.do_input()  # Barf emoji
        #self.object_manager.update()
        self.entity_manager.update()

    def render(self):
        self.window.screen.fill((0, 0, 0))
        fps = round(self.clock.get_fps())
        self.window.screen.blit(self.background, (0, 0))
        self.window.screen.blit(self.level_im, (-self.player.game_x, -self.player.game_y))
        self.window.render_managers(self.entity_manager, self.object_manager)
        self.window.screen.blit(self.font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))
