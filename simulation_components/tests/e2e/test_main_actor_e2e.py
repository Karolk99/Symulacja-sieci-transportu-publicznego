import os
import time
import pykka
import logging
import unittest
from unittest import mock
from unittest.mock import patch

from simulation_components.definitions import TEST_RES_DIR
from simulation_components.main_actor import MainActor
from simulation_components.util.time import Time
from simulation_components.tests.util.ActorMock import ActorMock

logger = logging.getLogger('e2e.test')
logger.level = logging.DEBUG


class MainActorE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pykka.ActorRegistry.stop_all()
        cls.config_dir = os.path.join(TEST_RES_DIR, 'bus.config.yaml')

    @staticmethod
    def start(*args, **kwargs):
        obj = ActorMock()
        pykka.ActorRegistry.register(obj.actor_ref)
        logger.debug(f"Starting {obj}")
        obj._start_actor_loop()
        return obj.actor_ref

    @patch('simulation_components.vehicle.Bus.start', autospec=True)
    @patch('simulation_components.depot.BusStop.start', autospec=True)
    def test_adding_psg(self, mocked_bus_stop: mock.MagicMock, mocked_bus: mock.MagicMock):
        mocked_bus.side_effect = MainActorE2E.start
        mocked_bus_stop.side_effect = MainActorE2E.start

        MainActor.start(self.config_dir).proxy()
        duration = 4
        time.sleep(duration)

        self.assertEqual(mocked_bus.call_count, duration * 2)
        self.assertTrue(mocked_bus_stop.call_count, duration * 3)

    def tearDown(self) -> None:
        Time(...)\
            .__class__\
            .force_remove_instance()
        pykka.ActorRegistry.stop_all()
