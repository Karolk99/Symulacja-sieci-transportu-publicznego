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


class AbstractVehicle(ABC, pykka.ThreadingActor):
    id: int
    capacity: int
    route: Route
    current_route: List[RouteStop]
    passengers: List[AbstractPassenger]

    _position: int
    _state: BusState
    _boarding_timer: int
    _thread_loop: Thread

    BOARDING_TIME = 1
    SPEED = 2

    def __init__(self):
        super().__init__()
        self._position = 0
        self._state = BusState.Idle
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
    def state(self, _state: BusState):
        self._state = _state


class Bus(AbstractVehicle):
    def on_start(self) -> None:
        self._thread_loop = Thread(target=self.run)
        self._thread_loop.start()

    def on_stop(self) -> None:
        self._thread_loop.join()

    def run(self):
        delta = 0.0
        while True:
            # asyncio.run(self.drive(AbstractVehicle.SPEED * (time.time() - delta)))
            asyncio.run(self.drive(AbstractVehicle.SPEED * 1))
            delta = time.time()
            time.sleep(1)

    async def drive(self, distance: float):
        if self._state == BusState.Idle:
            return
        if len(self.current_route) == 0:
            # handle end of route
            return
        # is between stops
        if self._state != BusState.Boarding and self.current_route[0].to_next >= distance:
            self._position += distance
            self.current_route[0].to_next -= distance
        # is boarding
        else:
            await self._handle_stop()

    async def _handle_stop(self):
        self._state = BusState.Boarding
        await ActorRegistry.get_by_urn(self.current_route[0].stop_urn)\
            .proxy()\
            .handle_vehicle(self)
        self.current_route.pop(0)
        self._state = BusState.Running

    def __init__(self, _id: int, route: Route):
        super().__init__()
        self.id = _id
        self.capacity = 10
        self.route = route

        self.current_route = deepcopy(route.topology)
