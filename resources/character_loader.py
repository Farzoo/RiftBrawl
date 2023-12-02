import json
from pathlib import Path
from typing import Callable, Any

from pygame import Surface

from entities.base_attack import BaseAttackExecutor
from entities.character_animation import CharacterAnimation
from resources.animation_loader import AnimationLoader
from resources.attack_loader import AttackLoader
from resources.resources_registry import ResourcesRegistry
from resources.stats_loader import Stats, StatsLoader
from resources.textures_loader import TexturesLoader


class CharacterData:

    def __init__(self, name: str, icon: Surface, animation: CharacterAnimation, stats: Stats, primary_attack: BaseAttackExecutor, secondary_attack: BaseAttackExecutor):
        self.name = name
        self.icon = icon
        self.animations = animation
        self.stats = stats
        self.primary_attack = primary_attack
        self.secondary_attack = secondary_attack

class CharacterDataFactory:

    def __init__(self,
                 name: str,
                 icon: Surface,
                 animation_factory: Callable[[], CharacterAnimation],
                 stats_factory: Callable[[], Stats],
                 primary_attack_factory: Callable[[], BaseAttackExecutor],
                 secondary_attack_factory: Callable[[], BaseAttackExecutor]
                 ):
        self.name = name
        self.icon = icon
        self.animation_factory = animation_factory
        self.stats_factory = stats_factory
        self.primary_attack_factory = primary_attack_factory
        self.secondary_attack_factory = secondary_attack_factory

    def __call__(self):
        return CharacterData(self.name, self.icon.copy(), self.animation_factory(), self.stats_factory(), self.primary_attack_factory(), self.secondary_attack_factory())


class CharacterLoader:

    @staticmethod
    def load_characters_from_json(
            filepath: str,
            settings: ResourcesRegistry[str, Any],
            builder: ResourcesRegistry.ResourceRegistryBuilder[str, CharacterDataFactory]
    ) -> ResourcesRegistry.ResourceRegistryBuilder[str, CharacterDataFactory]:
        with open(filepath, 'r') as file:
            data = json.load(file)
            global_scaling = float(settings["base_scaling"])
            for entity_info in data["characters"]:
                relative_path = entity_info["folder_relative_path"]
                scale = float(entity_info["scale"])
                scale *= global_scaling

                icon = TexturesLoader.texture_loader((Path(filepath).parent / relative_path / "Icon.png").as_posix())

                anim_factory = \
                    AnimationLoader.load_animations_from_json((Path(filepath).parent / relative_path / "animations.json").as_posix(), scale)

                stats_factory = \
                    StatsLoader.load_stats_from_json((Path(filepath).parent / relative_path / "stats.json").as_posix(), scale)

                attacks_factory = \
                    AttackLoader.load_attacks_from_json((Path(filepath).parent / relative_path / "attacks.json").as_posix(), scale)

                builder.register(
                    entity_info["name"],
                    CharacterDataFactory(
                        entity_info["name"],
                        icon,
                        anim_factory,
                        stats_factory,
                        attacks_factory["primary_attack"],
                        attacks_factory["secondary_attack"]
                    )
                )

        return builder
