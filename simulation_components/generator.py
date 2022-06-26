import logging
from abc import ABC, abstractmethod

import pykka
import random
import networkx as nx
from typing import List, Any

from pykka import ActorProxy

from simulation_components.map import Map
from simulation_components.observer import Observer
from simulation_components.passenger import Passenger


class LoadDistribution:
    _SECONDS_IN_HOUR = 3600
    load: List[int]

    def __init__(self, load: List[int]) -> None:
        self.load = load

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.load == other.load

    def get_number_of_passengers(self, time: float):
        curr_hour = time / self._SECONDS_IN_HOUR
        index = int(curr_hour * (len(self.load) / 24)) % len(self.load)
        return self.load[index]


class AbstractPassengerGenerator(ABC, pykka.ThreadingActor):
    map: Map

    @abstractmethod
    def generate(self, time: float) -> None:
        pass


class PassengerGenerator(AbstractPassengerGenerator):

    def __init__(self, _map: Map):
        super().__init__()
        self.logger = logging.getLogger(f'simulation_components.generator.PassengerGenerator')
        self.map = _map

    @Observer.observe
    def generate(self, time: float) -> None:
        self.logger.debug('generate')
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
            # passenger path without source
            path = nx.shortest_path(self.map.topology, source=stop.id.get(), target=destination)[:1]
            passengers.append(Passenger(destination, stop.id.get(), path))

        stop.add_passengers(passengers)

    @staticmethod
    def _choose_stop(stops: List[str]) -> str:
        return random.choice(stops)

    def on_stop(self) -> None:
        self.logger.debug('Stopping PassengerGenerator actor')
