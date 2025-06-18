from dataclasses import dataclass
import enum


class MotorEvent(enum.Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    STOP = "stop"
    SET_SPEED = "set_speed"

    def __str__(self):
        return self.value


@dataclass(kw_only=True)
class MotorThreshold:
    speed_pct: float
    critical_temp: float
