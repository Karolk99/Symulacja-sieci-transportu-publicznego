from abc import ABC, abstractmethod
from time import sleep

from symulation_components.map import Route
from symulation_components.stop import BusStop
from symulation_components.vehicle import Bus
from symulation_components.visualizer import PromptVisualizer


class Runner:
    @staticmethod
    def run_simulation():
        stops = [
            BusStop('A'),
            BusStop('B'),
            BusStop('C'),
            BusStop('D'),
        ]
        weights = [
            12,
            15,
            13,
            20,
        ]

        route_a = Route.from_stops(stops, weights)

        vehicles = [
            Bus(1, route_a),
            # Bus(2, route_a)
        ]

        tick = 1
        while True:
            [v.drive(tick) for v in vehicles]
            sleep(0.1)
            PromptVisualizer.print(vehicles, route_a)


if __name__ == '__main__':
    Runner.run_simulation()
