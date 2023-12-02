from _ast import Set
from typing import Iterable, List

import pygame
from pygame import Vector2
from pygame.sprite import Group

from base_level import BaseLevel
from entities.character import Character
from entities.entity import Entity
from render.parallax_background import ParallaxBackground
from utils.multi_dispatcher import MultiDispatcher


class Level(BaseLevel):

    @property
    def spawn_points(self) -> List[Vector2]:
        return self._spawn_points

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def origin(self) -> Vector2:
        return self._origin

    @property
    def background(self) -> ParallaxBackground:
        return self._background

    def get_entities(self) -> Iterable[Entity]:
        return self._entities

    def __init__(self,
                 collision_dispatcher: MultiDispatcher[None],
                 background: ParallaxBackground,
                 spawn_points: List[Vector2],
                 width,
                 height,
                 gravity,
                 max_velocity_x,
                 origin: Vector2 = Vector2(0, 0),
                 ):

        self._collision_dispatcher = collision_dispatcher

        self._spawn_points = spawn_points
        
        self._background = background

        self._all_sprites = pygame.sprite.Group()

        self._entities_set = set()  # type: Set[Entity]
        self._entities = pygame.sprite.Group()  # type: Group[Entity]

        self._characters_set = set()  # type: Set[Character]
        self._characters = Group()  # type: Group[Character]

        self._entities_to_remove = []  # type: List[Entity]

        self._width = width
        self._height = height

        self._origin = origin

        self._gravity = gravity
        
        self._max_velocity_x = max_velocity_x

    def add_character(self, *characters):
        for character in characters:
            if character not in self._characters_set:
                self._characters_set.add(character)
                self._characters.add(character)
                self.add_entity(character)

    def remove_character(self, *characters):
        for character in characters:
            if character in self._characters_set:
                self._characters_set.remove(character)
                self._characters.remove(character)
                self.remove_entity(character)

    def request_entity_removal(self, entity: Entity):
        self._entities_to_remove.append(entity)


    def add_entity(self, *entities):
        for entity in entities:
            if entity not in self._entities_set:
                self._entities_set.add(entity)
                self._entities.add(entity)
                self._all_sprites.add(entity)

    def remove_entity(self, *entities):
        for entity in entities:
            if entity in self._entities_set:
                self._entities_set.remove(entity)
                self._entities.remove(entity)
                self._all_sprites.remove(entity)

    def update(self, dt):
        self._all_sprites.update(dt)
        for entity in self._entities:
            self._update_entity_position(dt, entity)
        for character in self._characters:
            self._update_character_grounded_status(character)
        for entity in self._entities:
            self._handle_sprite_collision(entity)
        self._process_entities_to_remove()

    def _update_entity_position(self, dt, entity):
        entity.velocity.y += self._gravity * dt
        if entity.box.bottom > self.origin.y:
            entity.box.bottom = self.origin.y
            entity.velocity.y = 0
        if entity.box.top < self.origin.y - self.height:
            entity.box.top = self.origin.y - self.height
            entity.velocity.y = 0
        if entity.box.left < self.origin.x:
            entity.box.left = self.origin.x
            entity.velocity.x = 0
        if entity.box.right > self.width + self.origin.x:
            entity.box.right = self.origin.x + self.width
            entity.velocity.x = 0
        if abs(entity.velocity.x) > self._max_velocity_x:
            entity.velocity.x = self._max_velocity_x * entity.velocity.x / abs(entity.velocity.x)

    def _update_character_grounded_status(self, character):
        character.on_ground = character.box.bottom == self.origin.y

    def _handle_sprite_collision(self, entity):
        collided_sprites = pygame.sprite.spritecollide(entity, self._entities, False) # type: List[Entity]

        def distance_to_nearest_edge(sprite):
            center_distance = Vector2(sprite.rect.center).distance_squared_to(Vector2(entity.rect.center))
            half_diagonal = sprite.rect.width ** 2 + sprite.rect.height ** 2
            edge_distance = center_distance - half_diagonal
            return max(0, edge_distance)

        collided_sprites.sort(key=distance_to_nearest_edge)

        for collided_sprite in collided_sprites:
            if collided_sprite != entity and not collided_sprite.destroyed:
                self._collision_dispatcher.dispatch_no_collect(entity, collided_sprite)

    def _process_entities_to_remove(self):
        for entity in self._entities_to_remove:
            self.remove_entity(entity)
        self._entities_to_remove.clear()








