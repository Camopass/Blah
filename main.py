import datetime
import logging
import os
import time
import traceback
import sys

import pygame

from Engine.Window import Window
from TitleScreen import TitleScreen

pygame.init()

pygame.joystick.init()

if not pygame.mixer.get_init():
    pygame.mixer.init()

player_level = ()

window = Window(1600, 960, "Slimey Man go wee wooo", "assets/icons/16.png")

clock = pygame.time.Clock()


class Profiler:
    def __init__(self, thing):
        self.time = None
        self.thing = thing

    def __enter__(self):
        self.time = time.perf_counter()
        return self

    def close(self):
        logging.debug(f'{self.thing} was closed after {time.perf_counter() - self.time} seconds.')
        del self

    def __exit__(self, exc_type, exc_value, trace):
        logging.debug(f'{self.thing} took {time.perf_counter() - self.time} seconds to run.')
        return self


scene = TitleScreen(window, clock)


def main():
    global scene
    running = True
    while running:
        with Profiler("Frame Time") as p:
            with Profiler("Events"):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        p.close()
                        running = False
                    if event.type == pygame.VIDEORESIZE:  # We do a little resizing
                        window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
                        window.update_resize()  # Set the scaling of the window screen
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse moment
                        if event.button == pygame.BUTTON_RIGHT:
                            window.right_click = True
                        if event.button == pygame.BUTTON_LEFT:
                            window.left_click = True
                        window.mouse_down(event.button)
                        scene.mouse_down(event.button)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == pygame.BUTTON_RIGHT:
                            window.right_click = False
                        if event.button == pygame.BUTTON_LEFT:
                            window.left_click = False
                        window.mouse_up(event.button)
                        scene.mouse_up(event.button)
                    if event.type == pygame.KEYDOWN:  # Fullscreen by pressing F11
                        if event.key == pygame.K_F11:
                            window.windowed() if window.is_fullscreen else window.fullscreen()
                        if event.key == pygame.K_F12:
                            dir = os.environ["USERPROFILE"] + f"/Desktop/{datetime.date.today()}.png"
                            pygame.image.save(window.screen, dir)

            with Profiler("Tick"):
                try:
                    scene.tick()
                except Exception as e:
                    traceback.print_exc()
                    print(e)

            if scene.next_scene is not None:
                s = scene.next_scene
                del scene
                scene = s

            #if pygame.mouse.get_focused():
            with Profiler("Rendering"):
                try:
                    scene.render()
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                # pygame.draw.rect(window.screen, (255, 255, 255), player.rect, 3)
                window.render()
                pygame.display.update()

            clock.tick(60)
            # clock.tick(6000)
    sys.exit()


if __name__ == '__main__':
    main()
