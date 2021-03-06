from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import pykka

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation_components.generator import LoadDistribution
    from simulation_components.passenger import AbstractPassenger


class AbstractStop(ABC, pykka.ThreadingActor):
    id: str
    passengers: List[AbstractPassenger]
    load_distribution: LoadDistribution

    def __init__(self):
        super().__init__()

    @abstractmethod
    def add_passengers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    @abstractmethod
    def handle_vehicle(self, passengers: [AbstractPassenger], possible_stops: [pykka.ActorProxy]):
        """
        Handle vehicle stopping on depot, exchange passengers etc.
        :param passengers:
        :param possible_stops:
        :return: None
        """
        pass
