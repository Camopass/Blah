import pygame

"""
Buttons for all your button-y purposes
"""


class Button:
    def __init__(self, x, y, name, icon, func=None, label=None):
        self.name = name
        self.x = x
        self.y = y
        self.icon = icon
        self.image = icon
        self.rect = pygame.Rect(x, y, icon.get_width(), icon.get_height())
        self.rect.x, self.rect.y = x, y
        self.func = func
        self.label = label
        self.f = pygame.font.SysFont('Arial', 20)

    def on_pressed(self, button):
        print('Button pressed.')
        self.func()

    def on_released(self, button):
        pass

    def update(self):
        pass

    def render(self, window):
        if type(window) != pygame.Surface:
            window.screen.blit(self.icon, (self.x, self.y))
        else:
            window.blit(self.icon, (self.x, self.y))
