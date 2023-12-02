from typing import Any, Tuple, Dict


class AttackFrame:
    def __init__(self, time_ms: float, size: Tuple[int, int], offset_top_left: Tuple[int, int]):
        self.time_ms = time_ms
        self.size = size
        self.offset_top_left = offset_top_left


class AttackFrameFactory:

    def __init__(self, time_ms_fraction: float, size: Tuple[int, int], offset_top_left: Tuple[int, int]):
        self.time_ms = time_ms_fraction
        self.size = size
        self.offset_top_left = offset_top_left

    def __call__(self) -> AttackFrame:
        return AttackFrame(self.time_ms, self.size, self.offset_top_left)


class AttackFrameLoader:

    @staticmethod
    def load_attack_frame(data: Dict[str, Any], frame_time_ms: float, default_time_ms_fraction: float, scale: int = 1
                          ) -> AttackFrameFactory:
        try:
            time_ms_fraction = float(data.get("time_ms_fraction", default_time_ms_fraction))
            size = tuple(data["size"])
            size = (int(size[0] * scale), int(size[1] * scale))
            offset_center = tuple(data["offset_center"])
            offset_center = (int(offset_center[0] * scale), int(offset_center[1] * scale))
            return AttackFrameFactory(time_ms_fraction * frame_time_ms, size, offset_center)
        except KeyError as e:
            raise ValueError("Invalid data dictionary, missing key: {}".format(str(e)))
