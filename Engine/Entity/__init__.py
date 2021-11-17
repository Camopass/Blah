import typing
import pygame
from math import sin

from Engine.Maths import Vec2


class Entity:
    def __init__(self, name: str, id: str, image: pygame.image = None, *, z_override: int = None):
        self.name = name
        self.id = id
        self.original_image = image
        self.image = image
        self.xvel = 0
        self.yvel = 0
        self._x = 0
        self._y = 0
        self.game_x, self.game_y = 0, 0
        self.z_override = z_override
        self.y_offset = 0
        self.x_offset = 0
        if image is not None:
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        else:
            self.rect = pygame.Rect(self.x, self.y, 1, 1)

    def get_x(self):
        return self._x

    def set_x(self, a):
        self._x = a
        self.rect.x = a - self.image.get_width() / 2

    def get_y(self):
        return self._y

    def set_y(self, a):
        self._y = a
        self.rect.y = a - self.image.get_height() / 2

    def update(self):
        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9
        self.game_x += self.xvel
        self.game_y += self.yvel

    def on_pressed(self, button):
        print("Entity pressed")

    def on_released(self, button):
        pass

    def render(self, screen):
        screen.blit(self.image, (self.x + self.x_offset - 64, self.y + self.y_offset - 64))

    def set_center(self, x, y):
        w, h = self.image.get_width(), self.image.get_height()
        w /= 2
        h /= 2
        self.x, self.y = x - h, y + w

    x = property(get_x, set_x)
    y = property(get_y, set_y)


class Object(Entity):
    def __init__(self, name: str, id: str, image, *, interactable: bool = False, range: int = None,
                 enable_bloom: bool = False, bloom_image=None, moveable=False, z_override: int = None):
        super().__init__(name, id, image)
        self.interactable = interactable
        self.activation_range = range
        self.enable_bloom = enable_bloom
        self.moveable = moveable
        self.z_override = z_override
        if self.enable_bloom:
            self.bloom_image = self.do_bloom(bloom_image)
        else:
            self.bloom_image = None

    def interact(self, player):
        pass

    def do_bloom(self, image):
        image2 = pygame.transform.smoothscale(image, (image.get_width() // 10, image.get_height() // 10))
        image.blit(pygame.transform.smoothscale(image2, (image.get_width(), image.get_height())), (0, 0),
                   special_flags=pygame.BLEND_RGBA_ADD)
        image3 = pygame.transform.smoothscale(image, (image.get_width() // 5, image.get_height() // 5))
        image.blit(pygame.transform.smoothscale(image3, (image.get_width(), image.get_height())), (0, 0),
                   special_flags=pygame.BLEND_RGBA_ADD)

        return image

    def render(self, screen):
        pos = Vec2(self.x + self.x_offset, self.y + self.y_offset)
        screen.blit(self.image, pos.to_tuple())
        if self.enable_bloom:
            x = pos - (Vec2.from_tuple(self.image.get_size()) // Vec2(2, 2))
            screen.blit(self.bloom_image, x.to_tuple())

    def update(self):
        pass
