from typing import Optional, Tuple, Dict

from pygame import Surface

from entities.animation import Animation

AnimationType = str


class CharacterAnimation:

    def __init__(self,
                 animations: Dict[AnimationType, Tuple[int, Animation]],
                 current_animation: AnimationType = "IDLE",
                 offset_center: Tuple[int, int] = (0, 0)
                 ):
        self._animations = animations
        self._current_animation = current_animation

        # noinspection PyTypeChecker
        self._animations_pending = (
            [None] * ((max(self._animations.values(), key=lambda x: x[0])[0])+1)
        )  # type: List[Tuple[int, Animation]]

        self._will_restart_current_animation = False
        self._offset_center = offset_center

    @property
    def offset_center(self) -> Tuple[int, int]:
        return self._offset_center

    def request_animation(self, animation_type: AnimationType) -> None:
        anim = self._animations[animation_type]
        self._animations_pending[anim[0]] = (animation_type, anim[1])

    def request_animation_stop(self, animation_type: AnimationType) -> None:
        self._animations_pending[self._animations[animation_type][0]] = None

    def request_animation_restart(self, animation_type: AnimationType) -> None:
        self._animations_pending[self._animations[animation_type][0]] = (animation_type, self._animations[animation_type][1])
        self._animations_pending[self._animations[animation_type][0]][1].reset()

    def get_animation_pending(self, animation_type: AnimationType) -> Optional[Animation]:
        anim = self._animations.get(animation_type, None)
        if anim is None:
            return None
        anim_pending = self._animations_pending[anim[0]]
        if anim_pending is None:
            return None
        return anim_pending[1]

    def process_pending_animations(self, dt) -> None:
        found_first = False
        for i in range(len(self._animations_pending)-1, -1, -1):
            if self._animations_pending[i] is not None:
                anim_type, anim = self._animations_pending[i]
                anim.update(dt)
                if anim.is_finished():
                    anim.reset()
                    self._animations_pending[i] = None
                if not found_first:
                    self._current_animation = anim_type
                    found_first = True

    @property
    def current_animation_type(self) -> str:
        return self._current_animation

    @property
    def current_animation(self) -> Animation:
        return self._animations[self._current_animation][1]

    def get_animation(self, animation_type: AnimationType) -> Animation:
        return self._animations[animation_type][1]

    def update(self, dt: float) -> None:
        self.process_pending_animations(dt)

    def get_frame(self, reversed: bool = False) -> Surface:
        return self._animations[self._current_animation][1].get_frame(reversed)
