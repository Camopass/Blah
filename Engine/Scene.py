"""Base class for scenes. Setup is setup, tick does game updates, and render renders. Close is called before a new
scene is created. """
import pygame


class Scene:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.next_scene = None

        self.setup()

    def setup(self):
        pass

    def tick(self):
        pass

    def render(self):
        pass

    def close(self):
        pass

    def mouse_down(self, button):
        pass

    def mouse_up(self, button):
        pass

    def events(self, event: pygame.event.Event):
        pass
