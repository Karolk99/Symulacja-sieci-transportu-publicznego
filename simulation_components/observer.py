import abc
import dataclasses
import logging
import csv
import io
import os.path

import pykka

from simulation_components.counter import CounterActor
from simulation_components.definitions import LOGGING_GLOB_PATH, LOGGING_CTX_PATH
from simulation_components.util.time import Time
from simulation_components.util.singleton import Singleton


class GlobalCsvFormatter(logging.Formatter):
    def __init__(self, path: str):
        super().__init__()
        self.output = io.StringIO()
        headers = ['timestamp', 'origin', 'buses', 'passengers', 'waiting_psg', 'commuting_psg']
        self.writer = csv.DictWriter(self.output, delimiter=',', lineterminator='\n', fieldnames=headers)

        if not os.path.isfile(path):
            self.writer.writeheader()  # file doesn't exist yet, write a header

    def format(self, record):
        # "timestamp", "origin", "buses", "passengers", "waiting_psg", "commuting_psg"
        self.writer.writerow({'timestamp': record.timestamp,
                              'origin': record.origin,
                              'buses': record.buses,
                              'passengers': record.passengers,
                              'waiting_psg': record.waiting_psg,
                              'commuting_psg': record.commuting_psg
                              })
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


class ContextCsvFormatter(logging.Formatter):
    def __init__(self, path: str):
        super().__init__()
        self.output = io.StringIO()
        headers = ['timestamp', 'type', 'id', 'value']
        self.writer = csv.DictWriter(self.output, delimiter=',', lineterminator='\n', fieldnames=headers)

        if not os.path.isfile(path):
            self.writer.writeheader()  # file doesn't exist yet, write a header

    def format(self, record):
        # timestamp type id value
        self.writer.writerow({'timestamp': record.timestamp,
                              'type': record.type,
                              'id': record.id,
                              'value': record.value
                              })
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
        global_formatter = GlobalCsvFormatter(LOGGING_GLOB_PATH)
        context_formatter = ContextCsvFormatter(LOGGING_CTX_PATH)

        self.global_logger = logging.getLogger('observer.global')
        handler = logging.FileHandler(LOGGING_GLOB_PATH)
        handler.setFormatter(global_formatter)
        self.global_logger.addHandler(handler)
        self.global_logger.setLevel(logging.INFO)

        self.context_logger = logging.getLogger('observer.context')
        handler = logging.FileHandler(LOGGING_CTX_PATH)
        handler.setFormatter(context_formatter)
        self.context_logger.addHandler(handler)
        self.context_logger.setLevel(logging.INFO)

        self._prv_time = None

        self._counter_actor = CounterActor.get_counter_actor()
        self.global_logger.debug(f'Spawned CounterActor {self._counter_actor}')

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

            # log context based
            self = args[0]
            match self.__class__.__name__:
                case ('Bus' | 'AbstractVehicle'):
                    obs.context_logger.info(f'{func.__name__}', extra={
                        'timestamp': Observer._get_timestamp(),
                        'type': 'Bus',
                        'id': self.id,
                        'value': len(self.passengers)
                    })
                case ('BusStop' | 'AbstractStop'):
                    obs.context_logger.info(f'{func.__name__}', extra={
                        'timestamp': Observer._get_timestamp(),
                        'type': 'BusStop',
                        'id': self.id,
                        'value': len(self.passengers)
                    })

            # log once global state
            if obs._prv_time != obs._get_timestamp():
                obs._prv_time = obs._get_timestamp()

                obs.global_logger.info(f'{func.__name__}', extra={'timestamp': Observer._get_timestamp(),
                                                                  'origin': func.__name__,
                                                                  'buses': buses_num,
                                                                  'passengers': commuting_passengers + waiting_passengers,
                                                                  'waiting_psg': waiting_passengers,
                                                                  'commuting_psg': commuting_passengers})

            return result

        return func_wrapper

    @classmethod
    def is_instance(cls):
        return cls in cls._instances
