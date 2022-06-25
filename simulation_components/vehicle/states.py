from enum import Enum


class VehicleState(Enum):
    """
    Utility states that vehicle
    can be in
    """
    Running = 1
    Boarding = 2
    Idle = 3
