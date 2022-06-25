from __future__ import annotations

import abc
import logging
import threading
import time
from threading import Thread


class Schedulable(abc.ABC):
    @abc.abstractmethod
    def tick(self) -> None:
        pass


class Scheduler(Thread):
    _ref: Schedulable
    _stop_event: threading.Event
    _refresh_rate: float

    def __init__(self, *, schedulable: Schedulable, refresh_rate: float = 1, logger: logging.Logger = None):
        super().__init__()
        self.logger = logger.getChild('Scheduler') if logger else logging.getLogger(
            'simulation_components.Scheduler')
        self._ref = schedulable
        self._stop_event = threading.Event()
        self._refresh_rate = refresh_rate

    def stop(self):
        self._stop_event.set()
        self.logger.debug('Stopping scheduler')

    def run(self) -> None:
        while not self._stop_event.is_set():
            self._ref.tick()
            time.sleep(self._refresh_rate)
