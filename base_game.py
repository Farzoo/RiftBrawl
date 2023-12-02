from abc import ABC, abstractmethod

import pygame
from pygame import Surface

from player import Player
from utils.event import Event


class BaseGame(ABC):

    @property
    @abstractmethod
    def player1(self) -> Player:
        pass

    @property
    @abstractmethod
    def player2(self) -> Player:
        pass

    @property
    @abstractmethod
    def window(self) -> pygame.Surface:
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def level(self):
        pass

    @property
    @abstractmethod
    def on_resize(self) -> Event[Surface]:
        pass

    @on_resize.setter
    @abstractmethod
    def on_resize(self, value: Event[Surface]):
        pass
