import pygame

from Engine.Maths import Vec2, pythagoras

# Object capsule


class ObjectManager:
    def __init__(self, screen, *objects):
        self.screen = screen
        self.objects = list(objects)

    def update(self):

        from main import player
        player.interactable_objects = []

        for object in self.objects:
            object.update()
            if object.interactable:
                if pythagoras(Vec2(object.x, object.y), Vec2(player.x, player.y)) <= object.activation_range:
                    player.interactable_objects.append(object)

    def get_render_entities(self):
        return self.objects
