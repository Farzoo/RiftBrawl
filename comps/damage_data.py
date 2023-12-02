from pygame import Vector2


class DamageData:

    def __init__(self, damage: float, velocity: Vector2):
        self._damage = damage
        self._velocity = velocity

    @property
    def damage(self) -> float:
        return self._damage

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    def __repr__(self):
        return "DamageData(damage={}, velocity={})".format(self._damage, self._velocity)