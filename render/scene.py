
import itertools
from typing import Iterable, Tuple

import pygame
from pygame import Vector2, Surface, Rect, SurfaceType
from pygame.rect import RectType

from base_game import BaseGame
from base_level import BaseLevel
from render.camera import Camera
from render.hud import HUD, PlayerHUD
from render.parallax_background import ParallaxBackground


class Scene:

    def __init__(self, game: BaseGame):
        self.game = game
        self.game.on_resize += self.resize

        self.camera1 = Camera(game.window, (0, 0), 0, 0, self.game.level)
        self.camera2 = Camera(game.window, (0, 0), 0, 0, self.game.level)

        self.line_pos = ((0, 0), (0, 0))

        self.HUD_cam1 = HUD(PlayerHUD(self.game.player1))
        self.HUD_cam2 = HUD(PlayerHUD(self.game.player2))

        self.resize(self.game.window)

    def update(self, dt):
        if self.game.player1.character is not None:
            self.camera1.update(self.game.player1.character.box.rect.midbottom)
        else:
            self.camera1.update(self.game.level.origin)

        if self.game.player2.character is not None:
            self.camera2.update(self.game.player2.character.box.rect.midbottom)
        else:
            self.camera2.update(self.game.level.origin)

    def draw(self):
        self._draw_camera(self.camera1)
        self._draw_camera(self.camera2)


        self._draw_hud(self.HUD_cam1, self.camera1)
        self._draw_hud(self.HUD_cam2, self.camera2)

        self._draw_line(self.game.window)

    def _draw_hud(self, hud: HUD, camera: Camera):
        hud_surface = camera.camera_surface.subsurface(Rect(0, 0, camera.width/3, camera.height/5))
        hud.draw(hud_surface)

    def _draw_line(self, window: Surface):
        line_width = window.get_width() // 100
        pygame.draw.line(window, (0, 0, 0), self.line_pos[0], self.line_pos[1], line_width)

    def _draw_camera(self, camera: Camera):
        self.game.level.background.draw(camera)

        camera.draw(
            *self._flatten_layers([(entity.layers, entity.image_rect) for entity in self.game.level.get_entities()])
        )
       # camera.draw(
            #[[self._create_mask(entity.rect), entity.rect] for entity in self.game.level.get_entities()]
        #)

        camera.finish_draw()


    def resize(self, display: Surface):
        width, height = display.get_size()
        self.camera1.rect.topleft = (0, 0)
        self.camera1.width = width
        self.camera1.height = height / 2
        self.camera1.display_surface = display

        self.camera2.rect.topleft = (0, height / 2)
        self.camera2.width = width
        self.camera2.height = height / 2
        self.camera2.display_surface = display

        self.line_pos = ((0, height / 2), (width, height / 2))

        self.HUD_cam1.padding_x_percentage = height/width * 0.1
        self.HUD_cam1.padding_y_percentage = width/height * 0.15

        self.HUD_cam2.padding_x_percentage = height/width * 0.1
        self.HUD_cam2.padding_y_percentage = width/height * 0.15

    @staticmethod
    def _flatten_layers(list_of_layers: Iterable[Tuple[Iterable['Surface | SurfaceType'], 'Rect | RectType']]) \
            -> Iterable[Tuple['Surface | SurfaceType', 'Rect | RectType']]:
        return ((surface, rect) for iterable, rect in list_of_layers for surface in iterable)

    @staticmethod
    def _create_mask(rect: Rect, color: Tuple[int, int, int] = (255, 0, 0, 0)) -> Surface:
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)  # Use pygame.SRCALPHA to handle alpha
        surface.fill((255, 255, 255, 50))  # Change the alpha value to the level of translucency required
        return surface
