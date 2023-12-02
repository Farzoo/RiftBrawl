from typing import Any, Iterable, Dict

from pygame import Vector2, Rect, Surface

from base_level import BaseLevel
from comps.damage_data import DamageData
from comps.damageable import Damageable
from comps.friendly_obj import FriendObject
from entities.entity import Entity
from key_bindings import Command
from resources.character_loader import CharacterData
from utils.event import Event


class Character(Entity, Damageable):

    def __init__(self,
                 level: BaseLevel,
                 character_data: CharacterData,
                 position: Vector2
                 ):
        Entity.__init__(self, level)
        Damageable.__init__(self, character_data.stats.health, FriendObject())
        self.data = character_data
        self._name = character_data.name
        self.speed = character_data.stats.speed
        self.jump_force = character_data.stats.jump_force
        self.animations = character_data.animations
        self.primary_attack = character_data.primary_attack
        self.secondary_attack = character_data.secondary_attack
        self.box.size = character_data.stats.hitbox_size
        self.box.midbottom = position
        self._is_moving = False
        self.on_ground = True
        self._invuln_time = 0.5  # invulnerability time in seconds
        self._invuln_counter = 0.0  # invulnerability counter
        self._before_next_attack_time = 0.5
        self._before_next_attack_counter = 0.0
        self._invulnerable_image = None
        self.on_death = Event[Character]()

    @property
    def image_rect(self) -> Rect:
        direction = 1 if not self._reversed else -1
        return self.image.get_rect(
            midbottom=direction * Vector2(self.animations.offset_center) + Vector2(self.box.rect.midbottom)
        )

    @property
    def image(self) -> Surface:
        image = self.animations.get_frame(self.reversed)
        return image

    @property
    def layers(self) -> Iterable[Surface]:
        yield self.image

    @property
    def invulnerable(self) -> bool:
        return self._invuln_counter > 0.0

    def take_damage(self, damage_data: DamageData) -> None:
        if not self.invulnerable and not self.is_dead:
            Damageable.take_damage(self, damage_data)
            if self.is_dead:
                self.animations.request_animation("DEATH")
            self._velocity.x = damage_data.velocity.x
            self._velocity.y += damage_data.velocity.y
            self._invuln_counter = self._invuln_time
            self.animations.request_animation("HURT")

            self._cancel_attacks()

    def _cancel_attacks(self):
        self.primary_attack.cancel()
        self.secondary_attack.cancel()

        self._before_next_attack_counter = self._before_next_attack_time

        self.animations.request_animation_stop("PRIMARY_ATTACK")
        self.animations.request_animation_stop("SECONDARY_ATTACK")

    def update(self, dt: float) -> None:
        self.animations.request_animation("IDLE")
        self.animations.update(dt)

        self._check_falling(dt)
        self._check_moving(dt)

        self._invuln_counter -= dt
        self._before_next_attack_counter -= dt

        if self.is_dead:
            if self.animations.get_animation_pending("DEATH") is None:
                self.on_death(self)
                self.destroy()

        self.primary_attack.update(dt)
        self.secondary_attack.update(dt)

        Entity.update(self, dt)

    def input(self, dt: float, inputs: Dict[Command, Any]):

        self._handle_move(dt, inputs)

        if inputs.get(Command.JUMP, False):
            self._handle_jump(dt)
        if inputs.get(Command.MOVE_DOWN, False):
            self._handle_move_down(dt)
        if inputs.get(Command.PRIMARY_ACTION, False):
            self._handle_primary_action(dt)
        if inputs.get(Command.SECONDARY_ACTION, False):
            self._handle_secondary_action(dt)

    def _handle_move(self, dt: float, inputs: Dict[Command, Any]):
        self._is_moving = True
        if inputs.get(Command.MOVE_RIGHT, False):
            self._handle_move_right(dt)
        elif inputs.get(Command.MOVE_LEFT, False):
            self._handle_move_left(dt)
        else:
            self._is_moving = False

    def _handle_move_right(self, dt):
        self._velocity.x += 1.0 * self.speed * dt
        self._reversed = False

    def _handle_move_left(self, dt):
        self._velocity.x += -1.0 * self.speed * dt
        self._reversed = True

    def _handle_move_down(self, dt):
        self._velocity.y += 1.0 * self.speed * dt

    def _handle_jump(self, dt):
        if self.on_ground and self._velocity.y >= 0.0:
            self._velocity.y -= 1.0 * self.jump_force
            self.on_ground = False
            self.animations.request_animation("JUMPING")

    def _handle_primary_action(self, dt):
        if self.primary_attack.can_execute() and self._before_next_attack_counter <= 0.0:
            self.animations.request_animation("PRIMARY_ATTACK")
            self.primary_attack.execute(self.level, self, self.friendly_obj)
            self._before_next_attack_counter = self._before_next_attack_time

    def _handle_secondary_action(self, dt):
        if self.secondary_attack.can_execute() and self._before_next_attack_counter <= 0.0:
            self.animations.request_animation("SECONDARY_ATTACK")
            self.secondary_attack.execute(self.level, self, self.friendly_obj)
            self._before_next_attack_counter = self._before_next_attack_time

    def _check_falling(self, dt):
        if not self.on_ground:
            self.animations.request_animation("FALLING")

    def _check_moving(self, dt):
        if self._is_moving:
            self.animations.request_animation("RUNNING")
        else:
            self.animations.request_animation_stop("RUNNING")
            if self.on_ground:
                self._velocity.x *= 1 - dt * 10
                if self._velocity.y > 0.0:
                    self._velocity.y = 0
            else:
                self._velocity.x *= 1 - dt

    def __repr__(self):
        return str(self._name)




