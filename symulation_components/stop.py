from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from passenger import AbstractPassenger


@dataclass
class LoadDistribution:
    pass  # TODO


class AbstractStop(ABC):
    id: str
    passengers: List[AbstractPassenger]
    load_distribution: LoadDistribution

    @abstractmethod
    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    @abstractmethod
    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass


class BusStop(AbstractStop):
    def add_passangers(self, passengers: List[AbstractPassenger]) -> bool:
        pass

    def getting_on_passangers(self, limit: int = 10) -> List[AbstractPassenger]:
        pass

    def __init__(self, _id: str):
        self.id = _id