import asyncio
import logging

from pykka import ActorProxy

from simulation_components.generator import LoadDistribution
from simulation_components.map import Route
from simulation_components.depot import BusStop
from simulation_components.vehicle import Bus, VehicleState, AbstractVehicle
from simulation_components.visualizer import PromptVisualizer


class Runner:
    @staticmethod
    async def start_vehicle(vehicle: ActorProxy, time: float):
        await asyncio.sleep(time)
        vehicle.state = VehicleState.Running

    @staticmethod
    async def run_simulation():
        # @TODO consider adding some configuration loading component

        logging.root.setLevel(logging.WARNING)

        distribution = [number for number in range(24)]
        load = LoadDistribution(distribution)

        # create route with bus stops and weights (distances to next bus stop)
        stops = [
            BusStop.start('A', load).proxy(),
            BusStop.start('B', load).proxy(),
            BusStop.start('C', load).proxy(),
            BusStop.start('D', load).proxy(),
        ]
        weights = [
            12,
            15,
            13,
            20,
        ]
        route_a = Route.from_stops(stops, weights)

        # create buses
        vehicles = [
            Bus.start(1, route_a, 100).proxy(),
            Bus.start(2, route_a, 100).proxy()
        ]

        # start console visualizer
        PromptVisualizer.start(vehicles, route_a)

        # start vehicles
        await asyncio.gather(Runner.start_vehicle(vehicles[0], 2),
                             Runner.start_vehicle(vehicles[1], 4))


if __name__ == '__main__':
    asyncio.run(Runner.run_simulation())
