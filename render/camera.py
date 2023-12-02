from typing import Tuple

import pygame.sprite
from pygame import Vector2, Surface, Rect


class Camera:

    def __init__(self, display_surface, camera_pos, width, height, level):
        self.rect = Rect(camera_pos, (width, height))
        self.level = level
        self.offset = Vector2(0, 0)
        self.display_surface = display_surface

    def transform(self, rect: pygame.Rect, speed: float = 1.0):
        new_x = rect.x - self.offset.x * speed - self.level.origin.x * (1-speed)
        new_y = rect.y - self.offset.y * speed - (self.level.origin.y - self.height) * (1-speed)

        return Rect(new_x, new_y, rect.width, rect.height)


    def draw(self, *surfaces: Tuple[Surface, pygame.Rect], speed: float = 1.0):
        """Applies the camera offset to a sprite and blits it onto the camera surface."""

        subsurface = self.display_surface.subsurface(
            Rect(self.rect.x, self.rect.y, self.width, self.height)
        )

        subsurface.blits(
            [(surface, self.transform(rect, speed)) for surface, rect in surfaces]
        )

    def draw_with_speed(self, *surfaces: Tuple[Surface, pygame.Rect, float]):
        """Applies the camera offset to a sprite and blits it onto the camera surface."""

        subsurface = self.display_surface.subsurface(
            Rect(self.rect.x, self.rect.y, self.width, self.height)
        )

        subsurface.blits(
                [(surface, self.transform(rect, speed)) for surface, rect, speed in surfaces]
            )

    def finish_draw(self):
        pass

    def update(self, xy: Tuple[int, int]):
        """Updates the camera's offset to center on the target."""
        xy_int = (int(xy[0]), int(xy[1]))
        self.offset.x = xy_int[0] - int(self.width / 2)
        self.offset.y = xy_int[1] - int(self.height / 2)

        if self.offset.x < self.level.origin.x:
            self.offset.x = self.level.origin.x
        elif self.offset.x + self.width > self.level.origin.x + self.level.width:
            self.offset.x = self.level.origin.x + self.level.width - self.width

        if self.offset.y > self.level.origin.y - self.height:
            self.offset.y = self.level.origin.y - self.height
        elif self.offset.y < self.level.origin.y - self.level.height:
            self.offset.y = self.level.origin.y - self.level.height

        surface = self.display_surface.subsurface(self.rect)
        surface.fill((0, 0, 0))


    @property
    def camera_surface(self):
        return self.display_surface.subsurface(self.rect)

    @property
    def width(self):
        return self.camera_surface.get_width()

    @width.setter
    def width(self, width):
        self.rect = Rect(self.rect.topleft, (width, self.height))

    @property
    def height(self):
        return self.camera_surface.get_height()

    @height.setter
    def height(self, height):
        self.rect = Rect(self.rect.topleft, (self.width, height))