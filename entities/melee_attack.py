from typing import Callable

from pygame import Vector2

from base_level import BaseLevel
from comps.damage_data import DamageData
from comps.damage_dealer import DamageDealer
from comps.damageable import Damageable
from entities.animation import Animation
from entities.attack_trajectory import AttackTrajectory
from entities.base_attack import BaseAttackExecutor
from entities.entity import Entity


class MeleeAttack(Entity, DamageDealer, Damageable):

    def KNOCKBACK_FORCE(self, x: float = 1.0, y: float = 1.0) -> Vector2:
        return Vector2(x*self._owner.box.width*5, -y*self._owner.box.height*3)

    def can_continue(self):
        return not self._trajectory.is_complete()

    def __init__(self,
                 level: BaseLevel,
                 owner: Entity,
                 trajectory: AttackTrajectory,
                 animation: Animation,
                 health: float,
                 damage: float,
                 friend_obj
                 ):
        Entity.__init__(self, level)
        DamageDealer.__init__(self, damage, friend_obj)
        Damageable.__init__(self, health, friend_obj)
        self._owner = owner
        self._trajectory = trajectory
        self._animation = animation
        self._elapsed_time = 0
        self._rect = trajectory.current_rect  # hitbox

    def update(self, dt: float) -> None:
        if not self.can_continue():
            self.destroy()
            return

        self._animation.update(dt)

        self._trajectory.update(dt)
        self.box.rect = self._trajectory.current_rect

        # Ajuste la position en fonction de la direction de l'owner
        if self._owner.reversed:  # Si l'owner est tourné vers la gauche
            self.box.center = (self._owner.rect.centerx - self.rect.x, self._owner.rect.centery + self.rect.y)
        else:  # Si l'owner est tourné vers la gauche
            self.box.center = (self._owner.rect.centerx + self.rect.x, self._owner.rect.centery + self.rect.y)

    @property
    def image_rect(self):
        return self.image.get_rect(center=self.rect.center)

    @property
    def image(self):
        return self._animation.get_frame(self.reversed)

    def deal_damage(self, damageable: Damageable) -> None:
        if not self.is_friendly(damageable):
            damageable.take_damage(DamageData(self.damage, self.calculate_knockback()))

    def take_damage(self, damage_data: DamageData) -> None:
        super().take_damage(damage_data)
        if self.is_dead:
            self.destroy()

    def calculate_knockback(self) -> Vector2:
        return self.KNOCKBACK_FORCE(x=-1 if self._owner.reversed else 1).elementwise() + (self._owner._velocity * 0.5)

    class MeleeAttackExecutor(BaseAttackExecutor):

        def cancel(self):
            if self._current_attack is not None:
                self._current_attack.destroy()

        def __init__(self, attack: Callable[[BaseLevel, Entity, object], 'MeleeAttack'], cooldown: float):
            self._attack_factory = attack
            self._cooldown = cooldown
            self._elapsed_time = 0.0
            # noinspection PyTypeChecker
            self._current_attack = None  # type: MeleeAttack

        def update(self, dt: float):
            self._elapsed_time -= dt

        def execute(self, level: BaseLevel, owner: Entity, friend_obj):
            if self.can_execute():
                if self._current_attack is not None:
                    self._current_attack.destroy()
                self._elapsed_time = self._cooldown
                self._current_attack = self._attack_factory(level, owner, friend_obj)
                level.add_entity(self._current_attack)

        def can_execute(self):
            return self._elapsed_time <= 0.0


