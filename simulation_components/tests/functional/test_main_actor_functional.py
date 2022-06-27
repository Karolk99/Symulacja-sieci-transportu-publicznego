import os
import time
import unittest
from unittest.mock import patch

import pykka

from simulation_components.definitions import TEST_RES_DIR
from simulation_components.main_actor import MainActor
from simulation_components.util.time import Time
from simulation_components.vehicle import AbstractVehicle


class MainActorFunctTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_config2 = os.path.join(TEST_RES_DIR, 'example_config2.yaml')

    def test_sanity(self):
        MainActor.start(self.example_config2).proxy()
        time.sleep(5)
        buses = pykka.ActorRegistry.get_by_class(AbstractVehicle)
        for bus in buses:
            self.assertLess(0, bus.proxy().position.get())

    @patch.object(MainActor, 'tick')
    def test_adding_passengers(self, mocked_main_actor):
        main_actor = MainActor.start(self.example_config2).proxy()
        # with patch.object(MainActor, 'tick', wraps=main_actor.tick) as mock:
        time.sleep(2)
        print(f'{mocked_main_actor.call_count=}')

    def test_stability(self):
        MainActor.start(self.example_config2).proxy()
        time.sleep(20)

    def tearDown(self) -> None:
        ref = pykka.ActorRegistry.get_by_class(MainActor)[0]
        ref.stop(True, timeout=10)
        time.sleep(1)
        pykka.ActorRegistry.stop_all(timeout=5)
        Time(...)\
            .__class__\
            .force_remove_instance()

    @classmethod
    def tearDownClass(cls) -> None:
        # pykka.ActorRegistry.stop_all()
        ...
