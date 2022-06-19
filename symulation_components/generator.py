from abc import ABC, abstractmethod

import pykka
import random
import networkx as nx
from typing import List

from pykka import ActorProxy

from symulation_components.map import Map
from symulation_components.passenger import Passenger


class LoadDistribution:
    load: List[int]

    def __init__(self, load: List[int]) -> None:
        self.load = load

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.load == other.load

    def get_number_of_passengers(self, time: float):
        index = int(time) % len(self.load)
        return self.load[index]


class AbstractPassengerGenerator(ABC, pykka.ThreadingActor):
    map: Map

    @abstractmethod
    def generate(self, time: float) -> None:
        pass


class PassengerGenerator(AbstractPassengerGenerator):

    def __init__(self, map: Map):
        super().__init__()
        self.map = map

    def generate(self, time: float) -> None:
        for _, stop in self.map.stops.items():
            self.generate_for_one_stop(stop, time)

    def generate_for_one_stop(self, stop: ActorProxy, time: float) -> None:
        possible_destinations = list(nx.descendants(self.map.topology, stop.id.get()))
        if not possible_destinations:
            return
        number_of_passengers = stop.load_distribution.get().get_number_of_passengers(time)

        passengers = []
        for _ in range(number_of_passengers):
            destination = self._choose_stop(possible_destinations)
            passengers.append(Passenger(destination, stop.id.get()))

        stop.add_passengers(passengers)

    @staticmethod
    def _choose_stop(stops: List[str]) -> str:
        return random.choice(stops)
