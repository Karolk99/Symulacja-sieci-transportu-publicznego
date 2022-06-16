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
        # check if busy (another vehicle already here) and wait
        while self._state == StopState.BUSY:
            time.sleep(0.01)

        # start handling vehicle
        self._state = StopState.BUSY
        vehicle.add_passengers(self.getting_on_passengers(vehicle))
        vehicle.remove_passengers(self.getting_out_passengers(vehicle))

        self._state = StopState.EMPTY
        # handling finished

    def add_passengers(self, passengers: List[AbstractPassenger]) -> None:
        self.passengers.extend(passengers)

    def getting_out_passengers(self, vehicle: AbstractVehicle) -> List[int]:
        passengers_indexes = []
        for index, passenger in enumerate(vehicle.passengers):
            if passenger.destination == self.id:
                passengers_indexes.append(index)

        return passengers_indexes

    def getting_on_passengers(self, vehicle: AbstractVehicle) -> List[AbstractPassenger]:
        passenger_indexes = []
        for index, passenger in enumerate(self.passengers):
            if self.right_destination(vehicle, passenger):
                passenger_indexes.append(index)

        getting_on_passengers = []
        for index in passenger_indexes:
            if vehicle.seats_left == len(getting_on_passengers):
                break
            getting_on_passengers.append(self.passengers.pop(index))

        return getting_on_passengers

    @staticmethod
    def right_destination(vehicle: AbstractVehicle, passenger: AbstractPassenger) -> bool:
        if passenger.destination in vehicle.stops_left:
            return True
        return False

    def __init__(self, _id: str):
        super().__init__()
        self.id = _id
        self.load_distribution = LoadDistribution()