import pygame

from Engine.EntityManager import EntityManager
from Engine.Window import Window

# In-Game screen


class Screen:
    def __init__(self, window: Window, x: float, y: float, width: float, height: float):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.open = False
        self.last_toggled = pygame.time.get_ticks()
        self.textRenderer = pygame.font.SysFont('assets/fonts/vcr.ttf', 20)

    def toggle_open(self):
        if pygame.time.get_ticks() - self.last_toggled < 100:
            return
        if self.open:
            self.open = False
        else:
            self.open = True
        self.last_toggled = pygame.time.get_ticks()

    def render(self):
        if self.open:
            c = pygame.color.Color((10, 10, 10, 10))
            self.surface.fill(c)
            self.window.screen.blit(self.surface, (self.x, self.y))


class DataScreen(Screen):
    def __init__(self, window: Window, x: float, y: float, width: float, height: float, title: str, entity_manager: EntityManager):
        super().__init__(window, x, y, width, height)
        self.title = title
        self.entity_manager = entity_manager

    def get_data(self, entity_manage: EntityManager):
        return ''

    # Render some text
    def render(self):
        if self.open:
            c = pygame.color.Color((10, 10, 10, 10))
            self.surface.fill(c)
            x = self.width * 0.1
            y = self.height * 0.03
            self.surface.blit(self.textRenderer.render(self.title, True, (255, 255, 255)), (x, y))
            data = self.get_data(self.entity_manager)
            y = self.height * 0.1
            for line in data.split('\n'):
                self.surface.blit(self.textRenderer.render(line, True, (255, 255, 255)), (x, y))
                y += self.textRenderer.get_height() + 2
            self.window.screen.blit(self.surface, (self.x, self.y))
