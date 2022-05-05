from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

import pykka

from symulation_components.depot import StopState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from symulation_components.generator import LoadDistribution
    from symulation_components.passenger import AbstractPassenger
    from symulation_components.vehicle import AbstractVehicle


class AbstractStop(ABC, pykka.ThreadingActor):
    id: str
    passengers: List[AbstractPassenger]
    load_distribution: LoadDistribution

    _state: StopState

    def __init__(self):
        super().__init__()
        self._state = StopState.EMPTY

    @abstractmethod
    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    @abstractmethod
    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass

    @abstractmethod
    def handle_vehicle(self, vehicle: AbstractVehicle):
        """
        Handle vehicle stopping on depot, exchange passengers etc.
        :param vehicle: vehicle that stops in
        :return: None
        """
        pass
