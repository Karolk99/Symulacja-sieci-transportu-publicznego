import asyncio
import time
from copy import deepcopy
from threading import Thread

from symulation_components.map import Route
from symulation_components.vehicle import VehicleState
from symulation_components.vehicle import AbstractVehicle


class Bus(AbstractVehicle):
    """
    Implementation of Bus type vehicle
    """
    def on_start(self) -> None:
        self._thread_loop = Thread(target=self.run)
        self._thread_loop.start()

    def on_stop(self) -> None:
        self._thread_loop.join()

    def run(self):
        """
        Constant runner inside actor
        with refresh rate 1 second
        :return:
        """
        delta = 0.0
        while True:
            asyncio.run(self.drive(AbstractVehicle.SPEED * (time.time() - delta)))
            delta = time.time()
            time.sleep(self._iteration_time)

    async def drive(self, distance: float) -> None:
        """
        async method that changes position of bus.
        If bus reaches bus stop it calls
        appropriate bus stop agent and waits till
        passengers are handled.
        :param distance: how far bus has driven
        :return: None
        """
        if self._state == VehicleState.Idle:
            return
        if len(self.current_route) == 0:
            # handle end of route
            return
        # is between stops
        if self._state != VehicleState.Boarding and self.current_route[0].to_next >= distance:
            self._position += distance
            self.current_route[0].to_next -= distance
        # is boarding
        else:
            await self._handle_stop()

    async def _handle_stop(self):
        """
        When bus reaches bus stop
        this method carries necessary steps
        :return:
        """
        self._state = VehicleState.Boarding
        await self.current_route[0].stop.handle_vehicle(self)
        self.current_route.pop(0)
        self._state = VehicleState.Running

    def __init__(self, _id: int, route: Route, capacity: int):
        super().__init__()
        self.id = _id
        self.capacity = capacity
        self.route = route

        self.current_route = deepcopy(route.topology)
