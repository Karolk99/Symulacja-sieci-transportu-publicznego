from abc import ABC, abstractmethod


class LoadDistribution:
    @staticmethod
    def get_dist(vehicle, route):
        return 2 if vehicle.id == 1 else 3


class AbstractGenerator(ABC):
    @abstractmethod
    def generate_passengers(self, stop) -> bool:
        pass
