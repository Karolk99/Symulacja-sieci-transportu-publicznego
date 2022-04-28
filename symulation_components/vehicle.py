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


class BusState(Enum):
    Running = 1
    Boarding = 2
    Idle = 3


class AbstractVehicle(ABC):
    id: int
    capacity: int
    route: Route
    current_route: List[RouteStop]
    passengers: List[AbstractPassenger]

    _position: int
    _state: BusState
    _boarding_timer: int

    BOARDING_TIME = 5

    def __init__(self):
        self._position = 0
        self._state = BusState.Idle
        self._boarding_timer = AbstractVehicle.BOARDING_TIME

    @abstractmethod
    def drive(self, distance: int):
        pass

    @abstractmethod
    def _handle_stop(self) -> None:
        pass

    @property
    def position(self) -> int:
        return self._position

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, _state: BusState):
        self._state = _state


class Bus(AbstractVehicle):
    def drive(self, distance: int):
        if self._state == BusState.Idle:
            return
        if len(self.current_route) == 0:
            # handle end of route
            return
        # is between stops
        if self._state != BusState.Boarding and self.current_route[0].to_next >= distance:
            self._position += int(distance)
            self.current_route[0].to_next -= distance
        # is boarding
        else:
            self._handle_stop()

    def _handle_stop(self):
        if self._boarding_timer == AbstractVehicle.BOARDING_TIME:
            self._state = BusState.Boarding
        if self._boarding_timer == 0:
            self._state = BusState.Running
            self.current_route.pop(0)
            self._position += 1
            self._boarding_timer = AbstractVehicle.BOARDING_TIME + 1
        self._boarding_timer -= 1

    def __init__(self, _id: int, route: Route):
        super().__init__()
        self.id = _id
        self.capacity = 10
        self.route = route

        self.current_route = deepcopy(route.topology)
