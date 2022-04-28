from abc import ABC, abstractmethod
from typing import List
from vehicle import AbstractVehicle
from map import AbstractMap, Route


class Visualizer(ABC):
    @staticmethod
    @abstractmethod
    def print(_vehicles: List[AbstractVehicle],
              _map: AbstractMap):
        ...


class PromptVisualizer(Visualizer):
    @staticmethod
    def print(_vehicles: List[AbstractVehicle], _route: Route):
        for v in _vehicles[:-1]:
            print(' ' * v.position, v.id)
        print(' ' * _vehicles[-1].position, _vehicles[-1].id)
        for route_stop in _route.topology:
            print(f'{route_stop.id}', end='')
            print('-' * int(route_stop.to_next), end='')
        print('\n\n\n')