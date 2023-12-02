from typing import Any, Dict

import pygame
from pygame import Rect, Vector2

from base_level import BaseLevel
from entities.animation import Animation
from entities.character import Character
from entities.melee_attack import MeleeAttack
from entities.character_animation import CharacterAnimation
from entities.entity import Entity
from key_bindings import Command
from resources.character_loader import CharacterData
from utils.event import Event


class Player:

    def __init__(self, name: str, character: Character, respawn_point: Vector2):
        self.name = name
        self._character = character
        self.lives_left = 3
        self.respawn_point = respawn_point
        self.character.box.midbottom = self.respawn_point
        self.character.on_death += self.on_death
        self.on_character_death = Event[Player]()

    def input(self, dt: float, inputs: Dict[Command, Any]):
        if self.character.is_dead:
            return
        self.character.input(dt, inputs)

    def on_death(self, character: Character):
        self.lives_left -= 1
        self.on_character_death(self)

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, character: Character):
        self._character.on_death -= self.on_death
        self._character = character
        self._character.on_death += self.on_death
        self._character.position = self.respawn_point

    @property
    def has_lost(self):
        return self.lives_left <= 0