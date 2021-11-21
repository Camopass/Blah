import os
import pygame
import json


class Frame:
    def __init__(self, json):
        self.frame = json['frame']
        self.rotated = json['rotated']
        self.trimmed = json['trimmed']
        self.spriteSourceSize = json['spriteSourceSize']
        self.sourceSize = json['sourceSize']


class Frames:
    def __init__(self, frames):
        self.frames = []
        for i, frame in frames.items():
            self.frames.append(Frame(frame))


class Meta:
    def __init__(self, json):
        self.app = json['app']
        self.version = json['version']
        self.image = json['image']
        self.format = json['format']
        self.size = json['size']
        self.scale = json['scale']


class AnimateAnimation:
    def __init__(self, json):
        self.frames = Frames(json['frames'])
        self.meta = Meta(json['meta'])


class Animation:
    def __init__(self, fp, scaling=1.0):
        self.json_path = fp
        with open(fp, 'r', encoding='utf-8-sig') as f:
            j = json.load(f)
            self.aa_animation = AnimateAnimation(j)
        self.meta = self.aa_animation.meta
        self.image_path = os.path.join(os.path.dirname(os.path.relpath(fp)), self.meta.image)
        self.scale = self.meta.scale
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.frames = []
        self.scaling = scaling

        print(self.aa_animation.frames.frames)
        for data in self.aa_animation.frames.frames:
            self.frames.append(data)

        self.length = len(self.frames)

    def get_image(self, tick, seconds=None):
        if seconds is not None:
            tick /= seconds
        frame = int(tick) % self.length
        frame = self.frames[int(frame)]

        if not frame.rotated:
            rect = frame.frame
            if self.scaling == 1:
                return self.image.subsurface(pygame.Rect(rect['x'], rect['y'], rect['w'], rect['h']))
            elif self.scaling == 2:
                return pygame.transform.scale2x(self.image.subsurface(pygame.Rect(rect['x'], rect['y'], rect['w'], rect['h'])))
            else:
                im = self.image.subsurface(pygame.Rect(rect['x'], rect['y'], rect['w'], rect['h']))
                return pygame.transform.scale(im, (im.get_height() * self.scaling, im.get_height() * self.scaling))
