from abc import abstractmethod, ABC
from math import ceil, floor
from typing import Optional, Iterable

import pygame.sprite
from pygame import Vector2, Rect

from base_level import BaseLevel
from entities.box import Box


class Entity(pygame.sprite.Sprite, ABC):

    def __init__(self,
                 level: BaseLevel,
                 ):
        pygame.sprite.Sprite.__init__(self)

        self._level = level

        self._velocity = Vector2(0.0, 0.0)

        self._box = Box(0, 0, 0, 0)

        self._reversed = False

        self._destroyed = False

    @property
    def box(self) -> Box:
        return self._box

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    @property
    def level(self) -> BaseLevel:
        return self._level

    @level.setter
    def level(self, level: BaseLevel) -> None:
        self._level = level

    @property
    @abstractmethod
    def image(self) -> pygame.Surface:
        pass

    @property
    def layers(self) -> Iterable[pygame.Surface]:
        yield self.image

    @property
    def image_rect(self) -> Rect:
        return self.rect

    @property
    def rect(self) -> Rect:
        return self.box.rect

    @property
    def reversed(self) -> bool:
        return self._reversed

    @property
    def destroyed(self) -> bool:
        return self._destroyed

    def destroy(self) -> None:
        self.level.request_entity_removal(self)
        self._destroyed = True

    def update(self, dt: float) -> None:
        self.box.x += self._velocity.x * dt
        self.box.y += self._velocity.y * dt

