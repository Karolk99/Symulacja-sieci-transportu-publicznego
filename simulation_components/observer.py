import abc
import dataclasses
import logging
import csv
import io

import pykka

from simulation_components.counter import CounterActor
from simulation_components.definitions import LOGGING_PATH
from simulation_components.util.time import Time
from simulation_components.util.singleton import Singleton


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        # "timestamp", "origin", "buses", "passengers", "waiting_psg", "commuting_psg"
        self.writer.writerow([record.sim_time,
                              record.msg,
                              record.buses_num,
                              record.psg_num,
                              record.waiting_psg,
                              record.com_psg
                              ])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


@dataclasses.dataclass
class Frame:
    name: str
    passengers: int


class Observable(abc.ABC):
    @abc.abstractmethod
    def info_(self):
        pass


class Observer(metaclass=Singleton):

    def __init__(self):
        self.logger = logging.getLogger('observer')
        handler = logging.FileHandler(LOGGING_PATH)
        handler.setFormatter(CsvFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self._counter_actor = CounterActor.get_counter_actor()
        self.logger.debug(f'Spawned CounterActor {self._counter_actor}')

    @staticmethod
    def _get_timestamp():
        return str(Time(...)) if Time.is_instance() else '__:__'

    @classmethod
    def observe(cls, func):
        obs = cls()

        def func_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            buses_num = len(pykka.ActorRegistry.get_by_class_name('Bus'))
            commuting_passengers = obs._counter_actor.commuting_passengers().get()
            waiting_passengers = obs._counter_actor.waiting_passengers().get()

            obs.logger.info(f'{func.__name__}', extra={'sim_time': Observer._get_timestamp(),
                                                       'buses_num': buses_num,
                                                       'psg_num': commuting_passengers + waiting_passengers,
                                                       'waiting_psg': waiting_passengers,
                                                       'com_psg': commuting_passengers})
            return result

        return func_wrapper

    @classmethod
    def is_instance(cls):
        return cls in cls._instances
