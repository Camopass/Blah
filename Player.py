import pygame

from Engine.Entity import Entity

class Player(Entity):
    def __init__(self, image):
        super().__init__("Player", "player", image)
        self.max_health = 5
        self.health = 5
        # self.animation = Animation() # TODO: Add animations you ducking dumbass
