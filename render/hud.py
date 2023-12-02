import pygame
from pygame import freetype, Surface
from player import Player
from resources.resources_manager import ResourcesManager


def get_text_surface(text, font_size, font_color=(255, 255, 255), padding=10):
    font = ResourcesManager.font
    text_size = font.get_rect(text, size=font_size).size

    padded_text_size = (text_size[0] + 2 * padding, text_size[1] + 2 * padding)

    padded_text_surface = pygame.Surface(padded_text_size, pygame.SRCALPHA)

    font.render_to(padded_text_surface, (padding, padding), text, font_color, size=font_size)

    return padded_text_surface


def get_health_bar_surface(health_percentage, width, height, fill_color=(255, 0, 0), outline_color=(255, 255, 255),outline_thickness=2):
    fill_width = (width - (outline_thickness * 2)) * health_percentage
    bar_surface = pygame.Surface((width, height))
    bg_rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(bar_surface, outline_color, bg_rect)
    fill_rect = pygame.Rect(outline_thickness, outline_thickness, fill_width, height - (outline_thickness * 2))
    pygame.draw.rect(bar_surface, fill_color, fill_rect)
    return bar_surface


class PlayerHUD:
    def __init__(self, player: Player, health_bar_height_percentage=0.5, padding_x_percentage=0.05, padding_y_percentage=0.01):
        self.player = player
        self.health_bar_height_percentage = health_bar_height_percentage
        self.padding_x_percentage = padding_x_percentage
        self.padding_y_percentage = padding_y_percentage
        self.last_health_percentage = None
        self.last_lives_left = None
        self.health_bar_surface = None
        self.score_surface = None

        self.last_icon = player.character.data.icon
        self.last_icon_surface_ajusted = None

        self.scene_rect = None

    def draw(self, scene: pygame.Surface):
        actual_padding_x = int(scene.get_width() * self.padding_x_percentage)
        actual_padding_y = int(scene.get_height() * self.padding_y_percentage)
        actual_font_size = int(scene.get_height() * self.health_bar_height_percentage)
        actual_health_height = int(scene.get_height() * self.health_bar_height_percentage)

        if self.scene_rect is None or self.scene_rect != scene.get_rect():
            self.scene_rect = scene.get_rect()
            self.score_surface = None
            self.health_bar_surface = None
            self.last_icon_surface_ajusted = None

        if self.last_icon_surface_ajusted is None or self.last_icon != self.player.character.data.icon:
            self.last_icon = self.player.character.data.icon

            new_icon_height = scene.get_height() - 2 * actual_padding_y
            scaling_factor = new_icon_height / self.last_icon.get_height()
            new_icon_width = self.last_icon.get_width() * scaling_factor

            self.last_icon_surface_ajusted = pygame.transform.scale(self.last_icon,(int(new_icon_width), int(new_icon_height)))

        if self.score_surface is None or self.last_lives_left != self.player.lives_left:
            self.score_surface = get_text_surface(str(self.player.lives_left), actual_font_size, font_color=(255, 255, 255),
                                                  padding=actual_padding_y)
            self.score_surface.convert_alpha()
            self.last_lives_left = self.player.lives_left

        health_percentage = self.player.character.health_percentage
        padding_between_health_bar_and_score = int(scene.get_width() * self.padding_x_percentage)

        if health_percentage != self.last_health_percentage:
            health_width = scene.get_width() - self.last_icon_surface_ajusted.get_width() - self.score_surface.get_width() - 4 * actual_padding_x - padding_between_health_bar_and_score
            self.health_bar_surface = get_health_bar_surface(health_percentage, health_width, actual_health_height)
            self.health_bar_surface.convert_alpha()

        half_height = scene.get_height() // 2
        icon_y = half_height - (self.last_icon_surface_ajusted.get_height() // 2)
        health_bar_y = half_height - (self.health_bar_surface.get_height() // 2)
        score_y = half_height - (self.score_surface.get_height() // 2)

        to_blit = (
            (self.last_icon_surface_ajusted, (actual_padding_x, icon_y)),
            (
            self.health_bar_surface, (2 * actual_padding_x + self.last_icon_surface_ajusted.get_width(), health_bar_y)),
            (self.score_surface, (
            3 * actual_padding_x + self.last_icon_surface_ajusted.get_width() + self.health_bar_surface.get_width() + padding_between_health_bar_and_score,
            score_y))
        )
        scene.blits(to_blit)

class HUD:
    def __init__(self,player_HUD : PlayerHUD, padding_x_percentage = 0.01, padding_y_percentage = 0.01):
        self.player_hud = player_HUD
        self.padding_x_percentage = padding_x_percentage
        self.padding_y_percentage = padding_y_percentage

    def draw(self,window : pygame.Surface):
        x_padding = int( window.get_width() * self.padding_x_percentage)
        x_padding = x_padding if x_padding > 0 else 1
        y_padding = int( window.get_height() * self.padding_y_percentage)
        y_padding = y_padding if y_padding > 0 else 1

        hud_subsurface = window.subsurface( pygame.Rect( x_padding,y_padding, window.get_width() - 2 * x_padding, window.get_height() - 2 * y_padding) )

        self.player_hud.draw(hud_subsurface)