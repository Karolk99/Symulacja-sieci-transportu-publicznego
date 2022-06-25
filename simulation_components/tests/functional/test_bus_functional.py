import logging
import time
import unittest

import pykka

from simulation_components.depot import BusStop
from simulation_components.generator import LoadDistribution
from simulation_components.main_actor import Time
from simulation_components.map import Route
from simulation_components.vehicle import Bus


class BusFunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = logging.getLogger('tests.functional.BusFunctionalTest')

    def setUp(self) -> None:
        Time(24)

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

    def test_passengers_handling(self) -> None:
        ...

    def tearDown(self) -> None:
        Time(...)\
            .__class__\
            .force_remove_instance()
        pykka.ActorRegistry.stop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all()
