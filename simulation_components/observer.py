import abc
import dataclasses
import logging
import csv
import io

import pykka

from simulation_components.util.time import Time
from simulation_components.util.singleton import Singleton


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow([record.sim_time, record.msg, record.buses_num])
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
        handler = logging.StreamHandler()
        handler.setFormatter(CsvFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def _get_timestamp():
        return str(Time(...)) if Time.is_instance() else '__:__'

    @classmethod
    def observe(cls, func):
        obs = cls()

        def func_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            buses_num = len(pykka.ActorRegistry.get_by_class_name('Bus'))

            obs.logger.info(f'{func.__name__}', extra={'sim_time': Observer._get_timestamp(),
                                                       'buses_num': buses_num})
            return result

        return func_wrapper
