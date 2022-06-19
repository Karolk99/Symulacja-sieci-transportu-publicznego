import logging
import time
import unittest

import pykka

from symulation_components.depot import BusStop
from symulation_components.generator import LoadDistribution
from symulation_components.map import Route
from symulation_components.vehicle import Bus


class BusFunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = logging.getLogger('tests.functional.BusFunctionalTest')

    @staticmethod
    def basic_load():
        distribution = [number for number in range(24)]
        return LoadDistribution(distribution)

    def test_bus_sanity(self) -> None:
        """
        Check that bus goes along the route
        """
        load = BusFunctionalTest.basic_load()

        stops = [
            BusStop.start('A', load).proxy(),
            BusStop.start('B', load).proxy(),
        ]

        weights = [
            20,
            10
        ]
        route_a = Route.from_stops(stops, weights)

        bus = Bus.start(1, route_a, 50).proxy()
        time.sleep(4)
        self.assertLess(4, bus.position.get())
        self.logger.info(f'bus final position={bus.position.get()}')
        bus.stop()

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all()
