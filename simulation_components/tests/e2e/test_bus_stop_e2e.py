import os
import time
import unittest
from unittest import mock
from unittest.mock import patch

import pykka
from pykka import ActorProxy

from simulation_components.definitions import TEST_RES_DIR
from simulation_components.depot import AbstractStop
from simulation_components.generator import PassengerGenerator
from simulation_components.main_actor import MainActor, Time
from simulation_components.passenger import Passenger


class BuStopE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_config2 = os.path.join(TEST_RES_DIR, 'example_config2.yaml')
        cls.one_line_config = os.path.join(TEST_RES_DIR, 'one_line.config.yaml')

    @patch('simulation_components.generator.PassengerGenerator.generate_for_one_stop')
    def test_adding_psg(self, mocked_gen: mock.MagicMock):
        mocked_gen.side_effect = BuStopE2ETest.return_passenger
        MainActor.start(self.one_line_config).proxy()
        time.sleep(2)
        print(f'{mocked_gen.call_count=}')

        self.assertTrue(len((bus_stops := pykka.ActorRegistry.get_by_class(AbstractStop))))
        passengers_list = [stop.proxy().passengers.get() for stop in bus_stops]

        self.assertEqual(len(passengers_list[0]), mocked_gen.call_count // 2)
        self.assertTrue(all(len(passenger) == len(passengers_list[0]) for passenger in passengers_list))
        print(bus_stops[0].proxy().passengers.get())

    @staticmethod
    def return_passenger(*args, **kwargs):
        stop: ActorProxy = args[0]
        stop.add_passengers([Passenger('A', stop.id.get(), ['A', 'B', 'C'])])

    def tearDown(self) -> None:
        Time(...)\
            .__class__\
            .force_remove_instance()
        pykka.ActorRegistry.stop_all()
