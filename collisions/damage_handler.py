from comps.damage_dealer import DamageDealer
from comps.damageable import Damageable


class DamageCollisionHandler:

    @staticmethod
    def handle_damage_collision(damage_dealer: DamageDealer, damageable: Damageable) -> None:
        damage_dealer.deal_damage(damageable)