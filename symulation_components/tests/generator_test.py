from symulation_components.generator import PassengerGenerator
from symulation_components.map import Map, Route
from symulation_components.depot import BusStop

import asyncio
import networkx as nx


class Test:
    @staticmethod
    async def run_test():
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

        paths = [
            ('A', 'B'),
            ('B', 'C'),
            ('C', 'D'),
        ]

        route_a = Route.from_stops(stops, weights)
        graph = nx.DiGraph()
        graph.add_edges_from(paths)
        map_stops = {stop.id.get(): stop for stop in stops}
        map = Map(map_stops, [route_a], graph)

        PassengerGenerator.start(map).proxy()


if __name__ == '__main__':
    asyncio.run(Test.run_test())
