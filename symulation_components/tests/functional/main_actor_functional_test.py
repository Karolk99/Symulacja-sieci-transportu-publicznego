import time
import unittest

import pykka

from symulation_components.main_actor import MainActor
from symulation_components.vehicle import Bus, AbstractVehicle


class MainActorFunctTest(unittest.TestCase):
    def test_sanity(self):
        MainActor.start('../example_config2.yaml').proxy()
        time.sleep(5)
        buses = pykka.ActorRegistry.get_by_class(AbstractVehicle)
        for bus in buses:
            self.assertLess(0, bus.proxy().position.get())

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all()