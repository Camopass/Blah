import sys
import pygame

from DebugScreen import DebugScreen
from Engine import LevelRendering
from Engine.Entity import Entity
from Engine.EntityManager import EntityManager
from Engine.ObjectManager import ObjectManager
from Engine.UserInterface import UIElement
from Engine.Window import Window
from Player import Player

pygame.init()

pygame.joystick.init()

player_level = ()

window = Window(1600, 960, "Slimey Man go wee wooo")

bg = pygame.image.load("assets/Backgrounds/Testing.png")
background = pygame.transform.scale(bg, (1600, 960))

pt = pygame.image.load("assets/sprites/player/idle_01.png")
player_tex = pygame.transform.scale2x(pt)
player = Player(player_tex)
player.set_center(window.screen.get_width() / 2, window.screen.get_height() / 2)

entity_manager = EntityManager(window.screen, player)
window.entity_manager = entity_manager
object_manager = ObjectManager(window.screen)

clock = pygame.time.Clock()

font = pygame.font.Font("assets/fonts/vcr.ttf", 20)

global use_gamepad  # Global Variables? CRINGE!
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
use_gamepad = True if len(joysticks) > 0 else False  # TODO: Make this stupid script better

debug_screen = DebugScreen(window, 900, 10, 275, 700, 'Debug Screen', entity_manager)

ui = UIElement(pygame.image.load("assets/UI/Button.png").convert_alpha()).render(2, 2)
ui_im = pygame.transform.scale(ui, (ui.get_width() * 10, ui.get_height() * 10))


def do_input(controlled_player):
    if use_gamepad:
        x = joysticks[0].get_axis(0)
        y = joysticks[0].get_axis(1)
        if abs(x) > 0.1:
            controlled_player.xvel += x
        if abs(y) > 0.1:
            controlled_player.yvel += y
        if joysticks[0].get_button(6):
            debug_screen.toggle_open()
    else:
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            controlled_player.xvel -= 1
        if key[pygame.K_d]:
            controlled_player.xvel += 1
        if key[pygame.K_w]:
            controlled_player.yvel -= 1
        if key[pygame.K_s]:
            controlled_player.yvel += 1
        if key[pygame.K_b]:
            debug_screen.toggle_open()


level = LevelRendering.Level.load("Levels/Stuff.m2l", 32)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Get it? Sus?
            if event.type == pygame.VIDEORESIZE:  # We do a little resizing
                window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
                window.update_resize()  # Set the scaling of the window screen
            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse moment
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = True
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = True
                window.mouse_down(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = False
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = False
                window.mouse_up(event.button)
            if event.type == pygame.KEYDOWN:  # Fullscreen by pressing F11
                if event.key == pygame.K_F11:
                    window.windowed() if window.is_fullscreen else window.fullscreen()

        if pygame.mouse.get_focused():
            window.screen.fill((0, 0, 0))

            fps = round(clock.get_fps())

            do_input(player)  # Barf emoji

            # We do a little rendering
            entity_manager.update()
            object_manager.update()
            window.screen.blit(background, (0, 0))
            window.screen.blit(level.render(), (-player.game_x, -player.game_y))
            window.render_managers(entity_manager, object_manager)
            debug_screen.render()
            window.screen.blit(font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))
            pygame.draw.rect(window.screen, (255, 255, 255), player.rect, 2)

            window.screen.blit(ui_im, (500, 300))

            window.render()
            pygame.display.update()

            clock.tick(60)


if __name__ == '__main__':
    main()
