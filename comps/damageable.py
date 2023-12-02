from comps.damage_data import DamageData


class Damageable:

    def __init__(self, health_point: float, friendly_obj: object):
        self._health_point = health_point
        self._max_health_point = health_point
        self._is_dead = False
        self._friendly_obj = friendly_obj

    def take_damage(self, damage_data: DamageData) -> None:
        self._health_point -= damage_data.damage
        if self._health_point <= 0:
            self._is_dead = True
            self._health_point = 0
        if self._health_point > self._max_health_point:
            self._health_point = self._max_health_point

    @property
    def health_percentage(self) -> float:
        return self._health_point / self._max_health_point

    @property
    def health(self) -> float:
        return self._health_point

    @property
    def max_health(self) -> float:
        return self._max_health_point

    @property
    def is_dead(self) -> bool:
        return self._is_dead

    @property
    def friendly_obj(self) -> object:
        return self._friendly_obj


