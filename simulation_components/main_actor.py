import logging
import threading
from threading import Thread
import pykka
from pykka import ActorRef, ActorProxy

from simulation_components.counter import CounterActor
from simulation_components.depot import AbstractStop
from simulation_components.observer import Observer
from simulation_components.generator import PassengerGenerator
from simulation_components.map import Map
from simulation_components.util.scheduler import Schedulable, Scheduler
from simulation_components.util.serializer import Serializer
from simulation_components.util.time import Time
from simulation_components.vehicle import Bus, AbstractVehicle


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

    _refresh_rate: float

    def __init__(self, config_path: str):
        super().__init__()
        self.logger = logging.getLogger('simulation_components.main_actor.MainActor')
        Observer()
        try:
            serializer = Serializer(config_path)
            self._stops = serializer.get_stops()

            routes = serializer.get_routes()
            self._time_table = {}
            for route in routes:
                for time in route.schedule:
                    self._time_table.setdefault(Time.str2sec(time), []).append(route)
            base = serializer.get_time_base()
            if Time.is_instance():
                Time.force_remove_instance()
            self.time = Time(base)

            self._map = Map(self._stops, routes, serializer.get_graph())
            self._passenger_gen = PassengerGenerator.start(self._map).proxy()

            self._refresh_rate = serializer.get_ref_rate()
        except (ValueError, KeyError) as e:
            self.logger.error(e)
            exit(1)
        self._scheduler = Scheduler(schedulable=self,
                                    logger=self.logger,
                                    refresh_rate=self._refresh_rate)
        self._stop_event = threading.Event()
        self._last_id = 0
        self.logger.info('creating an instance of MainActor')

    def on_stop(self):
        self._scheduler.stop()
        self.logger.info(f'stopping an instance of MainActor {self._stop_event.is_set()}')

        # stop all passenger generators
        self.logger.info(f'stopping an instance of Passenger generators')
        [ref.stop(True) for ref in pykka.ActorRegistry.get_by_class(PassengerGenerator)]

        # stop all buses
        self.logger.info(f'stopping an instance of Vehicles')
        [ref.stop(True) for ref in pykka.ActorRegistry.get_by_class(AbstractVehicle)]

        # stop all stops
        self.logger.info(f'stopping an instance of BusStops')
        [ref.stop(True) for ref in pykka.ActorRegistry.get_by_class(AbstractStop)]

        # remove Observer
        Observer.force_remove_instance()

        # stop all counter actors
        self.logger.info(f'stopping an instance of Counters')
        [ref.stop(True) for ref in pykka.ActorRegistry.get_by_class(CounterActor)]

        # remove Time
        Time.force_remove_instance()

    def on_start(self) -> None:
        self._scheduler.start()
        self.logger.info('starting an instance of MainActor')

    @Observer.observe
    def tick(self) -> None:
        # change time
        prv_time = self.time.time_sec()
        self.time.tick()

        # update bus stops
        # for stop in self._stops:
        #     self._passenger_gen.generate_for_one_stop(self._stops[stop], self.time.time_sec())
        self._passenger_gen.generate(self.time.time_sec())

        # update buses
        for record in self._time_table:
            if prv_time <= record <= self.time.time_sec():
                # spawn appropriate buses
                for route in self._time_table[record]:
                    self._last_id += 1
                    bus = Bus.start(self._last_id, route, 50).proxy()
                    self.logger.debug(f'Spawned new bus (id={self._last_id}): {bus}')

        self.logger.info(f'tick, time={self.time}')

    @staticmethod
    def get_instance_proxy(config_path: str = None) -> pykka.ActorProxy:
        main_actors = pykka.ActorRegistry.get_by_class(MainActor)
        if not len(main_actors):
            if not config_path:
                raise ValueError('missing config_path, when no MainActor is present')
            return MainActor.start(config_path).proxy()
        return main_actors[0].proxy()
