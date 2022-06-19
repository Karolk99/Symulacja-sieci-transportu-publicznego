import time
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
    schedule: [float]
    topology: List[RouteStop]

    def set_schedule(self, schedule: [str]):
        self.schedule = [time.strptime(item, '%H:%M') for item in schedule]

    @classmethod
    def from_stops(cls, stops: List[ActorProxy], weights: List[float], schedule: [str] = None):
        top = [RouteStop(to_next=w, stop=s) for s, w in zip(stops, weights)]
        return cls(topology=top, schedule=schedule)


@dataclass
class Map:
    stops: Dict[str, ActorProxy]
    routs: List[Route]
    topology: DiGraph
