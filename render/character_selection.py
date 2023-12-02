from math import sqrt, ceil

import pygame
from game import Game
from key_bindings import Command, player1_key_mapping, player2_key_mapping
from resources.resources_manager import ResourcesManager


class CharacterSelectionScene:
    def __init__(self, screen):
        self.screen = screen
        self.characters = list(ResourcesManager.characters.keys())
        self.n_icons = len(self.characters)
        self.n_cols = int(sqrt(self.n_icons))
        self.n_rows = int(ceil(self.n_icons / self.n_cols))
        self.grid_cell_width = self.screen.get_width() // self.n_cols
        self.grid_cell_height = self.screen.get_height() // self.n_rows
        self.character_icons = []
        self.padding = 20
        self.font = pygame.font.Font(None, 24)

        for name in self.characters:
            icon = ResourcesManager.characters[name].icon
            scale_factor = min((self.grid_cell_width - 2 * self.padding) / icon.get_width(),
                               (self.grid_cell_height - 2 * self.padding) / icon.get_height())
            scaled_icon = pygame.transform.scale(
                icon, (round(icon.get_width() * scale_factor), round(icon.get_height() * scale_factor))
            )
            self.character_icons.append(scaled_icon)
            self.selected_character1 = 0
            self.selected_character2 = 0

    def draw_scene(self):
        self.screen.fill((0, 0, 0))
        for idx, icon in enumerate(self.character_icons):
            pos_x = (idx % self.n_cols * self.grid_cell_width + self.padding +
                     (self.grid_cell_width - 2 * self.padding - icon.get_width()) // 2)
            pos_y = (idx // self.n_cols * self.grid_cell_height + self.padding)

            # Currently selected character for player 1
            if idx == self.selected_character1:
                color = (0, 0, 255)  # blue for player 1 selection
                pygame.draw.rect(self.screen, color, pygame.Rect(pos_x, pos_y, icon.get_width(), icon.get_height()),
                                 4)

            # Currently selected character for player 2
            if idx == self.selected_character2:
                color = (255, 0, 0)  # red for player 2 selection
                pygame.draw.rect(self.screen, color, pygame.Rect(pos_x, pos_y, icon.get_width(), icon.get_height()),
                                 4)

            # Character name
            text = self.font.render(self.characters[idx], True, (255, 255, 255))
            text_pos = text.get_rect(centerx=pos_x + icon.get_width() / 2,
                                     top=pos_y + icon.get_height() + 10)
            self.screen.blit(text, text_pos)

            self.screen.blit(icon, (pos_x, pos_y))

        text = self.font.render("Press ENTER to start the game", True, (255, 255, 255))
        text_pos = text.get_rect(centerx=self.screen.get_width() / 2, centery=self.screen.get_height() - 50)
        self.screen.blit(text, text_pos)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if player1_key_mapping.get(event.key) == Command.MOVE_LEFT and self.selected_character1 % self.n_cols > 0:
                self.selected_character1 -= 1
            elif player1_key_mapping.get(event.key) == Command.MOVE_RIGHT and self.selected_character1 % self.n_cols < self.n_cols - 1:
                self.selected_character1 += 1
            elif player1_key_mapping.get(event.key) in (Command.MOVE_UP, Command.JUMP) and self.selected_character1 // self.n_cols > 0:
                self.selected_character1 -= self.n_cols
            elif player1_key_mapping.get(event.key) == Command.MOVE_DOWN and self.selected_character1 // self.n_cols < self.n_rows - 1:
                self.selected_character1 += self.n_cols

            elif player2_key_mapping.get(event.key) == Command.MOVE_LEFT and self.selected_character2 % self.n_cols > 0:
                self.selected_character2 -= 1
            elif player2_key_mapping.get(event.key) == Command.MOVE_RIGHT and self.selected_character2 % self.n_cols < self.n_cols - 1:
                self.selected_character2 += 1
            elif player2_key_mapping.get(event.key) in (Command.MOVE_UP, Command.JUMP) and self.selected_character2 // self.n_cols > 0:
                self.selected_character2 -= self.n_cols
            elif player2_key_mapping.get(event.key) == Command.MOVE_DOWN and self.selected_character2 // self.n_cols < self.n_rows - 1:
                self.selected_character2 += self.n_cols

            elif event.key == pygame.K_RETURN:
                if (self.selected_character1 is not None) and (self.selected_character2 is not None):
                    try:
                        return (self.characters[self.selected_character1], self.characters[self.selected_character2])
                    except IndexError:
                        pass
    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
                result = self.handle_event(event)
                if result:
                    return result
            self.draw_scene()