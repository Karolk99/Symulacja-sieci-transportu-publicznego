import time
from typing import List

from symulation_components.depot import AbstractStop, StopState
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
        vehicle.passengers = self.updated_bus_passengers(vehicle)

    def updated_bus_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        passengers_staying = self.passengers_staying(vehicle)
        new_passengers = self.getting_on_passengers(vehicle)

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
            if self.right_destination(vehicle, passenger):
                getting_on_passengers.append(passenger)
                self.passengers.remove(passenger)

        return getting_on_passengers

    @staticmethod
    def right_destination(vehicle: AbstractVehicle, passenger: AbstractPassenger) -> bool:
        if passenger.destination in vehicle.stops_left:
            return True
        return False

    def add_passengers(self, passengers: List[AbstractPassenger]) -> None:
        self.passengers.extend(passengers)

    def __init__(self, _id: str, load: LoadDistribution):
        super().__init__()
        self.id = _id
        self.load_distribution = load
        self.passengers = []
