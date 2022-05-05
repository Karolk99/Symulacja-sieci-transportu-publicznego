import time
from typing import List

from symulation_components.depot import AbstractStop, StopState
from symulation_components.generator import LoadDistribution
from symulation_components.passenger import AbstractPassenger


class BusStop(AbstractStop):
    def handle_vehicle(self, vehicle):
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
        time.sleep(LoadDistribution.get_dist(vehicle, vehicle.route))
        # TODO passengers exchange
        self._state = StopState.EMPTY
        # handling finished

    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass

    def __init__(self, _id: str):
        super().__init__()
        self.id = _id