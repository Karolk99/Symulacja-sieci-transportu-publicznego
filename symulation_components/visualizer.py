import sys
from abc import ABC, abstractmethod
from threading import Thread
from typing import List
import time
import pykka
from pykka import ActorRegistry
from symulation_components.vehicle import AbstractVehicle
from map import Route


class Visualizer(ABC, pykka.ThreadingActor):
    _thread_loop: Thread

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self):
        pass


class PromptVisualizer(Visualizer):
    """
    Visualizer generating basic output inside a console
    """
    def __init__(self, _vehicles: List[AbstractVehicle], _route: Route):
        super().__init__()
        self._vehicles = _vehicles
        self._route = _route

    def on_start(self) -> None:
        self._thread_loop = Thread(target=self.run)
        self._thread_loop.start()

    def on_stop(self) -> None:
        self._thread_loop.join()

    def run(self):
        while True:
            for v in self._vehicles[:-1]:
                print(' ' * int(v.position.get()), v.id.get())
            print(' ' * int(self._vehicles[-1].position.get()), self._vehicles[-1].id.get())
            for route_stop in self._route.topology:
                print(f'{ActorRegistry.get_by_urn(route_stop.stop_urn).proxy().id.get()}', end='')
                print('-' * int(route_stop.to_next), end='')
            print('\n\n\n')
            sys.stdout.flush()
            time.sleep(1)
