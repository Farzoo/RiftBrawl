from abc import abstractmethod, ABC
from typing import Iterable, List

from pygame import Vector2

from render.parallax_background import ParallaxBackground


class BaseLevel(ABC):

    @property
    @abstractmethod
    def spawn_points(self) -> List[Vector2]:
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @property
    @abstractmethod
    def origin(self) -> Vector2:
        pass

    @property
    @abstractmethod
    def background(self) -> ParallaxBackground:
        pass

    @abstractmethod
    def add_character(self, *characters: 'Character'):
        pass

    @abstractmethod
    def remove_character(self, *characters: 'Character'):
        pass

    @abstractmethod
    def add_entity(self, *entities: 'Entity'):
        pass

    @abstractmethod
    def remove_entity(self, *entities: 'Entity'):
        pass

    @abstractmethod
    def request_entity_removal(self, entity: 'Entity'):
        pass

    @abstractmethod
    def get_entities(self) -> Iterable['Entity']:
        pass

    @abstractmethod
    def update(self, dt):
        pass







