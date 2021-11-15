import base64
import pygame

def encode_image(image):
    return base64.b64encode(pygame.image.tostring(image, "RGBA")).decode('ascii')


def decode_image(image_str, size):
    return pygame.image.fromstring(base64.b64decode(image_str), size, "RGBA")
