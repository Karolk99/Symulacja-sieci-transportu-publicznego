from __future__ import annotations

import copy
from typing import Any

import pykka


class CounterActor(pykka.ThreadingActor):
    _waiting_passengers_counter: int
    _commuting_passengers_counter: int

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._waiting_passengers_counter = 0
        self._commuting_passengers_counter = 0

    def waiting_passengers(self):
        return self._waiting_passengers_counter

    def waiting_passengers_update(self, num: int):
        self._waiting_passengers_counter += num

    def commuting_passengers(self):
        return self._commuting_passengers_counter

    def commuting_passengers_update(self, num: int):
        self._commuting_passengers_counter += num

    def on_stop(self) -> None:
        print('deleted counter actor')

    def on_start(self) -> None:
        print('started counter actor')

    @staticmethod
    def get_counter_actor() -> pykka.ActorProxy:
        counter_actors = pykka.ActorRegistry.get_by_class(CounterActor)
        if not len(counter_actors):
            return CounterActor.start().proxy()
        return counter_actors[0].proxy()


class Counter:
    @staticmethod
    def _get_counter_actor_proxy():
        counter_actors = pykka.ActorRegistry.get_by_class(CounterActor)
        return counter_actors[0].proxy() if len(counter_actors) else None

    @staticmethod
    def tape(func):
        if not (counter := Counter._get_counter_actor_proxy()):
            counter = CounterActor.start().proxy()

        def func_wrapper(*args, **kwargs):
            match args[0].__class__.__name__:
                case ('BusStop' | 'Bus') as name:
                    prv = len(args[0].passengers)
                    result = func(*args, **kwargs)
                    nxt = len(args[0].passengers)
                    if name == 'BusStop':
                        counter.waiting_passengers_update(nxt - prv)
                    else:
                        counter.commuting_passengers_update(nxt - prv)
                case _:
                    result = func(*args, **kwargs)
            return result

        return func_wrapper
