from abc import ABC, abstractmethod
from stop import AbstractStop


class AbstractGenerator(ABC):
    @abstractmethod
    def generate_passengers(self, stop: AbstractStop) -> bool:
        pass
