from pygame import Vector2

from comps.damage_data import DamageData
from comps.damageable import Damageable


class DamageDealer:

    def __init__(self, damage: float, friendly_obj: object):
        self._damage = damage
        self._friendly_obj = friendly_obj

    def is_friendly(self, damageable: Damageable) -> bool:
        return self.friendly_obj == damageable.friendly_obj


    def deal_damage(self, damageable: Damageable) -> None:
        if not self.is_friendly(damageable):
            damageable.take_damage(DamageData(self.damage, Vector2(0, 0)))


    @property
    def friendly_obj(self) -> object:
        return self._friendly_obj

    @property
    def damage(self) -> float:
        return self._damage