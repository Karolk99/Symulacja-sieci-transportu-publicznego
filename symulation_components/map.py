from abc import ABC
from dataclasses import dataclass
from typing import List

from symulation_components.depot import AbstractStop


@dataclass
class RouteStop:
    stop_urn: str
    to_next: float


@dataclass
class Route:
    topology: List[RouteStop]

    @classmethod
    def from_stops(cls, stops: List[AbstractStop], weights: List[float]):
        top = [RouteStop(to_next=w, stop_urn=s.actor_urn.get()) for s, w in zip(stops, weights)]
        return cls(topology=top)


class AbstractMap(ABC):
    stops: List[AbstractStop]
    routs: List[Route]
