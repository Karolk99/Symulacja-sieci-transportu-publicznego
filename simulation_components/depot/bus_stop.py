import logging
from typing import List

from simulation_components.counter import Counter
from simulation_components.depot import AbstractStop
from simulation_components.generator import LoadDistribution
from simulation_components.passenger import AbstractPassenger
from simulation_components.vehicle import AbstractVehicle


class BusStop(AbstractStop):
    def handle_vehicle(self, vehicle: AbstractVehicle):
        """
        Called by vehicle when it reaches this BusStop.
        Only one Vehicle can be on the BusStop at
        the time.
        :param vehicle:
        :return:
        """
        self.logger.info(f'Handling vehicle {vehicle.id}')
        vehicle.passengers = self.updated_bus_passengers(vehicle)

    def get_id(self) -> str:
        return self.id

    def on_stop(self) -> None:
        self.logger.info('Stopping BusStop')

    def updated_bus_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        new_passengers = self.getting_on_passengers(vehicle)
        passengers_staying = self.passengers_staying(vehicle)

        return passengers_staying + new_passengers

    @Counter.tape
    def passengers_staying(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        passengers_staying = []
        for passenger in vehicle.passengers:
            if passenger.destination != self.id:
                passengers_staying.append(passenger)
        self.update_changing_lines_passengers(passengers_staying)
        return passengers_staying

    @Counter.tape
    def getting_on_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        getting_on_passengers = []
        for passenger in self.passengers:
            current_destination = self.current_destination(vehicle, passenger)
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
    def current_destination(vehicle: AbstractVehicle, passenger: AbstractPassenger) -> str:
        possible_stops = [stop.id.get() for stop in vehicle.stops_left()]
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
