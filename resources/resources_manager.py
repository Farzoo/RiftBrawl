from abc import ABC
from typing import Any

import pygame
from pygame import freetype
from pygame.font import Font

from resources.character_loader import CharacterDataFactory, CharacterLoader
from resources.resources_registry import ResourcesRegistry
from resources.settings_loader import SettingsLoader
from resources.textures_loader import TexturesLoader
from utils.lazy_class_field import LazyClassField
from utils.utils import get_project_root


class ResourcesManager(ABC):

    settings \
        = LazyClassField[ResourcesRegistry[str, Any]].create(
            lambda: SettingsLoader.load_settings_from_json(
                get_project_root() + "/assets/settings.json"
            ).build()
        )

    backgrounds_textures \
        = LazyClassField[ResourcesRegistry[str, pygame.Surface]](
            lambda: TexturesLoader.load_textures_from_json(
                get_project_root() + "/assets/textures/backgrounds/backgrounds.json",
                ResourcesManager.settings,
                ResourcesRegistry.ResourceRegistryBuilder()
            ).build()
        )

    characters \
        = LazyClassField[ResourcesRegistry[str, CharacterDataFactory]](
            lambda: CharacterLoader.load_characters_from_json(
                get_project_root() + "/assets/characters/characters.json",
                ResourcesManager.settings,
                ResourcesRegistry.ResourceRegistryBuilder()
            ).build()
        )

    font = LazyClassField[Font](lambda: ResourcesManager.get_font("Grand9K Pixel.ttf", 25))

    @staticmethod
    def get_font(font_name: str, font_size: int) -> Font:
        font = freetype.Font(get_project_root() + "/assets/fonts/" + font_name, font_size)
        font.antialiased = False
        return font





