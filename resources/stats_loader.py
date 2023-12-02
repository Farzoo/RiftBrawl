import json
from typing import Dict, Any, Tuple, List, Callable


class AttackFrame:
    def __init__(self, time_ms: float, size: Tuple[int, int], offset_top_left: Tuple[int, int]):
        self.time_ms = time_ms
        self.size = size
        self.offset_top_left = offset_top_left


class AttackFrameFactory:
    def __init__(self, time_ms: float, size: Tuple[int, int], offset_top_left: Tuple[int, int]):
        self.time_ms = time_ms
        self.size = size
        self.offset_top_left = offset_top_left

    def __call__(self):
        return AttackFrame(self.time_ms, self.size, self.offset_top_left)


class Stats:
    def __init__(self, hitbox_size: Tuple[int, int], health: float, speed: float, jump_force: float):
        self.hitbox_size = hitbox_size
        self.health = health
        self.speed = speed
        self.jump_force = jump_force

class StatsFactory:
    def __init__(self, hitbox_size: Tuple[int, int], health: float, speed: float, jump_force: float):
        self.hitbox_size = hitbox_size
        self.health = health
        self.speed = speed
        self.jump_force = jump_force

    def __call__(self):
        return Stats(
            tuple(self.hitbox_size),  self.health, self.speed, self.jump_force
        )


class StatsLoader:
    @staticmethod
    def load_stats_from_json(filepath: str, scale: float = 1) -> StatsFactory:
        with open(filepath, 'r') as file:
            data = json.load(file)

            hitbox_size = tuple(data["hitbox_size"])
            hitbox_size = (int(hitbox_size[0] * scale), int(hitbox_size[1] * scale))
            health = float(data["health"])
            speed = float(data["speed"]) * scale
            jump_force = float(data["jump_force"]) * scale

            return StatsFactory(hitbox_size, health, speed, jump_force)