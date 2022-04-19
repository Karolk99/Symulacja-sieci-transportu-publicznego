from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from passenger import AbstractPassenger


@dataclass
class RouteToNextStop:
    length: int
    next_stop_id: str
    current_position: int


class AbstractVechicle(ABC):
    id: int
    capacity: int
    route: RouteToNextStop
    passengers: List[AbstractPassenger]

    @abstractmethod
    def drive(self, distance: int) -> bool:
        pass

    @abstractmethod
    def open_doors(self) -> bool:
        pass
