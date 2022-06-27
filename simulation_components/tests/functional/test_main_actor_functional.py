import os
import time
import unittest
from unittest.mock import patch

import pykka

from simulation_components.definitions import TEST_RES_DIR, LOGGING_PATH_TEST
from simulation_components.main_actor import MainActor
from simulation_components.util.time import Time
from simulation_components.vehicle import AbstractVehicle


class MainActorFunctTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_config2 = os.path.join(TEST_RES_DIR, 'example_config2.yaml')

    def setUp(self) -> None:
        print('starting test')

    def test_sanity(self):
        MainActor.start(self.example_config2).proxy()
        time.sleep(5)
        buses = pykka.ActorRegistry.get_by_class(AbstractVehicle)
        for bus in buses:
            self.assertLess(0, bus.proxy().position().get())

    @patch.object(MainActor, 'tick')
    def test_tick(self, mocked_main_actor):
        duration = 2
        MainActor.start(self.example_config2).proxy()
        time.sleep(duration)
        call_count = mocked_main_actor.call_count
        print(f'{call_count}')
        self.assertTrue(call_count in [duration, duration + 1, duration - 1])

    def test_stability(self):
        MainActor.start(self.example_config2).proxy()
        time.sleep(20)

    def tearDown(self) -> None:
        MainActor.get_instance_proxy().stop()
        time.sleep(1)
        Time.force_remove_instance()
        time.sleep(2)
        print('ending test')

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all(timeout=5)
        time.sleep(2)
