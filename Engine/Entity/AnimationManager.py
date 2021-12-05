import typing
import pygame

from Engine.Entity.Animations import Animation
from Engine.util import TickQueue


class AnimationState:
    def __init__(self, animation: Animation, state: str, length: int = None, time_scaling=1.0):
        self.animation = animation
        self.state = state
        self.time_scaling = time_scaling
        if length is not None:
            self.length = length
        else:
            self.length = animation.length * 0.5

    def __repr__(self):
        return f'Animation {self.state}: length {self.length}'


class AnimationManager:
    def __init__(self, idle, *states):
        self.states = states
        self.queue = TickQueue()
        self.idle = idle

    def update(self) -> None:
        self.queue.update()

    def get_animation(self) -> AnimationState:
        for state in self.states:
            if self.queue.has_item(state):
                return state
        return self.idle

    def add_state(self, state: AnimationState):
        self.states.append(state)

    def add_animation(self, animation: AnimationState) -> None:
        if animation not in self.states:
            raise ValueError("Cannot add animation to queue. Please add animation to the state list with "
                             "animation_manager.add_state(state).")
        self.queue.add_item(animation, animation.length)

    def get_frame(self) -> pygame.Surface:
        animation = self.get_animation()
        ticks = pygame.time.get_ticks()
        frame = int(ticks * animation.time_scaling) % animation.length
        print(self.queue, pygame.time.get_ticks())
        return animation.animation.get_image(frame)
