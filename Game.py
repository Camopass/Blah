import pygame
from pygame import mixer

from Engine.Scene import Scene
from Engine import LevelRendering
from Engine.EntityManager import EntityManager
from Engine.ObjectManager import ObjectManager
from Particles import Particles

from Player import Player


if not pygame.mixer.get_init():
    pygame.mixer.init()

jump_snd = mixer.Sound("assets/Sounds/Blah/jump.wav")


class Game(Scene):
    def setup(self):
        bg = pygame.image.load("assets/Backgrounds/Testing.png")
        self.background = pygame.transform.scale(bg, (1600, 960))

        self.level = LevelRendering.Level.load("Levels/Island.m2l", 32)

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

        im = pygame.image.load("assets/sprites/leaf.png").convert_alpha()
        im2 = pygame.image.load("assets/sprites/leaf2.png").convert_alpha()
        images = [pygame.transform.scale2x(im), pygame.transform.scale2x(im2)]
        self.particles = Particles(images, 700, (self.level_im.get_width(), self.level_im.get_height() + 960))

    def do_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.player.xvel -= 1
            self.player.animation_manager.add_animation(self.player.animation_manager.states[1])
        if key[pygame.K_d]:
            self.player.xvel += 1
        if key[pygame.K_w] and self.player.collisions[1]['bottom']:
            jump_snd.play()
            self.player.yvel -= 50
        if key[pygame.K_s]:
            self.player.yvel += 1

    def tick(self):
        self.do_input()  # Barf emoji
        self.particles.tick()
        self.entity_manager.update()
        return 1

    def render(self):
        self.window.screen.fill((0, 0, 0))
        fps = round(self.clock.get_fps())
        self.window.screen.blit(self.background, (0, 0))
        self.window.screen.blit(self.level_im, (-self.player.game_x, -self.player.game_y))
        self.window.render_managers(self.entity_manager, self.object_manager)
        self.window.screen.blit(self.particles.render(), (-self.player.game_x, -(self.player.game_y + 480)))
        try:
            self.window.screen.blit(self.font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))
        except pygame.error:
            pass  # idfk dude it works it just sends some errors

        return 1
