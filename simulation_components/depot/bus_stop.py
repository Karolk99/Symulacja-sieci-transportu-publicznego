import logging
from typing import List

import pykka

from simulation_components.counter import Counter
from simulation_components.depot import AbstractStop
from simulation_components.generator import LoadDistribution
from simulation_components.passenger import AbstractPassenger
from simulation_components.vehicle import AbstractVehicle


class BusStop(AbstractStop):
    def handle_vehicle(self, passengers: [AbstractPassenger], possible_stops: [str]):
        """
        Called by vehicle when it reaches this BusStop.
        Only one Vehicle can be on the BusStop at
        the time.
        :param possible_stops:
        :param passengers:
        :return:
        """
        return self.updated_bus_passengers(passengers, possible_stops)

    def get_id(self) -> str:
        return self.id

    def on_stop(self) -> None:
        self.logger.info('Stopping BusStop')

    def updated_bus_passengers(self, passengers: [AbstractPassenger], possible_stops: [str]) -> List[AbstractPassenger]:
        new_passengers = self.getting_on_passengers(possible_stops)
        passengers_staying = self.passengers_staying(passengers)

        return passengers_staying + new_passengers

    @Counter.tape
    def passengers_staying(self, passengers: [AbstractPassenger]) -> List[AbstractPassenger]:
        passengers_staying = []
        for passenger in passengers:
            if passenger.destination != self.id:
                passengers_staying.append(passenger)
        self.update_changing_lines_passengers(passengers_staying)
        return passengers_staying

    @Counter.tape
    def getting_on_passengers(self, possible_stops: [str]) -> List[AbstractPassenger]:
        getting_on_passengers = []
        for passenger in self.passengers:
            current_destination = self.current_destination(possible_stops, passenger)
            if current_destination:
                passenger.current_destination = current_destination
                getting_on_passengers.append(passenger)
                self.passengers.remove(passenger)

        return getting_on_passengers

    def update_changing_lines_passengers(self, passengers_staying: List[AbstractPassenger]) -> None:
        for passenger in passengers_staying:
            if passenger.current_destination == self.id:
                passenger.current_destination = ""
                self.passengers.append(passenger)
                passengers_staying.remove(passenger)

    @staticmethod
    def current_destination(possible_stops: [str], passenger: AbstractPassenger) -> str:
        for stop in reversed(passenger.path):
            if stop in possible_stops:
                return stop
        return ""

    @Counter.tape
    def add_passengers(self, passengers: List[AbstractPassenger]) -> None:
        self.passengers.extend(passengers)

    def __init__(self, _id: str, load: LoadDistribution):
        super().__init__()
        self.id = _id
        self.logger = logging.getLogger(f'simulation_components.depot.bus_stop.BusStop[{self.id}]')
        self.load_distribution = load
        self.passengers = []
