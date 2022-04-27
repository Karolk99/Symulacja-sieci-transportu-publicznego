from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from stop import AbstractStop


@dataclass
class RouteStop:
    id: str
    to_next: float


@dataclass
class Route:
    topology: List[RouteStop]

    @classmethod
    def from_stops(cls, stops: List[AbstractStop], weights: List[float]):
        top = [RouteStop(to_next=w, id=s.id) for s, w in zip(stops, weights)]
        return cls(topology=top)


class AbstractMap(ABC):
    stops: List[AbstractStop]
    routs: List[Route]
