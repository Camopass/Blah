import pygame
import json

from Engine.util import encode_image, decode_image


class Level:
    def __init__(self, name, length, height, tile_size):
        self.name = name
        self.tile_size = tile_size
        self.piece_dict = {0: None, 1: pygame.image.load("assets/Tiles/dirt.png").convert(),
                           2: pygame.image.load("assets/Tiles/grass.png").convert()}
        self.image_dict = {0: None, 1: encode_image(self.piece_dict[1]),
                           2: encode_image(self.piece_dict[2])}
        self.length = length
        self.height = height
        self.floor_pieces = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        ]

    def render(self):
        surface = pygame.Surface((self.length * self.tile_size, self.height * self.tile_size), pygame.SRCALPHA, 32)
        for ind, i in enumerate(self.floor_pieces):
            if self.piece_dict[i] is not None:
                pos = (((ind % self.length) * self.tile_size),
                       ((ind // self.length) * self.tile_size))
                surface.blit(self.piece_dict[i], pos)
        return surface

    @classmethod
    def load(cls, directory, grid_size):
        with open(directory, 'r') as file:
            map_data = json.loads(file.read())
        l = Level(map_data["LevelName"], map_data["LevelLength"], map_data["LevelHeight"], map_data["TileSize"])
        piece_dict = {}
        for p_id, piece in map_data["LevelPieces"].items():
            if piece is None:
                piece_dict[p_id] = None
                continue
            piece_dict[p_id] = piece
        true_data = {}
        for p_id, item in piece_dict.items():
            if item is None:
                true_data[int(p_id)] = None
                continue
            true_data[int(p_id)] = decode_image(item, (grid_size, grid_size))
        l.piece_dict = true_data
        l.floor_pieces = map_data["LevelData"]
        return l
