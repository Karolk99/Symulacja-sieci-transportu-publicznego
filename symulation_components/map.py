from abc import ABC
from dataclasses import dataclass
from typing import Dict, List
from networkx import DiGraph
from pykka import ActorProxy


@dataclass
class RouteStop:
    stop: ActorProxy
    to_next: float


@dataclass
class Route:
    topology: List[RouteStop]

    @classmethod
    def from_stops(cls, stops: List[ActorProxy], weights: List[float]):
        top = [RouteStop(to_next=w, stop=s) for s, w in zip(stops, weights)]
        return cls(topology=top)


@dataclass
class Map:
    stops: Dict[str, ActorProxy]
    routs: List[Route]
    topology: DiGraph
