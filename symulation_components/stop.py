import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import pykka

from passenger import AbstractPassenger


class StopState(Enum):
    EMPTY = 0
    BUSY = 1


class LoadDistribution:
    @staticmethod
    def get_dist(vehicle, route):
        return 2 if vehicle.id == 1 else 1


class AbstractStop(ABC, pykka.ThreadingActor):
    id: str
    passengers: List[AbstractPassenger]
    load_distribution: LoadDistribution

    _state: StopState

    def __init__(self):
        super().__init__()
        self._state = StopState.EMPTY

    @abstractmethod
    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    @abstractmethod
    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass

    @abstractmethod
    def handle_vehicle(self, vehicle):
        pass


class BusStop(AbstractStop):
    def handle_vehicle(self, vehicle):
        while self._state == StopState.BUSY:
            time.sleep(0.01)
        self._state = StopState.BUSY
        time.sleep(LoadDistribution.get_dist(vehicle, vehicle.route))
        # TODO passengers exchange
        self._state = StopState.EMPTY

    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass

    def __init__(self, _id: str):
        super().__init__()
        self.id = _id
