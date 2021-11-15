"""
Window Manager for the game. Automatically adds support for resizing and fullscreen, and does a little rendering.
"""

import pygame

from math import ceil

from Engine.Maths import map_range


class Window:
    def __init__(self, width, height, caption: str = "PyGame Engine", icon=None):
        self.window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # This is the actual pygame surface
        self.screen = pygame.surface.Surface((width, height))  # This is the surface that you draw to
        self.target_width, self.target_height = width, height  # This is the width and height of the screen we resize it to
        self.resized_rect = self.screen.get_rect()  # This is the rect of the screen after resizing
        self.center_position = [0, 0]  # Offset of the resized screen to be centered on the window
        self.is_fullscreen = False  # If the window is fullscreen or not
        self.entity_manager = None  # Window Entity Manager
        self.original_dimensions = width, height
        self.aspect_ratio_multiplier = height / width, width / height
        pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(icon)

        self.left_click = False
        self.right_click = False
        self.middle_click = False

    # Set the window to fullscreen mode
    def fullscreen(self):
        self.is_fullscreen = True
        self.window_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.update_resize()

    # Set the window to windowed mode
    def windowed(self):
        self.is_fullscreen = False
        self.window_surface = pygame.display.set_mode((int(self.target_width - 200), int(self.target_height - 200)), pygame.RESIZABLE)
        self.update_resize()

    # Recalculate the sizing and positioning of the screen on the window
    def update_resize(self):
        window_width, window_height = self.window_surface.get_width(), self.window_surface.get_height()
        target_width = window_width
        if target_width * self.aspect_ratio_multiplier[0] > window_height:
            target_width = window_height * self.aspect_ratio_multiplier[1]
        if target_width is not None:
            target_height = target_width * self.aspect_ratio_multiplier[0]
            resized_screen = pygame.transform.smoothscale(self.screen, (ceil(target_width), ceil(target_height)))
            self.target_width, self.target_height = target_width, target_height

        width = self.window_surface.get_width()
        height = self.window_surface.get_height()
        screen_width = resized_screen.get_width()
        screen_height = resized_screen.get_height()
        center_position = [0, 0]

        a = width - screen_width
        center_position[0] = a / 2
        b = height - screen_height
        center_position[1] = b / 2

        self.resized_rect = pygame.rect.Rect(*center_position, target_width, target_height)

        self.center_position = center_position

    # I'm lazy
    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.get_transforms(x, y)

    # Transform a Pos from the window surface to the screen surface
    def get_transforms(self, x, y):
        if not self.resized_rect.collidepoint(x, y):
            return 0, 0
        window = self.window_surface.get_rect()
        # map x/(center_pos to width - center_pos) to x/(0 to screen width)
        m_x, m_y = map_range(x, self.center_position[0], window.width - self.center_position[0], 0, self.resized_rect.width),\
                   map_range(y, self.center_position[1], window.height - self.center_position[1], 0, self.resized_rect.height)
        m_x, m_y = map_range(m_x, 0, self.resized_rect.width, 0, self.original_dimensions[0]), \
                   map_range(m_y, 0, self.resized_rect.height, 0, self.original_dimensions[1])

        return m_x, m_y

    # Render the screen to the window using the positioning and resizing
    def render(self):
        self.window_surface.fill((0, 0, 0))
        resized_screen = pygame.transform.smoothscale(self.screen, (ceil(self.target_width), ceil(self.target_height)))
        self.window_surface.blit(resized_screen, self.center_position)

    # We do a little rendering
    def render_managers(self, *managers: iter):
        entities = []
        for manager in managers:
            entities += manager.get_render_entities()
        entities.sort(key=lambda entity: entity.y if entity.z_override is None else entity.z_override)
        for entity in entities:
            entity.render(self.screen)

    # When the mouse releases
    def mouse_up(self, button):
        if self.entity_manager is not None:
            for entity in self.entity_manager.entities:
                if entity.rect.collidepoint(self.get_mouse_pos()):
                    entity.on_pressed(button)

    # Mouse go down
    def mouse_down(self, button):
        if self.entity_manager is not None:
            for entity in self.entity_manager.entities:
                if entity.rect.collidepoint(self.get_mouse_pos()):
                    entity.on_released(button)
