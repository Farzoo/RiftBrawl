from enum import Enum

import pygame


class Command(Enum):
    MOVE_RIGHT = 0
    MOVE_LEFT = 1
    JUMP = 2
    MOVE_DOWN = 3
    PRIMARY_ACTION = 4
    SECONDARY_ACTION = 5
    MOVE_UP = 6


player1_key_mapping = {
    pygame.K_d: Command.MOVE_RIGHT,
    pygame.K_q: Command.MOVE_LEFT,
    pygame.K_SPACE: Command.JUMP,
    pygame.K_s: Command.MOVE_DOWN,
    pygame.K_z: Command.MOVE_UP,
    pygame.K_f: Command.PRIMARY_ACTION,
    pygame.K_g: Command.SECONDARY_ACTION,
}

player2_key_mapping = {
    pygame.K_RIGHT: Command.MOVE_RIGHT,
    pygame.K_LEFT: Command.MOVE_LEFT,
    pygame.K_UP: Command.JUMP,
    pygame.K_DOWN: Command.MOVE_DOWN,
    pygame.K_l: Command.PRIMARY_ACTION,
    pygame.K_m: Command.SECONDARY_ACTION,
}

