from abc import ABC, abstractmethod

from base_level import BaseLevel
from entities.entity import Entity


class BaseAttackExecutor(ABC):
    @abstractmethod
    def execute(self, level: BaseLevel, owner: Entity, friend_obj):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def can_execute(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass
