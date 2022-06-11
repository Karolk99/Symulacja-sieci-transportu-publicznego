from abc import ABC, abstractmethod

import time
import pykka
import random
import networkx as nx
from threading import Thread
from typing import List

from pykka import ActorProxy

from symulation_components.map import Map
from symulation_components.passenger import Passenger


class LoadDistribution:
    def __init__(self):
        pass

    @staticmethod
    def get_dist(vehicle, route):
        return 2 if vehicle.id == 1 else 3

    def get_number_of_passengers(self, iteration):
        return 2


class AbstractPassengerGenerator(ABC, pykka.ThreadingActor):
    map: Map
    hour: int
    frequency: int  # hours per one iteration

    _thread_loop: Thread

    @abstractmethod
    def on_start(self) -> None:
        pass

    @abstractmethod
    def on_stop(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def generate(self) -> None:
        pass


class PassengerGenerator(AbstractPassengerGenerator):

    def __init__(self, map: Map, frequency=1):
        super(PassengerGenerator, self).__init__()
        self.map = map
        self.frequency = frequency
        self.hour = 0

    def on_start(self) -> None:
        self._thread_loop = Thread(target=self.run)
        self._thread_loop.start()

    def on_stop(self) -> None:
        self._thread_loop.join()

    def run(self) -> None:
        while True:
            time.sleep(1)  # TODO: add parameter
            self.generate()
            self.hour = self.hour + self.frequency % 24

    def generate(self) -> None:
        for _, stop in self.map.stops.items():
            self.generate_for_one_stop(stop)

    def generate_for_one_stop(self, stop: ActorProxy) -> None:
        possible_destinations = list(nx.descendants(self.map.topology, stop.id.get()))
        if not possible_destinations:
            return
        number_of_passengers = stop.load_distribution.get().get_number_of_passengers(self.hour)

        passengers = []
        for _ in range(number_of_passengers):
            destination = self._choose_stop(possible_destinations)
            passengers.append(Passenger(destination, stop.id.get()))

        stop.add_passengers(passengers)

    @staticmethod
    def _choose_stop(stops: List[str]) -> str:
        return random.choice(stops)
