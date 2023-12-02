import random
import sys
from typing import Any, Dict

import pygame
import pygame.threads
from pygame import Vector2, Surface

import key_bindings
from base_game import BaseGame
from entities.character import Character
from level import Level
from player import Player
from render.result_scene import ResultScene
from render.scene import Scene
from resources.character_loader import CharacterDataFactory
from resources.level_registry import LevelRegistry
from resources.resources_manager import ResourcesManager
from utils.event import Event


class Game(BaseGame):

    @property
    def on_resize(self) -> Event[Surface]:
        return self._on_resize

    @on_resize.setter
    def on_resize(self, value: Event[Surface]):
        self._on_resize = value

    @property
    def player1(self) -> Player:
        return self._player1

    @property
    def player2(self) -> Player:
        return self._player2

    def __init__(self, screen: Surface, player1_character: str, player2_character: str, fps=1000, title="Game"):

        self._screen = screen

        pygame.display.set_caption(title)

        self.title = title

        self._fps = fps
        self._clock = pygame.time.Clock()
        self._running = True
        self._on_resize = Event[Surface]()

        self._level = LevelRegistry.LevelsFactory["level_1"]()

        self._player1 = Player("player1", self.create_character(player1_character, self._level), self._level.spawn_points[0])
        self._player1.on_character_death += self.on_character_death

        self._player2 = Player("player2", self.create_character(player2_character, self._level), self._level.spawn_points[-1])
        self._player2.on_character_death += self.on_character_death

        self.level.add_character(self._player1.character, self._player2.character)

        self._scene_stack = []
        self._scene_stack.append(Scene(self))

        self._title_refresh_rate = 0.1


    @property
    def level(self):
        return self._level

    @property
    def window(self) -> pygame.Surface:
        return self._screen

    def run(self):
        while self._running:
            self.update()
            self.draw()

    def update(self):

        p1_inputs = {} # type: Dict[key_bindings.Command, Any]
        p2_inputs = {} # type: Dict[key_bindings.Command, Any]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.VIDEORESIZE:
                #self._screen = pygame.display.set_mode((event.w, event.h), self.flags)
                self._on_resize(self.window)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    self.close()

        keys = pygame.key.get_pressed()

        for key, command in key_bindings.player1_key_mapping.items():
            p1_inputs[command] = keys[key]

        for key, command in key_bindings.player2_key_mapping.items():
            p2_inputs[command] = keys[key]

        self._clock.tick(self._fps)

        self.player1.input(self._clock.get_time()/1000, p1_inputs)
        self.player2.input(self._clock.get_time()/1000, p2_inputs)

        self._level.update(self._clock.get_time()/1000)

        for scene in self._scene_stack:
            scene.update(self._clock.get_time()/1000)

        if self._title_refresh_rate <= 0:
            self._title_refresh_rate = 0.1
            pygame.display.set_caption(self.title + " " + str(self._clock.get_fps()))

        self._title_refresh_rate -= (self._clock.get_time()/1000)


    def draw(self):
        for scene in self._scene_stack:
            scene.draw()
        pygame.display.flip()

    def close(self):
        self._running = False

    def on_character_death(self, player: Player):
        if player.has_lost:
            if player == self._player1:
                self._scene_stack.append(ResultScene(self.player2, self))
            else:
                self._scene_stack.append(ResultScene(self.player1, self))
        else:
            player.character.on_death -= self.on_character_death
            player.respawn_point = random.choice(self._level.spawn_points)
            character = self.create_character(player.character.data.name, self._level, player.respawn_point)
            player.character = character

    def create_character(self, character_name: str, level: Level, position: Vector2 = Vector2(0, 0)):
        character_factory = ResourcesManager.characters[character_name]
        character = Character(level, character_factory(), position)
        self._level.add_character(character)
        return character

