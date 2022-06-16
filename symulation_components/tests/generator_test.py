from symulation_components.generator import PassengerGenerator, LoadDistribution
from symulation_components.map import Map, Route
from symulation_components.depot import BusStop

import asyncio
import networkx as nx
import time


class Test:
    @staticmethod
    async def run_test():
        distribution = [number for number in range(24)]
        load = LoadDistribution(distribution)
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

        gen_proxy = PassengerGenerator.start(map).proxy()

        # Test load distribution
        number = load.get_number_of_passengers(12.6)
        assert number == 12, f"Wrong number for laod distribution: {number}"

        # Test if correct number of passengers was generated
        gen_proxy.generate(12.3)
        time.sleep(1)
        for number, stop_proxy in enumerate(stops):
            pass_number = len(stop_proxy.passengers.get())
            if number == 3:  # Last stop should not generate any passengers
                assert pass_number == 0,\
                    f"Wrong number of passengers generated: Stop number: {number}, Value: {pass_number}"
                continue
            assert pass_number == 12, \
                f"Wrong number of passengers generated: Stop number: {number}, Value: {pass_number}"

        gen_proxy.stop()


if __name__ == '__main__':
    asyncio.run(Test.run_test())
