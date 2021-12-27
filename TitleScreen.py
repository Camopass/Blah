import traceback

import pygame

from Engine.Scene import Scene
from Engine.UserInterface import Button
from Game import Game


class TitleScreen(Scene):
    def setup(self):
        self.background = pygame.transform.scale(
            pygame.image.load("assets/Backgrounds/TitleScreen.png").convert(), (1600, 960))
        self.font = pygame.font.Font("assets/fonts/ComicMono.ttf ", 65)
        # self.particles = Particles("assets/sprites/particles/leaves.png", 5).convert()
        image = pygame.image.load("assets/UI/ButtonSmall.png").convert_alpha()
        play_button = Button.uie_button(image, 9, 800, 500, 7, 3, image, self.font, self.window,
                                        scaling=10, text="PLAY", padding=15)

        def on_click(window):
            try:
                self.next_scene = Game(window, self.clock)
            except Exception as e:
                traceback.print_exc()
                print(e)

        play_button.on_click = on_click
        self.buttons = [play_button]
        self.music = pygame.mixer.music.load('assets/Music/Menu.ogg')
        pygame.mixer.music.play(0)

    def tick(self):
        # self.particles.tick()
        return 0

    def mouse_up(self, button):
        if button == pygame.BUTTON_LEFT:
            for button in self.buttons:
                if button.rect.collidepoint(self.window.get_mouse_pos()):
                    button.on_click(self.window)

    def render(self):
        self.window.screen.blit(self.background, (0, 0))
        self.window.screen.blit(self.font.render("BLAH", True, (150, 255, 175)), (800 - (self.font.size("BLAH")[0] / 2),
                                                                                  200 - (self.font.size("BLAH")[1] / 2)))
        for i, button in enumerate(self.buttons):
            b = button.render()
            pos = (800 - (b.get_width() / 2), (200 * (i + 2)) - (b.get_height() / 2))
            self.window.screen.blit(b, pos)
            button.rect.update((pos[0], pos[1], button.rect.w, button.rect.h))
            if button.rect.collidepoint(self.window.get_mouse_pos()):
                pygame.draw.rect(self.window.screen, (255, 255, 255), button.rect, 3)
        # self.particles.render(self.window.screen, (0, 0))

        return 0
