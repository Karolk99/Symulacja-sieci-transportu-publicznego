import os
import time
import unittest
from unittest import mock

import pykka

from simulation_components.definitions import TEST_RES_DIR
from simulation_components.main_actor import MainActor
from simulation_components.util.time import Time


@unittest.skip
class BusE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_config2 = os.path.join(TEST_RES_DIR, 'example_config2.yaml')

    def setUp(self) -> None:
        print('starting test')
        MainActor.start(self.example_config2)

    @unittest.skip
    @mock.patch('simulation_components.depot.BusStop')
    def test_passengers_handling(self, mocked_bus_stop: mock.MagicMock):
        ...

    def tearDown(self) -> None:
        MainActor.get_instance_proxy().stop()
        Time.force_remove_instance()
        time.sleep(2)
        print('ending test')

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all()
        time.sleep(2)
