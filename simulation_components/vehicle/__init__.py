from .states import VehicleState
from .abstract_vehicle import AbstractVehicle
from .bus import Bus
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
