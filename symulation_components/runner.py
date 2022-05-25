import asyncio

from symulation_components.map import Route
from symulation_components.depot import BusStop
from symulation_components.vehicle import Bus, VehicleState, AbstractVehicle
from symulation_components.visualizer import PromptVisualizer


class Runner:
    @staticmethod
    async def start_vehicle(vehicle: AbstractVehicle, time: float):
        await asyncio.sleep(time)
        vehicle.state = VehicleState.Running

    @staticmethod
    async def run_simulation():
        # @TODO consider adding some configuration loading component

        # create route with bus stops and weights (distances to next bus stop)
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

        # create buses
        vehicles = [
            Bus.start(1, route_a).proxy(),
            Bus.start(2, route_a).proxy()
        ]

        # start console visualizer
        PromptVisualizer.start(vehicles, route_a)

        # start vehicles
        await asyncio.gather(Runner.start_vehicle(vehicles[0], 2),
                             Runner.start_vehicle(vehicles[1], 4))


if __name__ == '__main__':
    asyncio.run(Runner.run_simulation())
