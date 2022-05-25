from abc import ABC


class AbstractPassenger(ABC):
    destination: int
    source: int
