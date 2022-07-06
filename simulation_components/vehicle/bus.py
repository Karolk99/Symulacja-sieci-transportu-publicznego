import logging
import time

from simulation_components.counter import Counter
from simulation_components.map import Route
from simulation_components.observer import Observer
from simulation_components.passenger import AbstractPassenger
from simulation_components.vehicle import VehicleState
from simulation_components.vehicle import AbstractVehicle
from simulation_components.util.scheduler import Scheduler


class Bus(AbstractVehicle):
    """
    Implementation of Bus type vehicle

    # TODO add deleting after finishing root
    """

    def info_(self):
        return self.id, self.current_route[0].stop, self.passengers

    def on_start(self) -> None:
        self._scheduler.start()

    def on_stop(self) -> None:
        self._scheduler.stop()

    def run(self):
        raise NotImplementedError

    @Observer.observe
    def tick(self):
        """
        Constant runner inside actor
        with refresh rate 1 second
        :return:
        """
        self.logger.debug(f'running Bus.id={self.id}... {AbstractVehicle.SPEED * (time.time() - self.delta):.2f}')
        self.drive(AbstractVehicle.SPEED * (time.time() - self.delta))
        self.delta = time.time()

    def drive(self, distance: float) -> None:
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
        if self._state == VehicleState.Running and self.current_route[0].to_next >= distance:
            self._position += distance
            self.current_route[0].to_next -= distance
        # is boarding
        else:
            self._handle_stop()

    @Observer.observe
    @Counter.tape
    def _handle_stop(self):
        """
        When bus reaches bus stop
        this method carries necessary steps
        :return:
        """
        stop_id = self.current_route[0].stop.id.get()
        self.logger.debug(f'arrived to {stop_id}; stops left {len(self.current_route)} psg={len(self.passengers)}')
        self._state = VehicleState.Boarding
        stops_left = [stop.id.get() for stop in self.stops_left()]
        self.passengers = self.current_route[0].stop.handle_vehicle(self.passengers, stops_left).get()
        self.current_route.pop(0)
        self.logger.debug(f'leaving {stop_id}; stops left {len(self.current_route)} psg={len(self.passengers)}')
        # last stop
        if not self.current_route:
            self.logger.info(f'Bus stopped; passengers left: {len(self.passengers)}')
            self.stop()
        self._state = VehicleState.Running
        self._thread_hook = None

    @Counter.tape
    def set_passengers(self, passengers: [AbstractPassenger]):
        self.passengers = passengers

    def __init__(self, _id: int, route: Route, capacity: int):
        super().__init__()
        self.id = _id
        self.logger = logging.getLogger(f'simulation_components.vehicle.bus.Bus{self.id}')
        self._scheduler = Scheduler(schedulable=self, logger=self.logger)
        self.delta = time.time()
        self.capacity = capacity
        self.route = route

        self.current_route = route.topology[:]
