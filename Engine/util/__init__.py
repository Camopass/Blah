import base64
import pygame
import typing

def encode_image(image: pygame.Surface) -> str:
    return base64.b64encode(pygame.image.tostring(image, "RGBA")).decode('ascii')


def decode_image(image_str: str, size: typing.Tuple[int, int]) -> pygame.Surface:
    return pygame.image.fromstring(base64.b64decode(image_str), size, "RGBA")


class TickQueue:
    def __init__(self, *items: typing.List) -> None:
        tick = pygame.time.get_ticks()
        self.items: typing.List[typing.List[int, typing.Any]] = [[i[0] + tick, i[1]] for i in items]

    def add_item(self, item, length: int) -> None:
        if not self.has_item(item):
            self.items.append([pygame.time.get_ticks() + length, item])
        else:
            for item in self.items:
                if item[1] == item:
                    item[0] = pygame.time.get_ticks() + length

    def add_many(self, *items: typing.List) -> None:
        for i in items:
            self.add_item(i[0], i[1])

    def update(self) -> typing.Tuple:
        c_tick = pygame.time.get_ticks()
        expired_items = []
        for i, (tick, _) in enumerate(self.items):
            if tick <= c_tick and tick != 0:
                expired_items.append(self.items.pop(i))
        return tuple(expired_items)

    def has_item(self, item) -> bool:
        for _, i in self.items:
            if type(i) == item or i == item:
                return True

    def __list__(self):
        return self.items

    def __eq__(self, other):
        return self.items == other.items

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return str(self.items)

    def __ne__(self, other):
        return self.items != other.items

    def __sizeof__(self):
        return len(self.items)

    def __add__(self, other):
        return TickQueue(*(self.items + other.items))
