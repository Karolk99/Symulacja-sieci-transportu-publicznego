from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from stop import AbstractStop


@dataclass
class Route:
    pass  # TODO:


class AbstractMap(ABC):
    stops: List[AbstractStop]
    routs: List[Route]
