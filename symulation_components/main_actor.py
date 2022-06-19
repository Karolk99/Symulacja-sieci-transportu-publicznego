import logging
import threading
from threading import Thread
import pykka
from pykka import ActorRef, ActorProxy

from symulation_components.generator import PassengerGenerator
from symulation_components.map import Map
from symulation_components.util.scheduler import Schedulable, Scheduler
from symulation_components.util.serializer import Serializer
from symulation_components.vehicle import Bus


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Time(metaclass=Singleton):
    _value: float
    _base: int
    _res: float

    def __init__(self, base: int):
        self._value = 0.0
        self._base = base
        self._res = 24 * 60 * 60 / base

    def tick(self):
        self._value += 1
        self._value %= self._base

    def time_sec(self):
        return self._value * self._res

    def __float__(self):
        return self._value

    def __str__(self):
        _time = self.time_sec()
        return f'{int(_time / (60 * 60) % 24):0>2}:{int(_time / 60) % 60:0>2}.{int(_time % 60)}'

    @staticmethod
    def str2sec(time_str: str):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, [int(i) for i in time_str.split(":")])])


class MainActor(pykka.ThreadingActor, Schedulable):
    """
    Generate buses and update depots
    """
    time: Time
    _stops: [ActorRef]
    _time_table: dict
    _scheduler: Scheduler
    _thread_loop: Thread
    _stop_event: threading.Event
    _passenger_gen: ActorProxy
    _map: Map

    def __init__(self, config_path: str):
        super().__init__()
        self.logger = logging.getLogger('simulation_components.main_actor.MainActor')
        try:
            serializer = Serializer(config_path)
            self._stops = serializer.get_stops()

            routes = serializer.get_routes()
            self._time_table = {}
            for route in routes:
                for time in route.schedule:
                    self._time_table.setdefault(Time.str2sec(time), []).append(route)
            base = serializer.get_time_base()
            self.time = Time(base)

            # {stop.id.get(): stop for stop in self._stops}
            self._map = Map({}, routes, serializer.get_graph())
            self._passenger_gen = PassengerGenerator.start(self._map).proxy()
        except (ValueError, KeyError) as e:
            self.logger.error(e)
            exit(1)
        self._scheduler = Scheduler(schedulable=self, logger=self.logger)
        self._stop_event = threading.Event()
        self._last_id = 0
        self.logger.info('creating an instance of MainActor')

    def on_stop(self):
        self._scheduler.stop()
        self.logger.info(f'stopping an instance of MainActor {self._stop_event.is_set()}')

    def on_start(self) -> None:
        self._scheduler.start()
        self.logger.info('starting an instance of MainActor')

    def tick(self) -> None:
        # change time
        prv_time = self.time.time_sec()
        self.time.tick()

        # update bus stops
        for stop in self._stops:
            self._passenger_gen.generate_for_one_stop(self._stops[stop], self.time.time_sec())

        # update buses
        for record in self._time_table:
            if prv_time <= record <= self.time.time_sec():
                # spawn appropriate buses
                for route in self._time_table[record]:
                    self._last_id += 1
                    bus = Bus.start(self._last_id, route, 50).proxy()
                    self.logger.debug(f'Spawned new bus: {bus}')

        self.logger.info(f'doing stuff... current time {self.time}')
