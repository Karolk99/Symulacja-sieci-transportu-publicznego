from typing import List

from symulation_components.depot import AbstractStop
from symulation_components.generator import LoadDistribution
from symulation_components.passenger import AbstractPassenger
from symulation_components.vehicle import AbstractVehicle


class BusStop(AbstractStop):
    def handle_vehicle(self, vehicle: AbstractVehicle):
        """
        Called by vehicle when it reaches this BusStop.
        Only one Vehicle can be on the BusStop at
        the time.
        :param vehicle:
        :return:
        """
        self.update_changing_lines_passengers(vehicle)
        vehicle.passengers = self.updated_bus_passengers(vehicle)

    def update_changing_lines_passengers(self, vehicle: AbstractVehicle) -> None:
        for passenger in vehicle.passengers:
            if passenger.current_destination == self.id:
                passenger.current_destination = ""
                self.passengers.append(passenger)
                vehicle.passengers.remove(passenger)

    def updated_bus_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        new_passengers = self.getting_on_passengers(vehicle)
        passengers_staying = self.passengers_staying(vehicle)

        return passengers_staying + new_passengers

    def passengers_staying(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        passengers_staying = []
        for passenger in vehicle.passengers:
            if passenger.destination != self.id:
                passengers_staying.append(passenger)

        return passengers_staying

    def getting_on_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        getting_on_passengers = []
        for passenger in self.passengers:
            current_destination = self.current_destination(vehicle, passenger)
            if current_destination:
                passenger.current_destination = current_destination
                getting_on_passengers.append(passenger)
                self.passengers.remove(passenger)

        return getting_on_passengers

    @staticmethod
    def current_destination(vehicle: AbstractVehicle, passenger: AbstractPassenger) -> str:
        possible_stops = vehicle.stops_left
        for stop in reversed(passenger.path):
            if stop in possible_stops:
                return stop
        return ""

    def add_passengers(self, passengers: List[AbstractPassenger]) -> None:
        self.passengers.extend(passengers)

    def __init__(self, _id: str, load: LoadDistribution):
        super().__init__()
        self.id = _id
        self.load_distribution = load
        self.passengers = []
