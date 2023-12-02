from pygame import Vector2

from base_level import BaseLevel
from collisions.damage_handler import DamageCollisionHandler
from level import Level
from render.parallax_background import ParallaxBackground, Layer
from resources.resources_manager import ResourcesManager
from resources.resources_registry import ResourcesRegistry
from utils.lazy_class_field import LazyClassField
from utils.multi_dispatcher import MultiDispatcher


class LevelFactory:

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args

    def __call__(self):
        return self.fn(*self.args)


class LevelRegistry:

    LevelsFactory = LazyClassField[ResourcesRegistry[str, LevelFactory]](
        lambda: LevelRegistry.get_levels(ResourcesRegistry.ResourceRegistryBuilder[str, LevelFactory]()).build()
    )

    @staticmethod
    def get_levels(builder: ResourcesRegistry.ResourceRegistryBuilder[str, LevelFactory]):
        builder.register("level_1", LevelFactory(LevelRegistry.get_level_1))
        return builder

    @staticmethod
    def get_level_1():
        collision_dispatcher = MultiDispatcher[None].MultiDispatcherBuilder()

        collision_dispatcher.register(DamageCollisionHandler.handle_damage_collision)

        global_scale = ResourcesManager.settings["base_scaling"]
        origin = Vector2(0, 0) * global_scale

        sky_ocean_background = ResourcesManager.backgrounds_textures['background_level_1']
        grass_surface = ResourcesManager.backgrounds_textures['floor']
        tree = ResourcesManager.backgrounds_textures['tree']

        parallax_background = ParallaxBackground([
            Layer(origin, sky_ocean_background, 0.1, "sky_ocean_background", repeat_vertical=False, repeat_horizontal=True),
            Layer(origin + Vector2(0, 40)*global_scale, tree, 1, "tree", repeat_vertical=False, repeat_horizontal=True),
            Layer(origin, grass_surface, 1, "grass_surface", repeat_vertical=False, repeat_horizontal=True),
        ])

        width = sky_ocean_background.get_width() / 2
        height = 1000 * global_scale

        gravity = 1500 * global_scale

        max_velocity_x = 800 * global_scale

        spawn_points = [Vector2(origin.x + i * width / 10, origin.y) for i in range(0, 11)]

        return Level(collision_dispatcher.build(), parallax_background, spawn_points, width, height, gravity, max_velocity_x, origin=origin)