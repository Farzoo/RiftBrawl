import json
from pathlib import Path
from typing import Tuple, Dict, List

import numpy as np
import pygame
from pygame import Surface

from entities.animation import Animation
from entities.character_animation import CharacterAnimation, AnimationType
from resources.textures_loader import TexturesLoader


class AnimationFactory:

    def __init__(self, images: List[Surface], total_time_seconds: float, loop: int = 1):
        self.images = images
        self.total_time_seconds = total_time_seconds
        self.loop = loop

    def __call__(self):
        return Animation(self.images, self.total_time_seconds, self.loop)


class CharacterAnimationFactory:

    def __init__(self, animations: Dict[AnimationType, Tuple[int, AnimationFactory]], offset_center: Tuple[int, int] = (0, 0)):
        self.animations = animations
        self.offset_center = offset_center

    def __call__(self):
        return CharacterAnimation(
            {anim_type: (priority, anim_factory()) for anim_type, (priority, anim_factory) in self.animations.items()},
            offset_center=self.offset_center
        )


class AnimationLoader:

    @staticmethod
    def load_animations_from_json(filepath: str, scale: float = 1) -> CharacterAnimationFactory:
        with open(filepath, 'r') as file:
            data = json.load(file)
            animations = {}  # type: Dict[AnimationType, Tuple[int, List[Surface], float, int]]
            size_per_frame = tuple(data["size"])
            offset_center = tuple(data["offset_center"])
            offset_center = (int(offset_center[0] * scale), int(offset_center[1] * scale))
            data = data["animations"]
            priority = 0
            for anim_type, anim_data in data.items():
                surfaces = AnimationLoader.load_animations(
                    (Path(filepath).parent / anim_data["file"]).as_posix(),
                    size_per_frame,
                    scale
                )

                animations[str(anim_type)] = (
                    priority,
                    surfaces,
                    float(anim_data["animation_total_time_ms"]) / 1000,
                    1 if bool(anim_data.get("loop", True)) is True else 0
                )
                priority += 1

            animations_factory = {
                anim_type: (priority, AnimationFactory(surfaces, speed, loop))
                for anim_type, (priority, surfaces, speed, loop) in animations.items()
            }

            return CharacterAnimationFactory(animations_factory, offset_center=offset_center)

    @staticmethod
    def load_animations(filepath: str, size: tuple, scale: int) -> List[pygame.Surface]:
        texture = TexturesLoader.texture_loader(filepath)

        num_frames = texture.get_width() // size[0]

        animation = [
            AnimationLoader.reduce_image_fast(texture.subsurface(pygame.Rect(x * size[0], 0, size[0], size[1])))
            for x in range(num_frames)
        ]

        animation = [
            pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale)).convert_alpha() for
            image in animation]

        return animation

    import pygame

    @staticmethod
    def reduce_image(image) -> pygame.Surface:
        width, height = image.get_size()

        min_x, min_y = width, height
        max_x, max_y = 0, 0

        for x in range(width):
            for y in range(height):
                if image.get_at((x, y))[3] != 0:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        new_width = max_x - min_x + 1
        new_height = max_y - min_y + 1

        new_image = image.subsurface((min_x, min_y, new_width, new_height))

        return new_image

    @staticmethod
    def reduce_image_fast(image):
        np_image = pygame.surfarray.pixels_alpha(image)

        alpha_indices = np.argwhere(np_image != 0)

        min_x, min_y = alpha_indices.min(axis=0)
        max_x, max_y = alpha_indices.max(axis=0)

        new_width = max_x - min_x + 1
        new_height = max_y - min_y + 1

        new_image = image.subsurface((min_x, min_y, new_width, new_height))

        return new_image
