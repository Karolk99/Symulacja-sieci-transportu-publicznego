from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Thread
from typing import List
import pykka

from typing import TYPE_CHECKING

from simulation_components.observer import Observable
from simulation_components.util.scheduler import Scheduler, Schedulable

if TYPE_CHECKING:
    from simulation_components.passenger import AbstractPassenger
    from simulation_components.map import Route, RouteStop
from simulation_components.vehicle import VehicleState


@dataclass
class RouteToNextStop:
    length: int
    next_stop_id: str
    current_position: int


class AbstractVehicle(pykka.ThreadingActor, Observable, Schedulable, ABC):
    id: int
    delta: float
    capacity: int
    route: Route
    current_route: List[RouteStop]
    passengers: List[AbstractPassenger]

    _position: int = 0
    _iteration_time: float = 1
    _state: VehicleState
    _boarding_timer: int
    _thread_loop: Thread
    _scheduler: Scheduler

    BOARDING_TIME = 1
    SPEED = 2

    def __init__(self):
        super().__init__()
        self.passengers = []
        self.delta = time.time()
        self._position = 0
        self._state = VehicleState.Running
        self._boarding_timer = AbstractVehicle.BOARDING_TIME
        self._scheduler = Scheduler(schedulable=self)

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

    def position(self) -> int:
        return self._position

    def state(self):
        return self._state

    def set_state(self, _state: VehicleState):
        self._state = _state

    def seats_left(self) -> int:
        return self.capacity - len(self.passengers)

    def stops_left(self) -> List[pykka.ActorProxy]:
        stops_left = []
        for route_stop in self.current_route:
            stops_left.append(route_stop.stop)
        return stops_left
