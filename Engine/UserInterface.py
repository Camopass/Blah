import pygame
import typing


def render_text_in_rect(font: pygame.font.Font, text: str, dim: typing.Tuple[int, int], *, line_spacing=3, color=(255, 255, 255)):
    """Render text inside a rect. This auto wraps the text."""
    surf = pygame.Surface((dim[0], dim[1]), flags=pygame.SRCALPHA)
    y = 0
    while len(text) > 0:
        leftover = ""
        while font.size(text)[0] > dim[0]:
            leftover += text[len(text) - 1]
            text = text[:-1]
        surf.blit(font.render(text, True, color), (0, y))
        y += line_spacing + font.size(text)[1]
        text = leftover[::-1]
    return surf


class UIElement:
    """
    UIElement is a class to create variable sized UI Elements.
    You supply the image and the size of the image. This could probably be automatically determined, but I don't want to.
    The image is split into 9 equal parts, and the middle segments are repeated so it can fit the size.

    Examples:

        ui = UIElement(image, 30)
        pygame.display.blit(image, [200, 500])

    """
    def __init__(self, image, length):
        self.image = image
        if image.get_width() != image.get_height():
            raise ValueError("Must be 1:1 Aspect Ratio.")
        if length % 3 != 0:
            raise ValueError("Size must be a multiple of 3")
        self.length = length
        am = length / 3
        self.segments = [
            image.subsurface((0, 0, am, am)), image.subsurface(am, 0, am, am), image.subsurface((am * 2, 0, am, am)),
            image.subsurface((0, am, am, am)), image.subsurface(am, am, am, am), image.subsurface((am * 2, am, am, am)),
            image.subsurface((0, am * 2, am, am)), image.subsurface((am, am * 2, am, am)),
            image.subsurface((am * 2, am * 2, am, am))
        ]
        self.am = am

    def render(self, width, height, scaling=False):
        """Width and height are the amount of tiles wide the returned image will be. Scaling is a size multiplier."""
        if width < 2 or height < 2:
            raise ValueError("Size must be greater than or equal to 2x2.")
        surf = pygame.Surface((self.am * width, self.am * height), flags=pygame.SRCALPHA, depth=32)
        surf.blit(self.segments[0], (0, 0))
        for i in range(height - 2):
            surf.blit(self.segments[3], (0, self.am * (i + 1)))
        surf.blit(self.segments[6], (0, self.am * (height - 1)))
        for i in range(width - 2):
            surf.blit(self.segments[1], (self.am * (i + 1), 0))
            for x in range(height - 2):
                surf.blit(self.segments[4], (self.am * (i + 1), self.am * (x + 1)))
            surf.blit(self.segments[7], (self.am * (i + 1), self.am * (height - 1)))
        surf.blit(self.segments[2], (self.am * (width - 1), 0))
        for i in range(height - 2):
            surf.blit(self.segments[5], (self.am * (width - 1), self.am * (i + 1)))
        surf.blit(self.segments[8], (self.am * (width - 1), self.am * (height - 1)))
        if scaling != False:
            return pygame.transform.scale(surf, (surf.get_width() * scaling, surf.get_height() * scaling))
        return surf


class Notice(UIElement):
    """
    A notice element is a UI Element with text inside of it.
    """
    def __init__(self, image, length, text):
        super().__init__(image, length)
        self.text = text

    def render(self, width, height, *, font, padding=3, scaling=False):
        """Font is the font renderer used. Padding moves the text further from the border."""
        surf = super().render(width, height, scaling=scaling)
        print(surf.get_width(), surf.get_height())
        text = render_text_in_rect(font, self.text, (surf.get_width() - padding * 2, surf.get_height() - padding * 2))
        surf.blit(text, (padding, padding))
        return surf


class BaseButton:
    """
    A button class. TODO: Fix buttons you idiot.
    """
    def __init__(self, rect, image):
        self._rect = rect
        self.image = image
        self.hovered = False
        self._x = rect.x
        self._y = rect.y

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect
        self._x = rect.x
        self._y = rect.y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._rect.x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._rect.y = y

    @classmethod
    def uie_button(cls, image, length, x, y, width, height, scaling=False):
        """Create a button with a UI Element texture."""
        image = UIElement(image, length).render(width, height, scaling=scaling)
        return cls(pygame.Rect(x, y, image.get_width(), image.get_height()), image)

    def on_click(self):
        pass

    def on_mouse_down(self):
        pass

    def get_image(self):
        return self.image

    def render(self):
        return self.get_image()


class Button(BaseButton):
    def __init__(self, rect, image, hovered_image, font, window, text=None, padding=3):
        self.text = text
        self.hovered_image = hovered_image
        super().__init__(rect, image)
        self.font = font
        self.window = window
        self.padding = padding

    @classmethod
    def uie_button(cls, image, length, x, y, width, height, hovered_image, font, window, *, scaling=False, text=None, padding=3):
        image = UIElement(image, length).render(width, height, scaling=scaling)
        h_im = UIElement(hovered_image, length).render(width, height, scaling=scaling)
        return cls(pygame.Rect(x, y, image.get_width(), image.get_height()), image, h_im, font, window, text=text, padding=padding)

    def get_image(self):
        if self.rect.collidepoint(self.window.get_mouse_pos()):
            return self.hovered_image
        else:
            return self.image

    def render(self):
        im = self.get_image()
        text = render_text_in_rect(self.font, self.text, (im.get_width() - self.padding, im.get_height() - self.padding))
        im.blit(text, ((im.get_width() - (text.get_width())), (im.get_height() - (text.get_height()))))
        return im
