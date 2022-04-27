from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import List
from enum import Enum
from passenger import AbstractPassenger
from symulation_components.map import Route, RouteStop


@dataclass
class RouteToNextStop:
    length: int
    next_stop_id: str
    current_position: int


class AbstractVehicle(ABC):
    id: int
    capacity: int
    route: Route
    _position: int
    current_route: List[RouteStop]
    passengers: List[AbstractPassenger]

    @abstractmethod
    def drive(self, distance: int):
        pass

    @abstractmethod
    def _handle_stop(self) -> None:
        pass

    @property
    def position(self) -> int:
        return self._position


class BusState(Enum):
    Running = 1
    Stopped = 2


class Bus(AbstractVehicle):
    def drive(self, distance: int):
        if len(self.current_route) == 0:
            # handle end of route
            return
        if self.current_route[0].to_next >= distance:
            self._position += int(distance)
            self.current_route[0].to_next -= distance
        else:
            self._handle_stop()

    def _handle_stop(self) -> None:
        self._position += 1
        self.current_route.pop(0)

    def __init__(self, _id: int, route: Route):
        self.id = _id
        self.capacity = 10
        self.route = route
        self._position = 0

        self.current_route = deepcopy(route.topology)
