from abc import ABC
from dataclasses import dataclass
from typing import Dict, List
from networkx import DiGraph
from pykka import ActorProxy


@dataclass
class RouteStop:
    stop_urn: str
    to_next: float


@dataclass
class Route:
    topology: List[RouteStop]

    @classmethod
    def from_stops(cls, stops: List[ActorProxy], weights: List[float]):
        top = [RouteStop(to_next=w, stop_urn=s.actor_urn.get()) for s, w in zip(stops, weights)]
        return cls(topology=top)


class AbstractMap(ABC):
    stops: Dict[str, ActorProxy]
    routs: List[Route]
    topology: DiGraph


@dataclass
class Map:
    stops: Dict[str, ActorProxy]
    routs: List[Route]
    topology: DiGraph
