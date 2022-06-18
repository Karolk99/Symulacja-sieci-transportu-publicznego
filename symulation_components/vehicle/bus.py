import asyncio
import logging
import time
from symulation_components.map import Route
from symulation_components.vehicle import VehicleState
from symulation_components.vehicle import AbstractVehicle
from symulation_components.util.scheduler import Scheduler


class Bus(AbstractVehicle):
    """
    Implementation of Bus type vehicle

    # TODO add deleting after finishing root
    """
    def on_start(self) -> None:
        self._scheduler.start()

    def on_stop(self) -> None:
        self._scheduler.stop()

    def run(self):
        raise NotImplementedError

    def tick(self):
        """
        Constant runner inside actor
        with refresh rate 1 second
        :return:
        """
        self.logger.debug(f'running Bus.id={self.id}... {AbstractVehicle.SPEED * (time.time() - self.delta):.2f}')
        asyncio.run(self.drive(AbstractVehicle.SPEED * (time.time() - self.delta)))
        self.delta = time.time()

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
        self.logger = logging.getLogger('simulation_components.vehicle.bus.Bus')
        self._scheduler = Scheduler(schedulable=self, logger=self.logger)
        self.delta = time.time()
        self.id = _id
        self.capacity = capacity
        self.route = route

        self.current_route = route.topology[:]
