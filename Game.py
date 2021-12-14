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
        bg = [pygame.image.load(f"assets/Backgrounds/TestBackground/{b}.png").convert_alpha() for b in ['0', '1', '2']]
        self.background = [pygame.transform.scale2x(pygame.transform.scale2x(b)) for b in bg]

        self.level = LevelRendering.Level.load("Levels/Island.m2l", 32)

        self.camera_pos = [0, 0]

        pt = pygame.image.load("assets/sprites/player/idle_01.png")
        player_tex = pygame.transform.scale2x(pt)
        self.player = Player(player_tex, self.level)
        self.player.rect = pygame.Rect(0, 0, 64, 96)
        self.player.x, self.player.y = 800, 500
        self.player.game_y = -500

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
        # self.particles.tick()
        self.player.update()
        self.camera_pos[0] += (self.player.game_x - self.camera_pos[0]) / 8
        self.camera_pos[1] += (self.player.game_y - self.camera_pos[1]) / 8
        return 1

    def render(self):
        self.window.screen.fill((0, 0, 0))
        fps = round(self.clock.get_fps())
        self.window.screen.blit(self.background[0], (0, 0))
        self.window.screen.blit(self.background[1], ((self.camera_pos[0] + 1600) * -0.2, (self.camera_pos[1] + 960) * -0.2))
        self.window.screen.blit(self.background[2], ((self.camera_pos[0] + 800) * -0.5, (self.camera_pos[1] + 1600) * -0.2))
        self.window.screen.blit(self.level_im, (-self.camera_pos[0], -self.camera_pos[1]))
        pos = (self.player.game_x - self.camera_pos[0] + 800, self.player.game_y - self.camera_pos[1] + 480)
        im = self.player.get_image()
        self.window.screen.blit(im, (pos[0] - self.player.rect.w / 2 - 35, pos[1] - self.player.rect.h / 2))
        # self.window.screen.blit(self.particles.render(), (-self.player.game_x, -(self.player.game_y + 480)))
        try:
            self.window.screen.blit(self.font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))
        except pygame.error:
            pass  # idfk dude it works it just sends some errors

        return 1
