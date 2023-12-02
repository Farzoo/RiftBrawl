from typing import List

import pygame
from pygame import Rect

from resources.stats_loader import AttackFrame


class AttackTrajectory:
    def __init__(self, frames: List[AttackFrame]):
        self.frames = frames
        self.rects = [Rect(frame.offset_top_left, frame.size) for frame in frames]
        self.total_duration = sum([frame.time_ms for frame in frames])
        self.elapsed_time = 0
        self.current_segment = 0
        self._current_rect = self.rects[0]  # Copie du premier Rect pour commencer
        self._is_finished = False

    def update(self, dt):
        self.elapsed_time += dt * 1000
        if self.elapsed_time >= self.frames[self.current_segment].time_ms:
            self.elapsed_time = 0
            self.current_segment += 1
            if self.current_segment < len(self.rects):
                self._current_rect = self.rects[self.current_segment]
            else:
                self._is_finished = True

    def reset(self):
        self.elapsed_time = 0
        self.current_segment = 0
        self._current_rect = self.rects[0]
        self._is_finished = False

    @property
    def current_rect(self):
        return Rect(self._current_rect)

    def is_complete(self):
        return self._is_finished
