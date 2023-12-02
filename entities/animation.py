from typing import List

import pygame
from pygame import Surface


class Animation:

    def __init__(self, images: List[Surface], total_time_seconds: float, loop: int = 1):
        self._right_images = images
        self._left_images = [pygame.transform.flip(image, True, False) for image in images]
        self.speed = total_time_seconds / len(images)
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.loop = loop
        self._is_finished = False

    @property
    def default_image(self) -> Surface:
        return self._right_images[0]

    def update(self, dt: float) -> None:
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.speed:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1)
            should_loop = self.current_frame == len(self._right_images)
            if should_loop:
                if self.loop == 1:
                    self.current_frame = 0
                else:
                    self.current_frame -= 1
            if self.current_frame == len(self._right_images) - 1:
                self._is_finished = True


    def is_finished(self) -> bool:
        return self._is_finished

    def get_frame(self, reversed: bool) -> Surface:
        if reversed:
            return self._left_images[self.current_frame]
        else:
            return self._right_images[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.time_since_last_frame = 0
        self._is_finished = False

