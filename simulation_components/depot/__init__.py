import logging
from .states import StopState
from .abstract_stop import AbstractStop
from .bus_stop import BusStop

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
