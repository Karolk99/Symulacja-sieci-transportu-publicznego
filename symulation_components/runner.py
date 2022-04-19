from abc import ABC, abstractmethod


class Runner(ABC):
    @staticmethod
    @abstractmethod
    def run_simulation():
        pass
