import json
from typing import Any

import numpy as np
import pygame
from pygame import Color

from resources.resources_registry import ResourcesRegistry


class TexturesLoader:

    @staticmethod
    def load_textures_from_json(
            filepath: str,
            settings: ResourcesRegistry[str, Any],
            builder: ResourcesRegistry.ResourceRegistryBuilder[str, pygame.Surface]
    ) -> ResourcesRegistry.ResourceRegistryBuilder[str, pygame.Surface]:
        with open(filepath, 'r') as file:
            data = json.load(file)
            base_scaling = float(settings["base_scaling"])
            for texture_info in data['textures']:
                name = texture_info['name']
                file_path = texture_info['path']
                size = tuple(texture_info['size'])
                scale = float(texture_info['scale'])
                builder.register(name, TexturesLoader.texture_loader(file_path, size, scale_factor=scale*base_scaling))
        return builder

    @staticmethod
    def texture_loader(filepath: str, size: tuple = None, scale_factor: float=1, color_key=None, alpha=False) -> pygame.Surface:
        texture = pygame.image.load(filepath)

        if size is None:
            size = texture.get_size()


        size = (size[0] * scale_factor, size[1] * scale_factor)

        texture = pygame.transform.scale(texture, size)

        if alpha or TexturesLoader.has_transparency(texture):
            texture = texture.convert_alpha()
            texture.set_colorkey(Color(0, 0, 0, 0), pygame.RLEACCEL)
        else:
            texture = texture.convert()

        if color_key is not None:
            texture.set_colorkey(color_key, pygame.RLEACCEL)

        return texture

    @staticmethod
    def has_transparency(surface: pygame.Surface, threshold=255) -> bool:
        image_with_alpha = surface.convert_alpha()

        try:
            alpha_array = pygame.surfarray.pixels_alpha(image_with_alpha)
            has_any = np.any(alpha_array < threshold)
            del alpha_array
            return has_any
        except ValueError:
            # If there's a ValueError, the image doesn't have an alpha channel
            return False
