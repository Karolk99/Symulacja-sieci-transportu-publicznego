from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Thread
from typing import List
import pykka

from pykka import ActorRegistry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from symulation_components.passenger import AbstractPassenger
    from symulation_components.map import Route, RouteStop
from symulation_components.vehicle import VehicleState


@dataclass
class RouteToNextStop:
    length: int
    next_stop_id: str
    current_position: int


class AbstractVehicle(ABC, pykka.ThreadingActor):
    id: int
    capacity: int
    route: Route
    current_route: List[RouteStop]
    passengers: List[AbstractPassenger]

    _position: int = 0
    _iteration_time: float = 1
    _state: VehicleState
    _boarding_timer: int
    _thread_loop: Thread

    BOARDING_TIME = 1
    SPEED = 2

    def __init__(self):
        super().__init__()
        self._state = VehicleState.Idle
        self._boarding_timer = AbstractVehicle.BOARDING_TIME

    def add_passengers(self, passengers: List[AbstractPassenger]):
        self.passengers.extend(passengers)

    @abstractmethod
    def on_start(self) -> None:
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def drive(self, distance: float):
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
    def state(self, _state: VehicleState):
        self._state = _state

    @property
    def seats_left(self) -> int:
        return self.capacity - len(self.passengers)

    @property
    def stops_left(self) -> List[str]:
        stops_left = []
        for route_stop in self.current_route:
            stops_left.append(route_stop.stop.id.get())
        return stops_left

