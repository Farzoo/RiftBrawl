import json
from typing import Any, Callable, Dict, List

import pygame

from base_level import BaseLevel
from entities.animation import Animation
from entities.attack_trajectory import AttackTrajectory
from entities.base_attack import BaseAttackExecutor
from entities.entity import Entity
from entities.melee_attack import MeleeAttack
from resources.attack_frame_loader import AttackFrameLoader
from resources.stats_loader import AttackFrameFactory


class MeleeAttackFactory:

    def __init__(
            self, trajectory: Callable[[], AttackTrajectory], animation: Animation, health: float, damage: float
    ):
        self.trajectory = trajectory
        self.animation = animation
        self.health = health
        self.damage = damage

    def __call__(self, level: BaseLevel, owner: Entity, friend_obj):
        return MeleeAttack(level, owner, self.trajectory(), self.animation, self.health, self.damage, friend_obj)

class MeleeAttackExecutorFactory:

        def __init__(self, attack_factory: MeleeAttackFactory, cooldown: float):
            self.attack_factory = attack_factory
            self.cooldown = cooldown

        def __call__(self) -> MeleeAttack.MeleeAttackExecutor:
            return MeleeAttack.MeleeAttackExecutor(self.attack_factory, self.cooldown)


class AttackTrajectoryFactory:

        def __init__(self, frames_factory: List[AttackFrameFactory]):
            self.frames_factory = frames_factory

        def __call__(self):
            return AttackTrajectory([frame() for frame in self.frames_factory])


class AttackLoader:

    @staticmethod
    def load_attacks_from_json(filepath: str, scale: float = 1) -> Dict[str, Callable[[], BaseAttackExecutor]]:
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                attacks_factory = {}
                for attack_name, attack_data in data.items():
                    attack_data["scale"] = scale
                    attacks_factory[attack_name] = AttackLoader.load_attack(attack_data)
                return attacks_factory
        except Exception as e:
            raise ValueError("Invalid data dictionary: {}".format(str(e)))

    @staticmethod
    def load_attack(data: Dict[str, Any]) -> Callable[[], BaseAttackExecutor]:
        attack_type = data["type"]
        if attack_type == "MELEE":
            return AttackLoader.load_weapon_attack(data)
        else:
            raise ValueError("Invalid attack type: {}".format(attack_type))

    @staticmethod
    def load_weapon_attack(data: Dict[str, Any]) -> Callable[[], MeleeAttack.MeleeAttackExecutor]:
        cooldown = float(data["cooldown"])
        trajectory_data = data["trajectory"]
        trajectory_data["scale"] = data["scale"]
        trajectory = AttackLoader.load_attack_trajectory(trajectory_data)
        animation = Animation([pygame.Surface((0, 0))], 0, 0)
        health = float(data["health"])
        damage = float(data["damage"])
        return MeleeAttackExecutorFactory(
            MeleeAttackFactory(trajectory, animation, health, damage),
            cooldown
        )

    @staticmethod
    def load_attack_trajectory(trajectory_data: Dict[str, Any]) -> AttackTrajectoryFactory:
        frame_time_ms = float(trajectory_data["frame_time_ms"])
        default_time_ms_fraction = float(trajectory_data["default_time_ms_fraction"])
        frames_data = trajectory_data["frames"]
        scale = trajectory_data["scale"]

        frames_factory = [
            AttackFrameLoader.load_attack_frame(frame_data, frame_time_ms, default_time_ms_fraction, scale=scale)
            for frame_data in frames_data
        ]

        return AttackTrajectoryFactory(frames_factory)


