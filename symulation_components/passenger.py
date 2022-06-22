from abc import ABC
from typing import List


class AbstractPassenger(ABC):
    destination: str
    source: str
    path: List[str]
    current_destination: str


class Passenger(AbstractPassenger):
    def __init__(self, destination: str, source: str, path: List[str]) -> None:
        self.destination = destination
        self.source = source
        self.path = path
        self.current_destination = ""
