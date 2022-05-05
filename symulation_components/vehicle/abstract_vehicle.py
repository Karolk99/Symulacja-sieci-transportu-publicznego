from __future__ import annotations
import asyncio
import time
from abc import ABC, abstractmethod
from copy import deepcopy, copy
from dataclasses import dataclass
from threading import Thread
from typing import List
import pykka
from enum import Enum

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

    _position: int
    _state: VehicleState
    _boarding_timer: int
    _thread_loop: Thread

    BOARDING_TIME = 1
    SPEED = 2

    def __init__(self):
        super().__init__()
        self._position = 0
        self._state = VehicleState.Idle
        self._boarding_timer = AbstractVehicle.BOARDING_TIME

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



