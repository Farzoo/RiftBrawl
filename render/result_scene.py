import pygame

from base_game import BaseGame
from player import Player
from resources.resources_manager import ResourcesManager


class ResultScene:

    def __init__(self, winner: Player, game: BaseGame, duration: float = 5.0):
        self.winner = winner
        self.game = game
        self.font = ResourcesManager.font
        self.duration = duration

    def draw(self):
        if self.winner is None or self.winner.has_lost:
            text = "Match Draw"
        else:
            text = "{} Won!".format(self.winner.name)

        text_size = self.font.get_rect(text, size=50).size
        position = ((self.game.window.get_width() - text_size[0]) // 2, (self.game.window.get_height() - text_size[1]) // 2)

        self.font.render_to(self.game.window, position, text, (255, 255, 255), size=50)

    def update(self, dt):
        self.duration -= dt
        if self.duration <= 0:
            self.game.close()