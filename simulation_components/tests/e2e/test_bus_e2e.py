import os
import unittest
from unittest import mock

import pykka

from simulation_components.definitions import TEST_RES_DIR
from simulation_components.main_actor import MainActor, Time


class BusE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_config2 = os.path.join(TEST_RES_DIR, 'example_config2.yaml')

    def setUp(self) -> None:
        MainActor.start(self.example_config2).proxy()

    @mock.patch('simulation_components.depot.BusStop')
    def test_passengers_handling(self, mocked_bus_stop: mock.MagicMock):
        ...

    def tearDown(self) -> None:
        Time(...)\
            .__class__\
            .force_remove_instance()
        pykka.ActorRegistry.stop_all()
