import asyncio
from abc import ABC, abstractmethod
from time import sleep

from symulation_components.map import Route
from symulation_components.messages import VehicleMsg
from symulation_components.stop import BusStop
from symulation_components.vehicle import Bus, BusState, AbstractVehicle
from symulation_components.visualizer import PromptVisualizer


class Runner:
    @staticmethod
    async def start_vehicle(vehicle: AbstractVehicle, time: float):
        await asyncio.sleep(time)
        vehicle.state = BusState.Running

    @staticmethod
    async def run_simulation():
        stops = [
            BusStop.start('A').proxy(),
            BusStop.start('B').proxy(),
            BusStop.start('C').proxy(),
            BusStop.start('D').proxy(),
        ]
        weights = [
            12,
            15,
            13,
            20,
        ]

        route_a = Route.from_stops(stops, weights)

        vehicles = [
            Bus.start(1, route_a).proxy(),
            Bus.start(2, route_a).proxy()
        ]

        PromptVisualizer.start(vehicles, route_a)
        await asyncio.gather(Runner.start_vehicle(vehicles[0], 2),
                             Runner.start_vehicle(vehicles[1], 4))


if __name__ == '__main__':
    asyncio.run(Runner.run_simulation())
