import itertools
from typing import Tuple, List

import pygame
from pygame import Rect, Vector2

from render.camera import Camera


class Layer:
    def __init__(self, pos: 'Tuple[int, int] | Vector2', image: pygame.Surface, speed: float, name: str,
                 repeat_horizontal: bool = True, repeat_vertical: bool = False):
        self.image = image
        self.rect = self.image.get_rect(bottomleft=pos)
        self.speed = speed
        self.name = name
        self.repeat_horizontal = repeat_horizontal
        self.repeat_vertical = repeat_vertical

    def __repr__(self):
        return "Layer({}, {}, {}, {}, {}, {})".format(self.rect.bottomleft,
                                                      self.image,
                                                      self.speed,
                                                      self.name,
                                                      self.repeat_horizontal,
                                                      self.repeat_vertical
                                                      )

class ParallaxBackground:
    def __init__(self, layers: List[Layer] = None):
        self._layers = layers or []  # type: List[Layer]
        self._sort_layers()
        self._cached_surfaces = None

    @property
    def layers(self):
        return self._layers

    def add_layer(self, layer: Layer):
        self._layers.append(layer)
        self._sort_layers()

    def remove_layer(self, layer: Layer):
        if layer in self._layers:
            self._layers.remove(layer)
            self._sort_layers()

    def _sort_layers(self):
        self._layers.sort(key=lambda layer: layer.speed)

    def _get_surfaces(self, camera: Camera):
        surfaces = []
        for layer in self._layers:
            layer_width, layer_height = layer.image.get_size()

            repeat_count_x = 1
            repeat_count_y = 1

            start_x = layer.rect.x
            start_y = layer.rect.y

            if layer.repeat_horizontal:
                repeat_count_x = int(camera.level.width / layer_width) + 1
            if layer.repeat_vertical:
                repeat_count_y = int(camera.level.height / layer_height) + 1

            for i in range(repeat_count_x):
                for j in range(repeat_count_y):
                    x_position = start_x + (i * layer_width)
                    y_position = start_y + (j * layer_height)
                    surfaces.append(
                        (layer.image, Rect(x_position, y_position, layer_width, layer_height), layer.speed)
                    )

        return surfaces

    def _get_surfaces_optimize(self, camera: Camera):
        surfaces = []
        for layer in self._layers:
            layer_width, layer_height = layer.image.get_size()

            repeat_count_x = 1
            repeat_count_y = 1

            start_x = layer.rect.x
            start_y = layer.rect.y

            if layer.repeat_horizontal:
                start_x = start_x + layer_width * int(
                    ((camera.offset.x - camera.level.origin.x) * layer.speed) / layer_width)
                repeat_count_x = int(camera.width / layer_width) + 2
            if layer.repeat_vertical:
                start_y = start_y + layer_height * int(
                    ((camera.offset.y - camera.level.origin.y + camera.height) * layer.speed) / layer_height)
                repeat_count_y = int(camera.height / layer_height) + 2

            for i in range(repeat_count_x):
                for j in range(repeat_count_y):
                    x_position = start_x + (i * layer_width)
                    y_position = start_y - (j * layer_height)
                    surfaces.append(
                        (layer.image, Rect(x_position, y_position, layer_width, layer_height), layer.speed)
                    )

        return surfaces

    def draw(self, camera: Camera):
        surfaces = self._get_surfaces_optimize(camera)
        camera.draw_with_speed(*surfaces)
