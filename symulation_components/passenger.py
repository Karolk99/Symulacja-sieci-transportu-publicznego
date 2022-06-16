from abc import ABC


class AbstractPassenger(ABC):
    destination: str
    source: str


class Passenger(AbstractPassenger):
    def __init__(self, destination: str, source: str) -> None:
        self.destination = destination
        self.source = source
