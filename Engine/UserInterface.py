import pygame


class UIElement:
    def __init__(self, image, length=30):
        self.image = image
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

    def render(self, width, height):
        if width < 2 or height < 2:
            raise ValueError("Size must be greater than or equal to 3x3.")
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
        return surf
