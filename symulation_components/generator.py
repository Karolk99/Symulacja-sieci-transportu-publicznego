from abc import ABC, abstractmethod
from stop import AbstractStop


class AbstractGenerator(ABC):
    @abstractmethod
    def generete_passengers(self, stop: AbstractStop) -> bool:
        pass
